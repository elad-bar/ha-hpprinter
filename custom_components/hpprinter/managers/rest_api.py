from datetime import datetime
import json
import logging
import sys

from aiohttp import ClientResponseError, ClientSession, ClientTimeout, TCPConnector
from defusedxml import ElementTree
from flatten_json import flatten
import xmltodict

from homeassistant.const import CONF_HOST
from homeassistant.helpers.aiohttp_client import (
    ENABLE_CLEANUP_CLOSED,
    MAXIMUM_CONNECTIONS,
    MAXIMUM_CONNECTIONS_PER_HOST,
    async_create_clientsession,
)
from homeassistant.helpers.dispatcher import dispatcher_send
from homeassistant.util import slugify, ssl
from homeassistant.util.ssl import SSLCipherList

from ..common.consts import (
    IGNORED_KEYS,
    PRODUCT_STATUS_ENDPOINT,
    PRODUCT_STATUS_OFFLINE_PAYLOAD,
    SIGNAL_HA_DEVICE_DISCOVERED,
)
from ..models.config_data import ConfigData
from ..models.exceptions import IntegrationAPIError, IntegrationParameterError
from .ha_config_manager import HAConfigManager

_LOGGER = logging.getLogger(__name__)


class RestAPIv2:
    def __init__(self, hass, config_manager: HAConfigManager):
        self._loop = hass.loop
        self._config_manager = config_manager
        self._hass = hass
        self._endpoints = self._config_manager.endpoints

        self._session: ClientSession | None = None

        self._data: dict = {}
        self._data_config: dict = {}
        self._last_update: dict[str, float] = {}

        self._raw_data: dict = {}

        self._is_connected: bool = False

        self._device_dispatched: list[str] = []
        self._support_prefetch: bool = False

        self._is_printer_online: bool = False

    @property
    def data(self) -> dict | None:
        return self._data

    @property
    def data_config(self) -> dict | None:
        return self._data_config

    @property
    def raw_data(self) -> dict | None:
        return self._raw_data

    @property
    def config_data(self) -> ConfigData | None:
        if self._config_manager is not None:
            return self._config_manager.config_data

        return None

    async def terminate(self):
        _LOGGER.info("Terminating session to HP Printer EWS")

        self._is_connected = False

        if self._session is not None:
            await self._session.close()

            self._session = None

    async def initialize(self, throw_exception: bool = False):
        try:
            if not self.config_data.hostname:
                raise IntegrationParameterError(CONF_HOST)

            if self._session is None:
                if self._hass is None:
                    self._session = ClientSession(loop=self._loop)
                else:
                    self._session = async_create_clientsession(hass=self._hass)

            await self._load_metadata()

        except Exception as ex:
            if throw_exception:
                raise ex

            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.warning(
                f"Failed to initialize session, Error: {ex}, Line: {line_number}"
            )

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
        status = await self._revalidate_printer_status()

        if status is None:
            raise IntegrationAPIError(PRODUCT_STATUS_ENDPOINT)

    async def _revalidate_printer_status(self):
        now = datetime.now()
        now_ts = now.timestamp()

        status_endpoint = PRODUCT_STATUS_ENDPOINT
        last_update = self._last_update.get(status_endpoint, 0)

        last_update_diff = int(now_ts - last_update)
        interval = self._config_manager.get_update_interval(status_endpoint)

        if interval > last_update_diff:
            return None

        product_status_data = await self._get_request(status_endpoint)
        self._is_printer_online = product_status_data is not None

        if self._is_printer_online:
            self._last_update = {}

            return product_status_data

        return None

    async def update(self):
        product_status_data: dict | None = None
        endpoints_updated = 0

        if not self._is_printer_online:
            product_status_data = await self._revalidate_printer_status()

            if product_status_data is None:
                return endpoints_updated

        now = datetime.now()
        now_ts = now.timestamp()

        for endpoint in self._endpoints:
            last_update = self._last_update.get(endpoint, 0)
            last_update_diff = int(now_ts - last_update)
            interval = self._config_manager.get_update_interval(endpoint)

            if interval > last_update_diff:
                continue

            if endpoint == PRODUCT_STATUS_ENDPOINT and product_status_data is not None:
                resource_data = product_status_data

            else:
                resource_data = await self._get_request(endpoint)

            endpoints_updated += 1

            if resource_data is None:
                if endpoint == PRODUCT_STATUS_ENDPOINT:
                    self._raw_data[endpoint] = PRODUCT_STATUS_OFFLINE_PAYLOAD

            else:
                self._raw_data[endpoint] = resource_data
                self._last_update[endpoint] = now.timestamp()

        devices = self._get_devices_data()

        self._extract_data(devices)

        _LOGGER.debug(f"Scheduled update: {endpoints_updated} endpoints were updated")

    def _extract_data(self, devices: list[dict]):
        device_data = {}
        device_config = {}

        for item in devices:
            item_config = item.get("config")
            item_data = item.get("data")

            device_type = item_config.get("device_type")
            identifier = item_config.get("identifier")
            properties = item_config.get("properties")
            flat = item_config.get("flat", False)

            device_key = device_type

            if identifier is not None:
                identifier_key = identifier.get("key")
                identifier_mapping = identifier.get("mapping")

                key_data = item_data.get(identifier_key)

                device_id = (
                    item_data.get(identifier_key)
                    if identifier_mapping is None
                    else identifier_mapping.get(key_data)
                )

                if flat:
                    new_items_data = {
                        slugify(f"{device_id}_{key}"): item_data[key]
                        for key in item_data
                        if key != identifier_key
                    }

                    new_properties = {
                        slugify(f"{device_id}_{key}"): properties[key]
                        for key in properties
                        if key != identifier_key
                    }

                    item_data = new_items_data
                    properties = new_properties

                else:
                    device_key = f"{device_type}.{device_id}"

            data = device_data[device_key] if device_key in device_data else {}

            has_data = len(list(item_data.keys())) > 0
            data.update(item_data)

            if has_data:
                device_data[device_key] = data

                if device_key in device_config:
                    config = device_config[device_key]
                    config["properties"].update(properties)

                else:
                    device_config[device_key] = {
                        "device_type": device_type,
                        "properties": properties,
                    }

        self._data_config = device_config
        self._data = device_data

        for device_key in self._data:
            self.device_data_changed(device_key)

    @staticmethod
    def _get_device_from_list(
        data: list[dict], identifier_key: str, device_id
    ) -> dict | None:
        data_items = [
            data_item
            for data_item in data
            if data_item.get(identifier_key) == device_id
        ]

        if data_items:
            return data_items[0]

        else:
            return None

    def _get_device_config(self, device_type: str) -> dict | None:
        data_configs = [
            data_point
            for data_point in self._config_manager.data_points
            if device_type == data_point.get("name")
        ]

        if data_configs:
            return data_configs[0]

        else:
            return None

    @staticmethod
    def _get_data_section(data: dict, path: str) -> dict:
        path_parts = path.split(".")
        result = data

        if result is not None:
            for path_part in path_parts:
                result = result.get(path_part)

        return result

    def _get_devices_data(self):
        devices = []

        for data_point in self._config_manager.data_points:
            endpoint = data_point.get("endpoint")
            path = data_point.get("path")
            properties = data_point.get("properties")

            if endpoint is not None:
                data_item = self._raw_data.get(endpoint)

                data = self._get_data_section(data_item, path)

                if properties is not None:
                    if isinstance(data, list):
                        devices.extend(
                            [
                                self._get_device_data(data_item, properties, data_point)
                                for data_item in data
                            ]
                        )

                    else:
                        device = self._get_device_data(data, properties, data_point)

                        devices.append(device)

        return devices

    @staticmethod
    def _get_device_data(
        data_item: dict, properties: dict, device_config: dict
    ) -> dict:
        device_data = {}

        data_item_flat = {} if data_item is None else flatten(data_item, ".")

        for property_key in properties:
            property_details = properties.get(property_key)
            property_path = property_details.get("path")
            options = property_details.get("options")
            validation_warning = property_details.get("validationWarning", False)
            value = data_item_flat.get(property_path)

            is_valid = True if options is None else str(value).lower() in options

            if value is not None:
                if is_valid:
                    device_data[property_key] = value
                else:
                    log = _LOGGER.warning if validation_warning else _LOGGER.debug

                    log(
                        f"Unsupported value of {property_key}, expecting: {options}, received: {value}"
                    )

        data = {"config": device_config, "data": device_data}

        return data

    async def _get_request(
        self, endpoint: str, ignore_error: bool = False
    ) -> dict | None:
        result: dict | None = None
        start_ts = datetime.now().timestamp()

        try:
            url = f"{self.config_data.url}{endpoint}"

            timeout = ClientTimeout(total=5)

            async with self._session.get(
                url, timeout=timeout, verify_ssl=False
            ) as response:
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

                completed_ts = datetime.now().timestamp()
                time_taken = completed_ts - start_ts
                _LOGGER.debug(f"Request to {url} completed, Time: {time_taken:.3f}s")

        except ClientResponseError as cre:
            if cre.status == 404:
                if not ignore_error:
                    exc_type, exc_obj, tb = sys.exc_info()
                    line_number = tb.tb_lineno
                    completed_ts = datetime.now().timestamp()
                    time_taken = completed_ts - start_ts

                    _LOGGER.debug(
                        f"Failed to get response from {endpoint}, "
                        f"Error: {cre}, "
                        f"Line: {line_number}, "
                        f"Time: {time_taken:.3f}s"
                    )

            else:
                if not ignore_error:
                    exc_type, exc_obj, tb = sys.exc_info()
                    line_number = tb.tb_lineno
                    completed_ts = datetime.now().timestamp()
                    time_taken = completed_ts - start_ts

                    _LOGGER.error(
                        f"Failed to get response from {endpoint}, "
                        f"Error: {cre}, "
                        f"Line: {line_number}, "
                        f"Time: {time_taken:.3f}s"
                    )

        except Exception as ex:
            if not ignore_error:
                exc_type, exc_obj, tb = sys.exc_info()
                line_number = tb.tb_lineno

                completed_ts = datetime.now().timestamp()
                time_taken = completed_ts - start_ts

                _LOGGER.error(
                    f"Failed to get {endpoint}, "
                    f"Error: {ex}, "
                    f"Line: {line_number}, "
                    f"Time: {time_taken:.3f}s"
                )

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

    def device_data_changed(self, device_key: str):
        device_data = self._data.get(device_key)
        device_config = self._data_config.get(device_key)

        if device_key not in self._device_dispatched:
            self._device_dispatched.append(device_key)

            dispatcher_send(
                self._hass,
                SIGNAL_HA_DEVICE_DISCOVERED,
                self._config_manager.entry_id,
                device_key,
                device_data,
                device_config,
            )
