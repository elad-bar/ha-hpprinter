import logging
import sys

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from ..managers.ha_coordinator import HACoordinator
from .consts import DOMAIN, SIGNAL_HA_DEVICE_CREATED
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
    def _async_handle_device(
        entry_id: str, device_key: str, device_data: dict, device_config: dict
    ):
        if entry.entry_id != entry_id:
            return

        coordinator: HACoordinator = hass.data[DOMAIN][entry.entry_id]

        _async_handle_device_created(
            coordinator,
            platform,
            entity_type,
            async_add_entities,
            device_key,
            device_data,
            device_config,
        )

    entry.async_on_unload(
        async_dispatcher_connect(hass, SIGNAL_HA_DEVICE_CREATED, _async_handle_device)
    )


def _async_handle_device_created(
    coordinator: HACoordinator,
    platform: Platform,
    entity_type: type,
    async_add_entities,
    device_key: str,
    device_data: dict,
    device_config: dict,
):
    entities = []

    device_type = device_config.get("device_type")

    entity_descriptions: list[
        IntegrationEntityDescription
    ] = coordinator.config_manager.get_entity_descriptions(
        platform, device_type, device_data
    )

    for entity_description in entity_descriptions:
        try:
            entity = entity_type(entity_description, coordinator, device_key)

            entities.append(entity)

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(
                f"Failed to initialize {platform}.{entity_description.key}, "
                f"Device Type: {device_type}, "
                f"Error: {ex}, Line: {line_number}"
            )

    entity_keys = [entity.unique_id for entity in entities]

    entity_keys_str = ", ".join(entity_keys)

    _LOGGER.debug(
        f"Setting up {platform} {len(entities)} entities, Keys: {entity_keys_str}"
    )

    if entities:
        async_add_entities(entities, True)


class BaseEntity(CoordinatorEntity):
    _translations: dict

    def __init__(
        self,
        entity_description: IntegrationEntityDescription,
        coordinator: HACoordinator,
        device_key: str,
    ):
        super().__init__(coordinator)

        self.entity_description = entity_description

        self._device_key = device_key
        self._device_type = entity_description.device_type

        device_info = coordinator.get_device(device_key)

        entity_name = coordinator.config_manager.get_entity_name(
            entity_description, device_info
        )

        hostname = coordinator.config_manager.config_data.hostname

        unique_id_parts = [
            DOMAIN,
            hostname,
            device_key,
            entity_description.platform,
            entity_description.key,
        ]

        unique_id = slugify("_".join(unique_id_parts))

        self._attr_device_info = device_info
        self._attr_name = entity_name
        self._attr_unique_id = unique_id
        self._attr_icon = entity_description.icon

    @property
    def local_coordinator(self) -> HACoordinator:
        return self.coordinator

    def get_data(self) -> dict:
        data = self.local_coordinator.get_device_data(self._device_key)

        return data

    def get_value(self) -> str:
        data = self.local_coordinator.get_device_value(
            self._device_key, self.entity_description.key
        )

        return data
