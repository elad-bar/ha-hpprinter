import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_STATE, Platform
from homeassistant.core import HomeAssistant

from .common.base_entity import BaseEntity, async_setup_base_entry
from .common.entity_descriptions import IntegrationBinarySensorEntityDescription
from .managers.ha_coordinator import HACoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    await async_setup_base_entry(
        hass,
        entry,
        Platform.BINARY_SENSOR,
        HABinarySensorEntity,
        async_add_entities,
    )


class HABinarySensorEntity(BaseEntity, BinarySensorEntity):
    """Representation of a sensor."""

    def __init__(
        self,
        entity_description: IntegrationBinarySensorEntityDescription,
        coordinator: HACoordinator,
        device_key: str,
    ):
        super().__init__(entity_description, coordinator, device_key)

        self._attr_device_class = entity_description.device_class
        self._entity_on_values = entity_description.on_values

        self._set_value()

    def _set_value(self):
        state = self.get_value()

        is_on = str(state).lower() in self._entity_on_values

        self._attr_is_on = is_on
        self._attr_extra_state_attributes = {ATTR_STATE: state}

    def _handle_coordinator_update(self) -> None:
        """Fetch new state parameters for the sensor."""
        self._set_value()
        super()._handle_coordinator_update()
