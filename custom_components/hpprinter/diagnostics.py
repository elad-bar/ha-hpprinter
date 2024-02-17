"""Diagnostics support for Tuya."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.device_registry import DeviceEntry

from .common.consts import DOMAIN
from .managers.ha_coordinator import HACoordinator

_LOGGER = logging.getLogger(__name__)


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    _LOGGER.debug("Starting diagnostic tool")

    return await _async_get_diagnostics(hass, entry)


async def async_get_device_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry, device: DeviceEntry
) -> dict[str, Any]:
    """Return diagnostics for a device entry."""
    return await _async_get_diagnostics(hass, entry, device)


async def _async_get_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
    _device: DeviceEntry | None = None,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    _LOGGER.debug("Getting diagnostic information")

    coordinator: HACoordinator = hass.data[DOMAIN][entry.entry_id]

    data = {
        "disabled_by": entry.disabled_by,
        "disabled_polling": entry.pref_disable_polling,
        "debug": await coordinator.get_debug_data(),
    }

    return data


@callback
def _async_device_as_dict(
    hass: HomeAssistant, identifiers, additional_data: dict
) -> dict[str, Any]:
    """Represent a Shinobi monitor as a dictionary."""
    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)

    ha_device = device_registry.async_get_device(identifiers=identifiers)
    data = {}

    if ha_device:
        data["device"] = {
            "name": ha_device.name,
            "name_by_user": ha_device.name_by_user,
            "disabled": ha_device.disabled,
            "disabled_by": ha_device.disabled_by,
            "parameters": additional_data,
            "entities": [],
        }

        ha_entities = er.async_entries_for_device(
            entity_registry,
            device_id=ha_device.id,
            include_disabled_entities=True,
        )

        for entity_entry in ha_entities:
            state = hass.states.get(entity_entry.entity_id)
            state_dict = None
            if state:
                state_dict = dict(state.as_dict())

                # The context doesn't provide useful information in this case.
                state_dict.pop("context", None)

            data["device"]["entities"].append(
                {
                    "disabled": entity_entry.disabled,
                    "disabled_by": entity_entry.disabled_by,
                    "entity_category": entity_entry.entity_category,
                    "device_class": entity_entry.device_class,
                    "original_device_class": entity_entry.original_device_class,
                    "icon": entity_entry.icon,
                    "original_icon": entity_entry.original_icon,
                    "unit_of_measurement": entity_entry.unit_of_measurement,
                    "state": state_dict,
                }
            )

    return data
