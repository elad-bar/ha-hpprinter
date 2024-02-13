import logging
import sys

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from ..managers.ha_coordinator import HACoordinator
from .consts import ADD_COMPONENT_SIGNALS, DOMAIN
from .entity_descriptions import IntegrationEntityDescription

_LOGGER = logging.getLogger(__name__)


async def async_setup_base_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    platform: Platform,
    entity_type: type,
    async_add_entities,
):
    @callback
    def _async_handle_device(entry_id: str):
        if entry.entry_id != entry_id:
            return

        try:
            coordinator: HACoordinator = hass.data[DOMAIN][entry.entry_id]

            entity_descriptions = coordinator.get_entity_descriptions(platform)

            entities = [
                entity_type(entity_description, coordinator)
                for entity_description in entity_descriptions
                if entity_description.platform == platform
            ]

            _LOGGER.debug(f"Setting up {platform} entities: {entities}")

            async_add_entities(entities, True)

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(
                f"Failed to initialize {platform}, Error: {ex}, Line: {line_number}"
            )

    for add_component_signal in ADD_COMPONENT_SIGNALS:
        entry.async_on_unload(
            async_dispatcher_connect(hass, add_component_signal, _async_handle_device)
        )


class BaseEntity(CoordinatorEntity):
    _device_code: str
    _entity_description: IntegrationEntityDescription
    _translations: dict

    def __init__(
        self,
        entity_description: IntegrationEntityDescription,
        coordinator: HACoordinator,
        item_id: str | None,
    ):
        super().__init__(coordinator)

        self.entity_description = entity_description

        self._item_id = item_id
        self._data_key = self._entity_description.data_point_key

        device_info = coordinator.get_device(
            entity_description.device_type, self._item_id
        )

        entity_name = coordinator.config_manager.get_entity_name(
            entity_description, device_info
        )

        unique_id_parts = [DOMAIN, entity_description.platform, entity_description.key]

        unique_id = slugify("_".join(unique_id_parts))

        self._attr_device_info = device_info
        self._attr_name = entity_name
        self._attr_unique_id = unique_id

        self._data = {}

    @property
    def local_coordinator(self) -> HACoordinator:
        return self.coordinator

    @property
    def data(self) -> dict | None:
        return self._data

    def get_data(self) -> dict:
        section = self._entity_description.data_point_section
        array_key = self._entity_description.data_point_item_key

        data = self.local_coordinator.get_device_data(
            section, array_key=array_key, item_id=self._item_id
        )

        return data
