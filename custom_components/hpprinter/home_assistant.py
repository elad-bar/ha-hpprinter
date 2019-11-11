"""
Support for Blue Iris.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/hpprinter/
"""
import logging

from homeassistant.const import (EVENT_HOMEASSISTANT_START)
from homeassistant.helpers.event import track_time_interval
from homeassistant.util import slugify

from .const import *

_LOGGER = logging.getLogger(__name__)


class HPPrinterHomeAssistant:
    def __init__(self, hass, scan_interval, name, hp_data):
        self._scan_interval = scan_interval
        self._hass = hass
        self._name = name
        self._hp_data = hp_data

    def initialize(self):
        def refresh_data(event_time):
            """Call BlueIris to refresh information."""
            _LOGGER.debug(f"Updating {DOMAIN} component at {event_time}")

            self.update()

        track_time_interval(self._hass, refresh_data, self._scan_interval)

        self._hass.bus.listen_once(EVENT_HOMEASSISTANT_START, refresh_data)

    def notify_error(self, ex, line_number):
        _LOGGER.error(f"Error while initializing {DOMAIN}, exception: {ex},"
                      f" Line: {line_number}")

        self._hass.components.persistent_notification.create(
            f"Error: {ex}<br /> You will need to restart hass after fixing.",
            title=NOTIFICATION_TITLE,
            notification_id=NOTIFICATION_ID)

    def notify_error_message(self, message):
        _LOGGER.error(f"Error while initializing {DOMAIN}, Error: {message}")

        self._hass.components.persistent_notification.create(
            (f"Error: {message}<br /> You will need to restart hass after"
             " fixing."),
            title=NOTIFICATION_TITLE,
            notification_id=NOTIFICATION_ID)

    def update(self):
        self._hp_data.update()

        data = self._hp_data.data
        root = data.get("ProductUsageDyn", {})
        printer_data = root.get("PrinterSubunit")
        scanner_data = root.get("ScannerEngineSubunit")
        consumables_data = root.get("ConsumableSubunit")

        if printer_data is not None:
            self.create_printer_sensor(printer_data)

        if scanner_data is not None:
            self.create_scanner_sensor(scanner_data)

        if consumables_data is not None:
            printer_consumables = consumables_data.get("Consumable")

            if printer_consumables is not None:
                for key in printer_consumables:
                    consumable = printer_consumables.get(key)

                    if consumable is not None:
                        self.create_ink_sensor(consumable)

    def create_printer_sensor(self, printer_data):
        sensor_name = f"{self._name} Printer"

        entity_id = f"sensor.{slugify(sensor_name)}"

        total_printed_pages = self.clean_parameter(printer_data, "TotalImpressions", "0")

        color_printed_pages = self.clean_parameter(printer_data, "ColorImpressions")
        monochrome_printed_pages = self.clean_parameter(printer_data, "MonochromeImpressions")

        printer_jams = self.clean_parameter(printer_data, "Jams")
        if printer_jams == "N/A":
            printer_jams = self.clean_parameter(printer_data, "JamEvents", "0")

        cancelled_print_jobs_number = self.clean_parameter(printer_data, "TotalFrontPanelCancelPresses")

        state = total_printed_pages

        attributes = {
            "Color": color_printed_pages,
            "Monochrome": monochrome_printed_pages,
            "Jams": printer_jams,
            "Cancelled": cancelled_print_jobs_number,
            "unit_of_measurement": "pages",
            "friendly_name": sensor_name
        }

        self._hass.states.set(entity_id, state, attributes)

    def create_scanner_sensor(self, scanner_data):
        sensor_name = f"{self._name} Scanner"

        entity_id = f"sensor.{slugify(sensor_name)}"

        scan_images_count = self.clean_parameter(scanner_data, "ScanImages")
        adf_images_count = self.clean_parameter(scanner_data, "AdfImages")
        duplex_sheets_count = self.clean_parameter(scanner_data, "DuplexSheets")
        flatbed_images = self.clean_parameter(scanner_data, "FlatbedImages")
        scanner_jams = self.clean_parameter(scanner_data, "JamEvents", "0")
        scanner_mispick = self.clean_parameter(scanner_data, "MispickEvents", "0")

        if scan_images_count == 'N/A':
            new_scan_images_count = 0

            if adf_images_count != "N/A" and int(adf_images_count) > 0:
                new_scan_images_count = int(adf_images_count)

            if flatbed_images != "N/A" and int(flatbed_images) > 0:
                new_scan_images_count = new_scan_images_count + int(flatbed_images)

            scan_images_count = new_scan_images_count

        state = scan_images_count

        attributes = {
            "ADF": adf_images_count,
            "Duplex": duplex_sheets_count,
            "Flatbed": flatbed_images,
            "Jams": scanner_jams,
            "Mispick": scanner_mispick,
            "unit_of_measurement": "pages",
            "friendly_name": sensor_name
        }

        self._hass.states.set(entity_id, state, attributes)

    def create_ink_sensor(self, printer_consumable_data):
        color = self.clean_parameter(printer_consumable_data, "MarkerColor")
        head_type = self.clean_parameter(printer_consumable_data, "ConsumableTypeEnum")
        station = self.clean_parameter(printer_consumable_data, "ConsumableStation")
        remaining = self.clean_parameter(printer_consumable_data, "ConsumableRawPercentageLevelRemaining")

        sensor_name = f"{self._name} {color} {head_type}"

        entity_id = f"sensor.{slugify(sensor_name)}"

        state = remaining

        attributes = {
            "Color": color,
            "Type": head_type,
            "Station": station,
            "unit_of_measurement": "%",
            "friendly_name": sensor_name
        }

        self._hass.states.set(entity_id, state, attributes)

    @staticmethod
    def clean_parameter(data_item, data_key, default_value="N/A"):
        result = data_item.get(data_key, {})

        if not isinstance(result, str):
            result = result.get("#text", 0)

        if not isinstance(result, str):
            result = default_value

        return result
