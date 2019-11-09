"""
This component provides support for Blue Iris.
For more details about this component, please refer to the documentation at
https://home-assistant.io/components/blueiris/
"""
import sys
import logging

import voluptuous as vol

from homeassistant.const import (CONF_HOST, CONF_NAME)
from homeassistant.helpers import config_validation as cv

from .const import *
from .HPPrinterData import *
from .home_assistant import HPPrinterHomeAssistant

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_NAME): cv.string
    }),
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up a Blue Iris component."""
    ha = None
    initialized = False

    try:
        _LOGGER.debug(f"Loading HP Printer domain")
        conf = config[DOMAIN]
        scan_interval = SCAN_INTERVAL
        host = conf.get(CONF_HOST)
        name = conf.get(CONF_NAME, DEFAULT_NAME)

        if host is None:
            ha = HPPrinterHomeAssistant(hass, None, name, None)

            ha.notify_error_message("Host was not configured correctly")

        else:
            hp_data = ProductUsageDynPrinterData(host)

            ha = HPPrinterHomeAssistant(hass, scan_interval, name, hp_data)

            hass.data[DATA_HP_PRINTER] = hp_data

            ha.initialize()

            initialized = True
            _LOGGER.debug(f"HP Printer domain is loaded")

    except Exception as ex:
        exc_type, exc_obj, tb = sys.exc_info()
        line_number = tb.tb_lineno

        if ha is not None:
            ha.notify_error(ex, line_number)

    return initialized
