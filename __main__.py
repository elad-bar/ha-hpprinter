#!/usr/bin/python3
import json
# import logging

from custom_components.hpprinter.HPDeviceData import *


class Logger:
    @staticmethod
    def debug(message):
        print(f"DEBUG - {message}")

    @staticmethod
    def error(message):
        print(f"ERROR - {message}")

    @staticmethod
    def store_data(file, content):
        print(f"{file} - {content}")


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    _LOGGER = Logger()  # logging.getLogger(__name__)

    hostname = "192.168.1.30"

    device_data = HPDeviceData(hostname, "HP7740")
    data = device_data.get_data()  # _LOGGER.store_data)

    json_data = json.dumps(data)
    _LOGGER.debug(json_data)


