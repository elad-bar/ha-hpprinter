from copy import copy
import logging

from homeassistant.const import Platform
from homeassistant.core import Event
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ..common.consts import DOMAIN, UPDATE_API_INTERVAL
from ..common.entity_descriptions import (
    CARTRIDGE_ENTITY_DESCRIPTIONS,
    DEFAULT_ENTITY_DESCRIPTIONS,
    IntegrationEntityDescription,
)
from .ha_config_manager import HAConfigManager
from .rest_api import RestAPIv2

_LOGGER = logging.getLogger(__name__)


class HACoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(
        self,
        hass,
        config_manager: HAConfigManager,
    ):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=config_manager.entry_title,
            update_interval=UPDATE_API_INTERVAL,
            update_method=self._async_update_data,
        )

        self._api = RestAPIv2(hass, config_manager)
        self._config_manager = config_manager
        self._main_device: DeviceInfo | None = None
        self._devices: dict[str, DeviceInfo] = {}
        self._device_type_mapping: dict[str, str] | None = None

    @property
    def config_manager(self):
        return self._config_manager

    async def on_home_assistant_start(self, _event_data: Event):
        await self.initialize()

    async def initialize(self):
        _LOGGER.debug("Initializing coordinator")

        entry = self.config_manager.entry
        platforms = self.config_manager.platforms
        await self.hass.config_entries.async_forward_entry_setups(entry, platforms)

        _LOGGER.info(f"Start loading {DOMAIN} integration, Entry ID: {entry.entry_id}")

        await self._api.initialize()

        await self.async_config_entry_first_refresh()

    def set_devices(self):
        self._device_type_mapping = {
            "Main": "main",
            "Adapters": "adapter",
            "Cartridges": "cartridge",
        }

        self.create_main_device()

        sub_units = [
            entity_description.device_type
            for entity_description in DEFAULT_ENTITY_DESCRIPTIONS
            if entity_description.device_type != "Main"
        ]

        sub_units = list(dict.fromkeys(sub_units))

        for sub_unit in sub_units:
            self.create_sub_unit_device(sub_unit)

            self._device_type_mapping[sub_unit] = sub_unit

        cartridge_details = self._api.data.get("Cartridges")
        for cartridge_data in cartridge_details:
            self.create_cartridge_device(cartridge_data)

        adapter_details = self._api.data.get("Adapters")
        for adapter_data in adapter_details:
            self.create_adapter_device(adapter_data)

    def create_main_device(self):
        entry_id = self.config_entry.entry_id
        entry_title = self.config_entry.entry_id

        product_details = self._api.data.get("Product")

        model = product_details.get("Make And Model")
        serial_number = product_details.get("Serial Number")
        manufacturer = product_details.get("Manufacturer Name")

        device_unique_id = f"{entry_id}.main"

        device_identifier = (DOMAIN, device_unique_id)

        device_info = DeviceInfo(
            identifiers={device_identifier},
            name=entry_title,
            model=model,
            serial_number=serial_number,
            manufacturer=manufacturer,
        )

        self._main_device = device_info
        self._devices[device_unique_id] = device_info

    def create_sub_unit_device(self, sub_unit: str):
        entry_id = self.config_entry.entry_id
        entry_title = self.config_entry.entry_id

        serial_number = self._main_device.get("serial_number")
        model = self._main_device.get("model")
        manufacturer = self._main_device.get("manufacturer")

        device_unique_id = f"{entry_id}.{sub_unit.lower()}"
        main_device_unique_id = f"{entry_id}.main"

        sub_unit_device_name = f"{entry_title} {sub_unit}"

        device_identifier = (DOMAIN, device_unique_id)

        device_info = DeviceInfo(
            identifiers={device_identifier},
            name=sub_unit_device_name,
            model=model,
            serial_number=serial_number,
            manufacturer=manufacturer,
            via_device=(DOMAIN, main_device_unique_id),
        )

        self._devices[device_unique_id] = device_info

    def create_cartridge_device(self, cartridge_data: dict):
        entry_id = self.config_entry.entry_id
        entry_title = self.config_entry.entry_id

        printer_device_unique_id = f"{entry_id}.printer"

        device_name_parts = [entry_title]
        cartridge_type: str = cartridge_data.get("Consumable Type Enum")
        cartridge_color = cartridge_data.get("Marker Color")
        manufacturer = cartridge_data.get("Brand")
        serial_number = cartridge_data.get("Serial Number")
        label_code = cartridge_data.get("Label Code")
        model = cartridge_data.get("Consumable Selectibility Number")

        if cartridge_type == "printhead":
            device_name_parts.append(cartridge_type.capitalize())
            model = cartridge_type

        else:
            device_name_parts.append(cartridge_color)
            device_name_parts.append(cartridge_type.capitalize())

        device_unique_id = f"{entry_id}.cartridge.{label_code}"

        cartridge_device_name = " ".join(device_name_parts)

        device_identifier = (DOMAIN, device_unique_id)

        device_info = DeviceInfo(
            identifiers={device_identifier},
            name=cartridge_device_name,
            model=model,
            serial_number=serial_number,
            manufacturer=manufacturer,
            via_device=(DOMAIN, printer_device_unique_id),
        )

        self._devices[device_unique_id] = device_info

    def create_adapter_device(self, adapter_data: dict):
        entry_id = self.config_entry.entry_id
        entry_title = self.config_entry.entry_id

        serial_number = self._main_device.get("serial_number")
        manufacturer = self._main_device.get("manufacturer")

        adapter_name = adapter_data.get("Name").upper()
        model = (
            adapter_data.get("DeviceConnectivityPortType")
            .replace("Embedded", "")
            .upper()
        )

        device_unique_id = f"{entry_id}.adapter.{adapter_name.lower()}"
        main_device_unique_id = f"{entry_id}.main"

        adapter_device_name = f"{entry_title} Adapter {adapter_name}"

        device_identifier = (DOMAIN, device_unique_id)

        device_info = DeviceInfo(
            identifiers={device_identifier},
            name=adapter_device_name,
            model=model,
            serial_number=serial_number,
            manufacturer=manufacturer,
            via_device=(DOMAIN, main_device_unique_id),
        )

        self._devices[device_unique_id] = device_info

    def get_device(self, device_type: str, item_id: str | None) -> DeviceInfo:
        device_id = self._device_type_mapping.get(device_type)

        if item_id is not None:
            device_id = f"{device_id}.{item_id}"

        device_unique_key = f"{self.config_entry.entry_id}.{device_id}"

        device_info = self._devices.get(device_unique_key)

        return device_info

    def get_device_data(
        self,
        section: str,
        key: str | None = None,
        array_key: str | None = None,
        item_id: str | None = None,
    ):
        data = self._api.data.get(section, {})

        if array_key:
            items = [item for item in data if item.get(array_key) == item_id]

            data = None if len(items) == 0 else items[0]

        if key and data is not None:
            return data.get(key)

        return data

    async def get_debug_data(self) -> dict:
        await self._api.update_full()

        data = {"raw": self._api.raw_data, "processed": self._api.data}

        return data

    async def _async_update_data(self):
        try:
            await self._api.update()

            return self._api.data

        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    def get_entity_descriptions(
        self, platform: Platform
    ) -> list[IntegrationEntityDescription]:
        entity_descriptions = [
            copy(entity_description)
            for entity_description in DEFAULT_ENTITY_DESCRIPTIONS
            if entity_description.platform == platform
        ]

        cartridges = self.get_device_data("Cartridges")

        for cartridge in cartridges:
            cartridge_entity_descriptions = self._get_cartridge_entity_descriptions(
                platform, cartridge
            )

            entity_descriptions.extend(cartridge_entity_descriptions)

        return entity_descriptions

    def _get_cartridge_entity_descriptions(
        self, platform: Platform, cartridge: dict
    ) -> list[IntegrationEntityDescription]:
        entity_descriptions = [
            self._get_cartridge_entity_description(entity_description, cartridge)
            for entity_description in CARTRIDGE_ENTITY_DESCRIPTIONS
            if entity_description.platform == platform
        ]

        result = [
            entity_description
            for entity_description in entity_descriptions
            if entity_description is not None
        ]

        return result

    @staticmethod
    def _get_cartridge_entity_description(
        entity_description: IntegrationEntityDescription, cartridge: dict
    ) -> IntegrationEntityDescription | None:
        is_valid = entity_description.filter(cartridge)

        if not is_valid:
            return None

        result = copy(entity_description)

        return result
