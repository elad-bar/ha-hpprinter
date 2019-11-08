import sys
import logging

import requests
import xmltodict
from .const import *

_LOGGER = logging.getLogger(__name__)


class HPPrinterData:
    def __init__(self, host, port=80, is_ssl=False, data_type=None):
        self._host = host
        self._port = port
        self._protocol = "https" if is_ssl else "http"
        self._data_type = data_type
        self._data = None

        self._url = f'{self._protocol}://{self._host}:{self._port}/DevMgmt/{self._data_type}.xml'

    @property
    def data(self):
        return self._data

    def update(self):
        try:
            _LOGGER.debug(f"Updating {self._data_type} from {self._host}")

            printer_data = self.get_data_from_printer()

            result = {}

            for root_key in printer_data:
                root_item = printer_data[root_key]

                item = self.extract_data(root_item, root_key)

                if item is not None:
                    result[root_key] = item

            self._data = result

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f'Failed to update data ({self._data_type}) and parse it, Error: {ex}, Line: {line_number}')

    def get_data_from_printer(self):
        try:
            _LOGGER.debug(f"Retrieving {self._data_type} from {self._host}")

            response = requests.get(self._url, timeout=10)
            response.raise_for_status()

            content = response.text
            for ns in NAMESPACES_TO_REMOVE:
                content = content.replace(f'{ns}:', '')

            json_data = xmltodict.parse(content)

            return json_data

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f'Failed to retrieve data ({self._data_type}) from printer, Error: {ex}, Line: {line_number}')

    def extract_data(self, data_item, data_item_key):
        try:
            ignore = data_item_key in IGNORE_ITEMS
            is_default_array = data_item_key in ARRAY_AS_DEFAULT

            if ignore:
                return None

            elif isinstance(data_item, dict):
                return self.extract_ordered_dictionary(data_item, data_item_key)

            elif isinstance(data_item, list) and not is_default_array:
                return self.extract_array(data_item, data_item_key)

            else:
                return data_item
        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f'Failed to extract {data_item_key} of {data_item}, Error: {ex}, Line: {line_number}')

    def extract_ordered_dictionary(self, data_item, item_key):
        try:
            result = {}

            for data_item_key in data_item:
                next_item = data_item[data_item_key]

                item = self.extract_data(next_item, data_item_key)

                if item is not None:
                    result[data_item_key] = item

            return result
        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f'Failed to extract from dictionary {item_key} of {data_item}, Error: {ex}, Line: {line_number}')

    def extract_array(self, data_item, item_key):
        try:
            result = {}
            keys = ARRAY_KEYS.get(item_key, [])
            index = 0

            for current_item in data_item:
                next_item_key = item_key
                item = {}
                for key in current_item:
                    next_item = current_item[key]

                    item_data = self.extract_data(next_item, key)

                    if item_data is not None:
                        item[key] = item_data

                        if key in keys:
                            next_item_key = f'{next_item_key}_{item[key]}'

                if len(keys) == 0:
                    next_item_key = f'{next_item_key}_{index}'

                result[next_item_key] = item

                index += 1

            return result
        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f'Failed to extract from array {item_key} of {data_item}, Error: {ex}, Line: {line_number}')


class ConsumableConfigDynPrinterData(HPPrinterData):
    def __init__(self, host, port=80, is_ssl=False):
        data_type = "ConsumableConfigDyn"

        super().__init__(host, port, is_ssl, data_type)


class ProductUsageDynPrinterData(HPPrinterData):
    def __init__(self, host, port=80, is_ssl=False):
        data_type = "ProductUsageDyn"

        super().__init__(host, port, is_ssl, data_type)


class ProductStatusDynData(HPPrinterData):
    def __init__(self, host, port=80, is_ssl=False):
        data_type = "ProductStatusDyn"

        super().__init__(host, port, is_ssl, data_type)
