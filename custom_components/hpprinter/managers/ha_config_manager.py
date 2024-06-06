from datetime import timedelta
import json
import logging
import os
from pathlib import Path

import aiofiles

from homeassistant.config_entries import STORAGE_VERSION, ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import translation
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.json import JSONEncoder
from homeassistant.helpers.storage import Store

from ..common.consts import (
    CONF_UPDATE_INTERVAL,
    CONFIGURATION_FILE,
    DEFAULT_ENTRY_ID,
    DEFAULT_NAME,
    DOMAIN,
)
from ..common.entity_descriptions import (
    IntegrationBinarySensorEntityDescription,
    IntegrationEntityDescription,
    IntegrationSensorEntityDescription,
)
from ..common.parameter_type import ParameterType
from ..models.config_data import ConfigData

_LOGGER = logging.getLogger(__name__)


class HAConfigManager:
    _translations: dict | None
    _entry: ConfigEntry | None
    _entry_id: str
    _entry_title: str
    _config_data: ConfigData
    _store: Store | None

    def __init__(self, hass: HomeAssistant | None, entry: ConfigEntry | None):
        self._hass = hass

        self._data = None
        self.platforms = []

        self._entity_descriptions: list[IntegrationEntityDescription] | None = None

        self._translations = None

        self._endpoints: list[str] | None = None

        self._data_points: dict | None = None
        self._exclude_uri_list: list[str] | None = None
        self._exclude_type_list: list[str] | None = None

        self._entry = entry
        self._entry_id = DEFAULT_ENTRY_ID if entry is None else entry.entry_id
        self._entry_title = DEFAULT_NAME if entry is None else entry.title

        self._config_data = ConfigData()

        self._is_initialized = False
        self._store = None

        if hass is not None:
            self._store = Store(
                hass, STORAGE_VERSION, CONFIGURATION_FILE, encoder=JSONEncoder
            )

    @property
    def is_initialized(self) -> bool:
        is_initialized = self._is_initialized

        return is_initialized

    @property
    def entry_id(self) -> str:
        entry_id = self._entry_id

        return entry_id

    @property
    def entry_title(self) -> str:
        entry_title = self._entry_title

        return entry_title

    @property
    def entry(self) -> ConfigEntry:
        entry = self._entry

        return entry

    @property
    def config_data(self) -> ConfigData:
        config_data = self._config_data

        return config_data

    @property
    def update_interval(self) -> timedelta:
        interval = self._data.get(CONF_UPDATE_INTERVAL, 5)
        result = timedelta(minutes=interval)

        return result

    @property
    def endpoints(self) -> list[str] | None:
        endpoints = self._endpoints

        return endpoints

    @property
    def data_points(self) -> dict | None:
        data_points = self._data_points

        return data_points

    async def initialize(self, entry_config: dict):
        await self._load()

        self._config_data.update(entry_config)

        await self._load_exclude_endpoints_configuration()
        await self._load_data_points_configuration()

        self._load_entity_descriptions()

        if self._hass:
            self._translations = await translation.async_get_translations(
                self._hass, self._hass.config.language, "entity", {DOMAIN}
            )

        self._is_initialized = True

    async def remove(self, entry_id: str):
        if self._store is None:
            return

        store_data = await self._store.async_load()

        entries = [DEFAULT_ENTRY_ID, entry_id]

        if store_data is not None:
            should_save = False
            data = {key: store_data[key] for key in store_data}

            for rm_entry_id in entries:
                if rm_entry_id in store_data:
                    data.pop(rm_entry_id)

                    should_save = True

            if should_save:
                await self._store.async_save(data)

    def get_entity_name(
        self, entity_description: IntegrationEntityDescription, device_info: DeviceInfo
    ) -> str:
        translation_key = entity_description.translation_key
        platform = entity_description.platform

        device_name = device_info.get("name")
        translation_key = f"component.{DOMAIN}.entity.{platform}.{translation_key}.name"

        translated_name = self._translations.get(
            translation_key, entity_description.name
        )

        if translated_name is None or translated_name == "":
            entity_name = f"{device_name} {entity_description.name}"

            _LOGGER.warning(
                f"Translations not found, "
                f"Key: {translation_key}, "
                f"Entity: {entity_description.name}"
            )

        else:
            entity_name = f"{device_name} {translated_name}"

            _LOGGER.debug(
                f"Translations requested, "
                f"Key: {translation_key}, "
                f"Entity: {entity_description.name}, "
                f"Value: {translated_name}"
            )

        return entity_name

    async def set_update_interval(self, value: int):
        _LOGGER.debug(f"Set update interval in minutes to to {value}")

        self._data[CONF_UPDATE_INTERVAL] = value

        await self._save()

    def get_debug_data(self) -> dict:
        data = self._config_data.to_dict()

        for key in self._data:
            data[key] = self._data[key]

        return data

    async def _load(self):
        self._data = None

        await self._load_config_from_file()

        if self._data is None:
            self._data = {}

        default_configuration = self._get_defaults()

        for key in default_configuration:
            value = default_configuration[key]

            if key not in self._data:
                self._data[key] = value

        await self._save()

    async def _load_config_from_file(self):
        if self._store is not None:
            store_data = await self._store.async_load()

            if store_data is not None:
                self._data = store_data.get(self._entry_id)

    @staticmethod
    def _get_defaults() -> dict:
        data = {CONF_UPDATE_INTERVAL: 5}

        return data

    async def _save(self):
        if self._store is None:
            return

        should_save = False
        store_data = await self._store.async_load()

        if store_data is None:
            store_data = {}

        entry_data = store_data.get(self._entry_id, {})

        _LOGGER.debug(
            f"Storing config data: {json.dumps(self._data)}, "
            f"Exiting: {json.dumps(entry_data)}"
        )

        for key in self._data:
            stored_value = entry_data.get(key)

            current_value = self._data.get(key)

            if stored_value != current_value:
                should_save = True

                entry_data[key] = self._data[key]

        if DEFAULT_ENTRY_ID in store_data:
            store_data.pop(DEFAULT_ENTRY_ID)
            should_save = True

        if should_save:
            store_data[self._entry_id] = entry_data

            await self._store.async_save(store_data)

    def _load_entity_descriptions(self):
        self._entity_descriptions = []

        for data_point in self._data_points:
            device_type = data_point.get("device_type")
            properties = data_point.get("properties")

            for property_key in properties:
                property_data = properties[property_key]

                if "platform" in property_data:
                    property_platform = property_data.get("platform")
                    exclude = property_data.get("exclude")
                    device_class = property_data.get("device_class")
                    icon = property_data.get("icon")
                    translation_key = property_key

                    if property_platform == str(Platform.BINARY_SENSOR):
                        on_values = [
                            value.lower()
                            for value in property_data.get("on_values", [])
                        ]

                        entity_description = IntegrationBinarySensorEntityDescription(
                            key=property_key,
                            name=property_key,
                            device_type=device_type,
                            exclude=exclude,
                            on_values=on_values,
                            device_class=device_class,
                            icon=icon,
                            translation_key=translation_key,
                        )

                        self._entity_descriptions.append(entity_description)

                    elif property_platform == str(Platform.SENSOR):
                        unit_of_measurement = property_data.get("unit_of_measurement")
                        options = property_data.get("options")

                        entity_description = IntegrationSensorEntityDescription(
                            key=property_key,
                            name=property_key,
                            device_type=device_type,
                            exclude=exclude,
                            native_unit_of_measurement=unit_of_measurement,
                            device_class=device_class,
                            icon=icon,
                            translation_key=translation_key,
                            options=options,
                        )

                        self._entity_descriptions.append(entity_description)

        self._update_platforms()

    def _update_platforms(self):
        for entity_description in self._entity_descriptions:
            if (
                entity_description.platform not in self.platforms
                and entity_description.platform is not None
            ):
                self.platforms.append(entity_description.platform)

    def get_entity_descriptions(
        self, platform: Platform, device_type: str, device_data: dict
    ) -> list[IntegrationEntityDescription]:
        entity_descriptions = [
            entity_description
            for entity_description in self._entity_descriptions
            if self._is_valid_entity(
                entity_description, device_data, device_type, platform
            )
        ]

        return entity_descriptions

    @staticmethod
    def _is_valid_entity(
        entity_description: IntegrationEntityDescription,
        data: dict,
        device_type: str,
        platform: Platform,
    ) -> bool:
        key = entity_description.key
        exclude = entity_description.exclude

        is_valid = (
            entity_description.platform == platform
            and entity_description.device_type == device_type
            and key in data
        )

        if is_valid and exclude:
            for exclude_key in exclude:
                exclude_value = exclude[exclude_key]

                if data.get(exclude_key) == exclude_value:
                    is_valid = False
                    break

        return is_valid

    async def _load_data_points_configuration(self):
        self._endpoints = []

        self._data_points = await self._get_parameters(ParameterType.DATA_POINTS)

        endpoint_objects = self._data_points

        for endpoint in endpoint_objects:
            endpoint_uri = endpoint.get("endpoint")

            if (
                endpoint_uri not in self._endpoints
                and endpoint_uri not in self._exclude_uri_list
            ):
                self._endpoints.append(endpoint_uri)

    async def _load_exclude_endpoints_configuration(self):
        endpoints = await self._get_parameters(ParameterType.ENDPOINT_VALIDATIONS)

        self._exclude_uri_list = endpoints.get("exclude_uri")
        self._exclude_type_list = endpoints.get("exclude_type")

    @staticmethod
    async def _get_parameters(parameter_type: ParameterType) -> dict:
        config_file = f"{parameter_type}.json"
        current_path = Path(__file__)
        parent_directory = current_path.parents[1]
        file_path = os.path.join(parent_directory, "parameters", config_file)

        file = await aiofiles.open(file_path)
        content = await file.read()
        await file.close()

        data = json.loads(content)

        return data

    def is_valid_endpoint(self, endpoint: dict):
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
