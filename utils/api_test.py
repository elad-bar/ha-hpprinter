import asyncio
import json
import logging
import os
import sys

from custom_components.hpprinter import HAConfigManager
from custom_components.hpprinter.common.consts import (
    DATA_KEYS,
    MODEL_PROPERTY,
    PRINTER_MAIN_DEVICE,
    PRODUCT_MAIN_ENDPOINT,
)
from custom_components.hpprinter.managers.rest_api import RestAPIv2
from homeassistant.core import HomeAssistant

DEBUG = str(os.environ.get("DEBUG", False)).lower() == str(True).lower()

log_level = logging.DEBUG if DEBUG else logging.INFO

root = logging.getLogger()
root.setLevel(log_level)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(log_level)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
stream_handler.setFormatter(formatter)
root.addHandler(stream_handler)

_LOGGER = logging.getLogger(__name__)


class APITest:
    def __init__(self):
        self._api: RestAPIv2 | None = None
        self._config_manager: HAConfigManager | None = None

        self._config_data = {
            key: os.environ.get(key)
            for key in DATA_KEYS
        }

    async def initialize(self):
        hass = HomeAssistant(".")

        self._config_manager = HAConfigManager(None, None)
        await self._config_manager.initialize(self._config_data)

        self._api = RestAPIv2(hass, self._config_manager)
        await self._api.initialize()

        await self._api.update([PRODUCT_MAIN_ENDPOINT])

        main_device = self._api.data.get(PRINTER_MAIN_DEVICE)
        model = main_device.get(MODEL_PROPERTY)
        title = f"{model} ({self._api.config_data.hostname})"

        _LOGGER.info(f"Title: {title}")

    def _modify_connection(self, index: int):
        self._api.config_data.update({
            key: os.environ.get(key) if index % 2 == 0 or key != "host" else "127.0.0.1"
            for key in self._api.config_data.to_dict()
        })

    async def update(self, times: int):
        if self._api.is_online:
            for i in range(0, times):
                await self._api.update()

                _LOGGER.debug(json.dumps(self._api.data[PRINTER_MAIN_DEVICE], indent=4))

                await asyncio.sleep(10)

        else:
            _LOGGER.warning("Failed to connect")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()

    instance = APITest()

    try:
        loop.run_until_complete(instance.initialize())
        loop.run_until_complete(instance.update(1))

    except KeyboardInterrupt:
        _LOGGER.info("Aborted")

    except Exception as rex:
        _LOGGER.error(f"Error: {rex}")
