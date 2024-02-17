from homeassistant.exceptions import HomeAssistantError


class IntegrationParameterError(HomeAssistantError):
    def __init__(self, parameter):
        self._parameter = parameter
        self._message = f"Invalid parameter value provided, Parameter: {parameter}"

    def __str__(self):
        return self._message


class IntegrationAPIError(HomeAssistantError):
    def __init__(self, url):
        self._url = url
        self._message = f"Failed to connect to URL: {url}"

    def __str__(self):
        return self._message
