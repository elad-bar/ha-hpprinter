from copy import copy
import json
import logging

from homeassistant.config_entries import STORAGE_VERSION, ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_TEMPERATURE_UNIT, CONF_USERNAME
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
    DEFAULT_ENTITY_DESCRIPTIONS,
    IntegrationEntityDescription,
)
from ..models.config_data import ConfigData

_LOGGER = logging.getLogger(__name__)


class HAConfigManager:
    _api_config: dict | None
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

        self._entity_descriptions = {}
        self._protocol_codes = {}
        self._protocol_codes_configuration = {}

        self._hvac_modes = {}
        self._hvac_modes_reverse = {}

        self._fan_modes = {}
        self._fan_modes_reverse = {}

        self._devices = {}
        self._api_config = None
        self._translations = None

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
    def update_interval(self) -> int:
        interval = self._data.get(CONF_UPDATE_INTERVAL, 60)

        return interval

    async def initialize(self, entry_config: dict):
        await self._load()

        self._config_data.update(entry_config)

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
        entity_key = entity_description.key
        platform = entity_description.platform

        device_name = device_info.get("name")

        translation_key = f"component.{DOMAIN}.entity.{platform}.{entity_key}.name"

        translated_name = self._translations.get(
            translation_key, entity_description.name
        )

        _LOGGER.debug(
            f"Translations requested, Key: {translation_key}, "
            f"Entity: {entity_description.name}, Value: {translated_name}"
        )

        entity_name = (
            device_name
            if translated_name is None or translated_name == ""
            else f"{device_name} {translated_name}"
        )

        return entity_name

    async def set_update_interval(self, value: int):
        _LOGGER.debug(f"Set update interval in seconds to to {value}")

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
        data = {CONF_TEMPERATURE_UNIT: {}}

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

            if key in [CONF_PASSWORD, CONF_USERNAME]:
                entry_data.pop(key)

                if stored_value is not None:
                    should_save = True

            else:
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

    def _load_entity_descriptions(self, product_id: str):
        entities = copy(DEFAULT_ENTITY_DESCRIPTIONS)

        self._update_platforms(entities)

        self._entity_descriptions[product_id] = entities

    def _update_platforms(self, entity_descriptions):
        for entity_description in entity_descriptions:
            if (
                entity_description.platform not in self.platforms
                and entity_description.platform is not None
            ):
                self.platforms.append(entity_description.platform)
