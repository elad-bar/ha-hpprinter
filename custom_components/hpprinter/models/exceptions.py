from homeassistant.exceptions import HomeAssistantError


class IntegrationAPIError(HomeAssistantError):
    def __init__(self, url):
        self._url = url
        self._message = f"Failed to connect to URL: {url}"

    def __str__(self):
        return self._message
