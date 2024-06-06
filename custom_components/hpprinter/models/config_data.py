import voluptuous as vol
from voluptuous import Schema

from homeassistant.const import CONF_HOST, CONF_PORT, CONF_SSL

from ..common.consts import DEFAULT_PORT, PROTOCOLS


class ConfigData:
    _host: str | None
    _ssl: bool | None
    _port: int | None

    def __init__(self):
        self._host = ""
        self._ssl = False
        self._port = DEFAULT_PORT

    @property
    def hostname(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def is_ssl(self) -> bool:
        return self._ssl

    @property
    def protocol(self):
        protocol = PROTOCOLS[self._ssl]

        return protocol

    @property
    def url(self):
        url = f"{self.protocol}://{self.hostname}:{self.port}"

        return url

    def update(self, data: dict):
        self._ssl = str(data.get(CONF_SSL, False)).lower() == str(True).lower()
        self._host = data.get(CONF_HOST)
        self._port = data.get(CONF_PORT, DEFAULT_PORT)

        if self._port is None:
            self._port = DEFAULT_PORT

    def to_dict(self):
        obj = {CONF_HOST: self._host, CONF_PORT: self._port, CONF_SSL: self._ssl}

        return obj

    def __repr__(self):
        to_string = f"{self.to_dict()}"

        return to_string

    @staticmethod
    def default_schema(user_input: dict | None) -> Schema:
        if user_input is None:
            user_input = {}

        new_user_input = {
            vol.Required(CONF_HOST, default=user_input.get(CONF_HOST)): str,
            vol.Required(
                CONF_PORT, default=user_input.get(CONF_PORT, DEFAULT_PORT)
            ): int,
            vol.Optional(CONF_SSL, default=user_input.get(CONF_SSL, False)): bool,
        }

        schema = vol.Schema(new_user_input)

        return schema
