#!/usr/bin/python3
from custom_components.hpprinter.managers.HPDeviceData import *

from homeassistant.core import HomeAssistant

logging.basicConfig(level=logging.DEBUG, filename="myapp.log", filemode="w")

_LOGGER = logging.getLogger(__name__)


class Test:
    def __init__(self):
        _LOGGER.info("Started")

        self._data = None

    @staticmethod
    async def async_parse():
        device_data = HPDeviceData(hass, ConfigManager())
        await device_data.update()

        json_data = json.dumps(device_data.device_data)
        _LOGGER.debug(json_data)

    @staticmethod
    def store_data(file, content):
        print(f"{file} - {content}")

    @staticmethod
    def data_provider(data_type):
        with open(f"samples/ink/{data_type}.json") as json_file:
            data = json.load(json_file)

            return data


if __name__ == "__main__":
    # execute only if run as the entry point into the program

    t = Test()
    hass = HomeAssistant()

    hass.loop.run_until_complete(t.async_parse())
