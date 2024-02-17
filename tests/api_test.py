import asyncio
import logging
import os
import sys

from custom_components.hpprinter import HAConfigManager
from custom_components.hpprinter.common.consts import DATA_KEYS
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
        await self._api.initialize(True)

        await self._api.update()

        # print(json.dumps(self._api.raw_data, indent=4))
        # print(json.dumps(self._api.data, indent=4))

    async def terminate(self):
        await self._api.terminate()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()

    instance = APITest()

    try:
        loop.create_task(instance.initialize())
        loop.run_forever()

    except KeyboardInterrupt:
        _LOGGER.info("Aborted")

    except Exception as rex:
        _LOGGER.error(f"Error: {rex}")

    finally:
        loop.run_until_complete(instance.terminate())
