from datetime import timedelta

from homeassistant.const import CONF_HOST, CONF_PORT, CONF_SSL

MANUFACTURER = "HP"
DEFAULT_NAME = "HP Printer"
DOMAIN = "hpprinter"
DATA_HP_PRINTER = f"data_{DOMAIN}"

INK_ICON = "mdi:cup-water"
PAGES_ICON = "mdi:book-open-page-variant"
SCANNER_ICON = "mdi:scanner"

PROTOCOLS = {True: "https", False: "http"}

NOT_AVAILABLE = "N/A"

PRINTER_STATUS = {
    "ready": "On",
    "scanProcessing": "Scanning",
    "copying": "Copying",
    "processing": "Printing",
    "cancelJob": "Cancelling Job",
    "inPowerSave": "Idle",
    "": "Off",
}

IGNORED_KEYS = ["@schemaLocation", "Version"]

SIGNAL_HA_DEVICE_NEW = f"signal_{DOMAIN}_device_new"
CONFIGURATION_FILE = f"{DOMAIN}.config.json"
LEGACY_KEY_FILE = f"{DOMAIN}.key"

UPDATE_API_INTERVAL = timedelta(minutes=5)

ADD_COMPONENT_SIGNALS = [SIGNAL_HA_DEVICE_NEW]
DEFAULT_ENTRY_ID = "config"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_TITLE = "title"

DATA_KEYS = [CONF_HOST, CONF_PORT, CONF_SSL]
