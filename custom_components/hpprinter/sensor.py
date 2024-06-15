from datetime import datetime
import logging

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, Platform
from homeassistant.core import HomeAssistant

from .common.base_entity import BaseEntity, async_setup_base_entry
from .common.consts import NUMERIC_UNITS_OF_MEASUREMENT
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

        self._attr_state_class = entity_description.state_class
        self._attr_device_class = entity_description.device_class
        self._attr_native_unit_of_measurement = (
            entity_description.native_unit_of_measurement
        )

        self._set_value()

    def _set_value(self):
        state = self.get_value()

        if state is not None:
            if self.native_unit_of_measurement in [PERCENTAGE]:
                state = float(state)

            elif self.native_unit_of_measurement in NUMERIC_UNITS_OF_MEASUREMENT:
                state = int(state)

            if self.device_class == SensorDeviceClass.DATE:
                state = datetime.fromisoformat(state)

            elif self.device_class == SensorDeviceClass.TIMESTAMP:
                tz = datetime.now().astimezone().tzinfo
                ts = datetime.fromisoformat(state).timestamp()
                state = datetime.fromtimestamp(ts, tz=tz)

            elif self.device_class == SensorDeviceClass.ENUM:
                state = state.lower()

        self._attr_native_value = state

    def _handle_coordinator_update(self) -> None:
        """Fetch new state parameters for the sensor."""
        self._set_value()
        super()._handle_coordinator_update()
