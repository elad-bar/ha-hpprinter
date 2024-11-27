import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .common.base_entity import BaseEntity, async_setup_base_entry
from .common.entity_descriptions import IntegrationButtonEntityDescription
from .managers.ha_coordinator import HACoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    await async_setup_base_entry(
        hass,
        entry,
        Platform.BUTTON,
        HAButtonEntity,
        async_add_entities,
    )


class HAButtonEntity(BaseEntity, ButtonEntity):
    """Representation of a sensor."""

    def __init__(
        self,
        entity_description: IntegrationButtonEntityDescription,
        coordinator: HACoordinator,
        device_key: str,
    ):
        super().__init__(entity_description, coordinator, device_key)

    async def async_press(self) -> None:
        """Press the button."""
        await self.local_coordinator.async_print_job(self._entity_description.key)
