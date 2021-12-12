"""
Support for HP Printer binary sensors.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/binary_sensor.hp_printer/
"""
from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant

from .helpers.const import *
from .models.base_entity import HPPrinterEntity, async_setup_base_entry
from .models.entity_data import EntityData

_LOGGER = logging.getLogger(__name__)

CURRENT_DOMAIN = DOMAIN_SENSOR


def get_device_tracker(hass: HomeAssistant, integration_name: str, entity: EntityData):
    sensor = HPPrinterSensor()
    sensor.initialize(hass, integration_name, entity, CURRENT_DOMAIN)

    return sensor


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Set up HP Printer based off an entry."""
    await async_setup_base_entry(
        hass, entry, async_add_entities, CURRENT_DOMAIN, get_device_tracker
    )


async def async_unload_entry(hass, config_entry):
    _LOGGER.info(f"async_unload_entry {CURRENT_DOMAIN}: {config_entry}")

    return True


class HPPrinterSensor(SensorEntity, HPPrinterEntity):
    """Representation a binary sensor that is updated by HP Printer."""

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.entity.state

    @property
    def device_class(self) -> SensorDeviceClass | str | None:
        """Return the class of this sensor."""
        return self.entity.sensor_device_class

    @property
    def state_class(self) -> SensorStateClass | str | None:
        """Return the class of this sensor."""
        return self.entity.sensor_state_class

    async def async_added_to_hass_local(self):
        _LOGGER.info(f"Added new {self.name}")

    def _immediate_update(self, previous_state: bool):
        if previous_state != self.entity.state:
            _LOGGER.debug(
                f"{self.name} updated from {previous_state} to {self.entity.state}"
            )

        super()._immediate_update(previous_state)
