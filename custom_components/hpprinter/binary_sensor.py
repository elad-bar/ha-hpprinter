"""
Support for Blue Iris binary sensors.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/binary_sensor.blueiris/
"""
import logging

from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.core import HomeAssistant

from .helpers.const import *
from .models.base_entity import async_setup_base_entry, HPPrinterEntity
from .models.entity_data import EntityData

_LOGGER = logging.getLogger(__name__)


CURRENT_DOMAIN = DOMAIN_BINARY_SENSOR


def get_binary_sensor(hass: HomeAssistant, integration_name: str, entity: EntityData):
    binary_sensor = HPPrinterBinarySensor()
    binary_sensor.initialize(hass, integration_name, entity, CURRENT_DOMAIN)

    return binary_sensor


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Set up EdgeOS based off an entry."""
    await async_setup_base_entry(
        hass, entry, async_add_entities, CURRENT_DOMAIN, get_binary_sensor
    )


async def async_unload_entry(hass, config_entry):
    _LOGGER.info(f"async_unload_entry {CURRENT_DOMAIN}: {config_entry}")

    return True


<<<<<<< Updated upstream
class PrinterBinarySensor(Entity):
    """Representation a binary sensor that is updated by MQTT."""

    def __init__(self, hass, printer_name, entity):
        """Initialize the HP Printer Binary Sensor."""
        self._hass = hass
        self._printer_name = printer_name
        self._entity = entity
        self._remove_dispatcher = None
        self._ha = _get_printer(self._hass, self._printer_name)

    @property
    def unique_id(self) -> Optional[str]:
        """Return the name of the node."""
        return f"{DEFAULT_NAME}-{CURRENT_DOMAIN}-{self.name}"

    @property
    def device_info(self):
        return self._ha.device_info

    @property
    def should_poll(self):
        """Return the polling state."""
        return False

    @property
    def name(self):
        """Return the name of the binary sensor."""
        return self._entity.get(ENTITY_NAME)

    @property
    def icon(self) -> Optional[str]:
        """Return the icon of the sensor."""
        return self._entity.get(ENTITY_ICON)
=======
class HPPrinterBinarySensor(HPPrinterEntity):
    """Representation a binary sensor that is updated by EdgeOS."""
>>>>>>> Stashed changes

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return bool(self.entity.state)

    @property
    def state(self):
        """Return the state of the binary sensor."""
        return STATE_ON if self.is_on else STATE_OFF

<<<<<<< Updated upstream
    @property
    def device_state_attributes(self):
        """Return true if the binary sensor is on."""
        return self._entity.get(ENTITY_ATTRIBUTES)

    async def async_added_to_hass(self):
        """Register callbacks."""
        self._remove_dispatcher = async_dispatcher_connect(self._hass, SIGNALS[CURRENT_DOMAIN], self.update_data)

    async def async_will_remove_from_hass(self) -> None:
        if self._remove_dispatcher is not None:
            self._remove_dispatcher()

    @callback
    def update_data(self):
        self.hass.async_add_job(self.async_update_data)

    async def async_update_data(self):
        _LOGGER.debug(f"{CURRENT_DOMAIN} update_data: {self.name} | {self.unique_id}")

        if self._ha is not None:
            self._entity = self._ha.get_entity(CURRENT_DOMAIN, self.name)

            if self._entity is None:
                self._entity = {}
                await self.async_remove()
            else:
                self.async_schedule_update_ha_state(True)
=======
    async def async_added_to_hass_local(self):
        _LOGGER.info(f"Added new {self.name}")

    def _immediate_update(self, previous_state: bool):
        if previous_state != self.entity.state:
            _LOGGER.debug(
                f"{self.name} updated from {previous_state} to {self.entity.state}"
            )

        super()._immediate_update(previous_state)
>>>>>>> Stashed changes
