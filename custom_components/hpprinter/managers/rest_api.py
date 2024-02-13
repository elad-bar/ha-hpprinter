import json
import logging
import os
from pathlib import Path
import sys

from aiohttp import ClientResponseError, ClientSession, ClientTimeout, TCPConnector
from defusedxml import ElementTree
import xmltodict

from homeassistant.helpers.aiohttp_client import (
    ENABLE_CLEANUP_CLOSED,
    MAXIMUM_CONNECTIONS,
    MAXIMUM_CONNECTIONS_PER_HOST,
)
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.util import ssl
from homeassistant.util.ssl import SSLCipherList

from ..common.consts import IGNORED_KEYS, SIGNAL_HA_DEVICE_NEW
from ..models.config_data import ConfigData
from ..models.exceptions import IntegrationAPIError
from .ha_config_manager import HAConfigManager

_LOGGER = logging.getLogger(__name__)


class RestAPIv2:
    def __init__(self, hass, config_manager: HAConfigManager):
        self._loop = hass.loop
        self._config_manager = config_manager
        self._hass = hass

        self._session: ClientSession | None = None

        self._data: dict = {}
        self._raw_data: dict = {}

        self._resources: dict | None = None
        self._data_points: dict | None = None

        self._endpoints: list[str] | None = None
        self._all_endpoints: list[str] | None = None

        self._exclude_uri_list: list[str] | None = None
        self._exclude_type_list: list[str] | None = None

        self._is_connected: bool = False

    @property
    def data(self) -> dict | None:
        return self._data

    @property
    def raw_data(self) -> dict | None:
        return self._raw_data

    @property
    def config_data(self) -> ConfigData | None:
        if self._config_manager is not None:
            return self._config_manager.config_data

        return None

    @property
    def _base_url(self):
        config_data = self.config_data

        url = f"{config_data.protocol}://{config_data.hostname}:{config_data.port}"

        return url

    async def initialize(self):
        try:
            if not self.config_data.hostname:
                _LOGGER.error("Failed to get hostname")
                return

            if self._session is None:
                self._session = ClientSession(
                    loop=self._loop, connector=self._get_ssl_connector()
                )

            self._load_exclude_endpoints_configuration()
            self._load_data_points_configuration()

            await self._load_metadata()

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.warning(
                f"Failed to initialize session, Error: {ex}, Line: {line_number}"
            )

    def _load_data_points_configuration(self):
        self._endpoints = []

        self._data_points = self._get_data_from_file("data_points")

        endpoint_objects = self._data_points.get("objects")

        for endpoint in endpoint_objects:
            endpoint_uri = endpoint.get("endpoint")

            if (
                endpoint_uri not in self._endpoints
                and endpoint_uri not in self._exclude_uri_list
            ):
                self._endpoints.append(endpoint_uri)

    def _load_exclude_endpoints_configuration(self):
        endpoints = self._get_data_from_file("endpoint_validations")

        self._exclude_uri_list = endpoints.get("exclude_uri")
        self._exclude_type_list = endpoints.get("exclude_type")

    @staticmethod
    def _get_data_from_file(file_name: str) -> dict:
        config_file = f"{file_name}.json"
        current_path = Path(__file__)
        parent_directory = current_path.parents[1]
        file_path = os.path.join(parent_directory, "data", config_file)

        with open(file_path) as f:
            data = json.load(f)

            return data

    def _get_ssl_connector(self):
        ssl_context = ssl.create_no_verify_ssl_context(SSLCipherList.INTERMEDIATE)

        connector = TCPConnector(
            loop=self._loop,
            enable_cleanup_closed=ENABLE_CLEANUP_CLOSED,
            ssl=ssl_context,
            limit=MAXIMUM_CONNECTIONS,
            limit_per_host=MAXIMUM_CONNECTIONS_PER_HOST,
        )

        return connector

    async def _load_metadata(self):
        self._all_endpoints = []

        endpoints = await self._get_request("/Prefetch?type=dtree")

        if not endpoints:
            raise IntegrationAPIError(self._base_url)

        for endpoint in endpoints:
            is_valid = self._is_valid_endpoint(endpoint)

            if is_valid:
                endpoint_uri = endpoint.get("uri")

                self._all_endpoints.append(endpoint_uri)

        self._is_connected = True

        async_dispatcher_send(
            self._hass,
            SIGNAL_HA_DEVICE_NEW,
            self._config_manager.entry_id,
        )

    def _is_valid_endpoint(self, endpoint: dict):
        endpoint_type = endpoint.get("type")
        uri = endpoint.get("uri")
        methods = endpoint.get("methods", ["get"])

        is_invalid_type = endpoint_type in self._exclude_type_list
        invalid_endpoint_uri = uri in self._exclude_uri_list
        invalid_uri_resource = uri.endswith("Cap.xml")
        invalid_uri_parameter = "{" in uri or "}" in uri
        invalid_methods = "get" not in methods

        invalid_data = [
            is_invalid_type,
            invalid_uri_resource,
            invalid_uri_parameter,
            invalid_methods,
            invalid_endpoint_uri,
        ]

        is_valid = True not in invalid_data

        return is_valid

    async def update(self):
        await self._update_data(self._endpoints)

    async def update_full(self):
        await self._update_data(self._all_endpoints)

    async def _update_data(self, endpoints):
        if not self._is_connected:
            return

        for endpoint in endpoints:
            resource_data = await self._get_request(endpoint)

            self._raw_data[endpoint] = resource_data

        endpoint_objects = self._data_points.get("objects")
        merge_items = self._data_points.get("merge")

        for data_point in endpoint_objects:
            data_point_name = data_point.get("name")
            data_point_endpoint = data_point.get("endpoint")
            data_point_path = data_point.get("path")
            data_point_sub_path = data_point.get("subPath")

            if data_point_endpoint is not None:
                data_item = self._raw_data.get(data_point_endpoint)

                item = self._get_data_item(data_item, data_point_path)

                if data_point_sub_path is not None:
                    if isinstance(item, list):
                        item = self._get_data_items(item, data_point_sub_path)

                    else:
                        item = self._get_sub_items(item, data_point_sub_path)

                self._data[data_point_name] = item

        for merge_item in merge_items:
            self._merge_data_items(merge_item)

    @staticmethod
    def _get_data_item(data_item: dict, path: str):
        path_parts = path.split(".")
        value = data_item.copy()

        for path_part in path_parts:
            value = value.get(path_part)

            if value is None:
                break

        return value

    def _get_sub_items(self, data_item: dict, sub_path_mapping: dict) -> dict:
        data = {}

        for sub_path_name in sub_path_mapping:
            sub_path = sub_path_mapping.get(sub_path_name)

            data[sub_path_name] = self._get_data_item(data_item, sub_path)

        return data

    def _get_data_items(
        self, data_items: list[dict], sub_path_mapping: dict
    ) -> list[dict]:
        result = []

        for data_item in data_items:
            data = self._get_sub_items(data_item, sub_path_mapping)

            result.append(data)

        return result

    def _merge_data_items(self, merge_item: dict):
        key_to = merge_item.get("to")
        key_from = merge_item.get("from")
        key = merge_item.get("key")

        data_items = self._data.get(key_to)
        additional_data = self._data.get(key_from).copy()

        del self._data[key_from]

        additional_data_mapped = {
            additional_data_item[key]: additional_data_item
            for additional_data_item in additional_data
        }

        for data_item in data_items:
            data_item_key = data_item.get(key)
            additional_data_item = additional_data_mapped.get(data_item_key)

            if additional_data_item is not None:
                data_item.update(additional_data_item)

    async def _get_request(self, endpoint: str) -> dict | None:
        result: dict | None = None
        try:
            url = f"{self._base_url}{endpoint}"

            timeout = ClientTimeout(connect=3, sock_read=10)

            async with self._session.get(url, timeout=timeout) as response:
                response.raise_for_status()

                if response.content_type == "application/javascript":
                    content = await response.text()
                    result = json.loads(content)

                else:
                    content = await response.text()
                    result = self._clean_data(content)

                    if result is not None:
                        result_keys = list(result.keys())
                        root_key = result_keys[0]

                        for ignored_key in IGNORED_KEYS:
                            if ignored_key in result[root_key]:
                                del result[root_key][ignored_key]

                _LOGGER.debug(f"Request to {url}")

        except ClientResponseError as cre:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno
            _LOGGER.error(
                f"Failed to get response from {endpoint}, Error: {cre}, Line: {line_number}"
            )

        except Exception as ex:
            print(ex)
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno
            _LOGGER.error(f"Failed to get {endpoint}, Error: {ex}, Line: {line_number}")

        return result

    def _clean_data(self, xml) -> dict:
        xml_data = ElementTree.fromstring(xml)

        self._strip_namespace(xml_data)

        data = xmltodict.parse(ElementTree.tostring(xml_data))

        return data

    def _strip_namespace(self, el):
        if el.tag.startswith("{"):
            el.tag = el.tag.split("}", 1)[1]

        keys = list(el.attrib.keys())

        for k in keys:
            if k.startswith("{"):
                k2 = k.split("}", 1)[1]
                el.attrib[k2] = el.attrib[k]
                del el.attrib[k]

        for child in el:
            self._strip_namespace(child)
