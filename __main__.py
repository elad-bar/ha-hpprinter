from custom_components.hpprinter.managers.HPDeviceData import *

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import HomeAssistant

logging.basicConfig(level=logging.DEBUG, filename="myapp.log", filemode="w")

_LOGGER = logging.getLogger(__name__)


class Test:
    def __init__(self):
        _LOGGER.info("Started")

        self._data = None
        self._config_manager = ConfigManager()

        data = {CONF_HOST: "", CONF_NAME: DEFAULT_NAME}

        config_entry: ConfigEntry = ConfigEntry(
            version=0,
            domain=DOMAIN,
            title=DEFAULT_NAME,
            data=data,
            source="",
            connection_class="",
            system_options={},
        )
        print("1.1")
        self._config_manager.update(config_entry)

        print("1.2")

        self._config_manager.data.file_reader = self.file_data_provider

        print("1.3")

        hass = HomeAssistant()

        print("1.4")

        self._device_data = HPDeviceData(hass, self._config_manager)

    async def async_parse(self):
        print("2.1")

        await self._device_data.update()

        print("2.2")

        json_data = json.dumps(self._device_data.device_data)
        _LOGGER.debug(json_data)

        print("2.3")

        await self.terminate()

    async def terminate(self):
        print("4.1")

        await self._device_data.terminate()

        print("4.2")

    @staticmethod
    def file_data_provider(data_type):
        print(f"3.{data_type}")

        with open(f"samples/ink/{data_type}.json") as json_file:
            data = json.load(json_file)

            return data


if __name__ == "__main__":
    # execute only if run as the entry point into the program

    t = Test()
    hass = HomeAssistant()

    hass.loop.run_until_complete(t.async_parse())
