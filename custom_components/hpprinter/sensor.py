from datetime import datetime
import logging

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .common.base_entity import BaseEntity, async_setup_base_entry
from .common.entity_descriptions import IntegrationSensorEntityDescription
from .managers.ha_coordinator import HACoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    await async_setup_base_entry(
        hass,
        entry,
        Platform.SENSOR,
        HASensorEntity,
        async_add_entities,
    )


class HASensorEntity(BaseEntity, SensorEntity):
    """Representation of a sensor."""

    def __init__(
        self,
        entity_description: IntegrationSensorEntityDescription,
        coordinator: HACoordinator,
        device_key: str,
    ):
        super().__init__(entity_description, coordinator, device_key)

        self._attr_device_class = entity_description.device_class
        self._attr_native_unit_of_measurement = (
            entity_description.native_unit_of_measurement
        )

    def _handle_coordinator_update(self) -> None:
        """Fetch new state parameters for the sensor."""
        state = self.get_value()

        if self.native_unit_of_measurement in ["%"]:
            state = float(state)

        elif self.native_unit_of_measurement in ["pages", "refill"]:
            state = int(state)

        if self.device_class == SensorDeviceClass.DATE:
            state = datetime.fromisoformat(state)

        self._attr_native_value = state

        self.async_write_ha_state()
