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
    "scanprocessing": "Scanning",
    "copying": "Copying",
    "processing": "Printing",
    "canceljob": "Cancelling Job",
    "inpowersave": "Idle",
    "off": "Off",
}

PRINTER_MAIN_DEVICE = "Main"

IGNORED_KEYS = ["@schemaLocation", "Version"]

SIGNAL_HA_DEVICE_CREATED = f"signal_{DOMAIN}_device_created"
SIGNAL_HA_DEVICE_DISCOVERED = f"signal_{DOMAIN}_device_discovered"
CONFIGURATION_FILE = f"{DOMAIN}.config.json"
LEGACY_KEY_FILE = f"{DOMAIN}.key"

UPDATE_API_INTERVAL = timedelta(seconds=1)

DEFAULT_ENTRY_ID = "config"
CONF_TITLE = "title"

DEFAULT_PORT = 80

DATA_KEYS = [CONF_HOST, CONF_PORT, CONF_SSL]

UNIT_OF_MEASUREMENT_PAGES = "pages"
UNIT_OF_MEASUREMENT_REFILLS = "refills"

NUMERIC_UNITS_OF_MEASUREMENT = [UNIT_OF_MEASUREMENT_PAGES, UNIT_OF_MEASUREMENT_REFILLS]

MODEL_PROPERTY = "make_and_model"

PRODUCT_STATUS_ENDPOINT = "/DevMgmt/ProductStatusDyn.xml"
PRODUCT_MAIN_ENDPOINT = "/DevMgmt/ProductConfigDyn.xml"

PRODUCT_STATUS_OFFLINE_PAYLOAD = {
    "ProductStatusDyn": {"Status": [{"StatusCategory": "off"}]}
}

DURATION_UNITS = {
    "s": "seconds",
    "m": "minutes",
    "h": "hours",
    "d": "days",
    "w": "weeks",
}

DEFAULT_INTERVAL = "5m"
