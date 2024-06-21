"""Config flow to configure."""
from __future__ import annotations

from copy import copy
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowHandler

from ..common.consts import (
    DATA_KEYS,
    DEFAULT_NAME,
    MODEL_PROPERTY,
    PRINTER_MAIN_DEVICE,
    PRODUCT_MAIN_ENDPOINT,
)
from ..models.config_data import ConfigData
from .ha_config_manager import HAConfigManager
from .rest_api import RestAPIv2

_LOGGER = logging.getLogger(__name__)


class IntegrationFlowManager:
    _hass: HomeAssistant
    _entry: ConfigEntry | None

    _flow_handler: FlowHandler
    _flow_id: str

    _config_manager: HAConfigManager

    def __init__(
        self,
        hass: HomeAssistant,
        flow_handler: FlowHandler,
        entry: ConfigEntry | None = None,
    ):
        self._hass = hass
        self._flow_handler = flow_handler
        self._entry = entry
        self._flow_id = "user" if entry is None else "init"
        self._config_manager = HAConfigManager(self._hass, None)

    async def async_step(self, user_input: dict | None = None):
        """Manage the domain options."""
        _LOGGER.info(f"Config flow started, Step: {self._flow_id}, Input: {user_input}")

        form_errors = None

        if user_input is None:
            if self._entry is None:
                user_input = {}

            else:
                user_input = {key: self._entry.data[key] for key in self._entry.data}

        else:
            try:
                await self._config_manager.initialize(user_input)

                api = RestAPIv2(self._hass, self._config_manager)

                await api.initialize()

                if api.is_online:
                    _LOGGER.debug("User inputs are valid")

                    await api.update([PRODUCT_MAIN_ENDPOINT])

                    main_device = api.data.get(PRINTER_MAIN_DEVICE, {})
                    model = main_device.get(MODEL_PROPERTY, DEFAULT_NAME)
                    title = f"{model} ({api.config_data.hostname})"

                    if self._entry is None:
                        data = copy(user_input)

                    else:
                        data = await self.remap_entry_data(user_input)
                        title = self._entry.title

                    return self._flow_handler.async_create_entry(title=title, data=data)

                else:
                    form_errors = {"base": "error_404"}

                    _LOGGER.warning("Failed to setup integration")

            except Exception as ex:
                form_errors = {"base": "error_400"}

                _LOGGER.error(f"Failed to setup integration, Error: {ex}")

        schema = ConfigData.default_schema(user_input)

        return self._flow_handler.async_show_form(
            step_id=self._flow_id, data_schema=schema, errors=form_errors
        )

    async def remap_entry_data(self, options: dict[str, Any]) -> dict[str, Any]:
        config_options = {}
        config_data = {}

        entry = self._entry
        entry_data = entry.data

        for key in options:
            if key in DATA_KEYS:
                config_data[key] = options.get(key, entry_data.get(key))

            else:
                config_options[key] = options.get(key)

        self._hass.config_entries.async_update_entry(
            entry, data=config_data, title=entry.title
        )

        return config_options
