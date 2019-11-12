from datetime import timedelta

DEFAULT_NAME = 'HP Printer'
DOMAIN = "hpprinter"
DATA_HP_PRINTER = f'data_{DOMAIN}'
SIGNAL_UPDATE_HP_PRINTER = f'updates_{DOMAIN}'
NOTIFICATION_ID = f'{DOMAIN}_notification'
NOTIFICATION_TITLE = f'{DEFAULT_NAME} Setup'

SCAN_INTERVAL = timedelta(minutes=60)

SENSOR_ENTITY_ID = 'sensor.{}_{}'
BINARY_SENSOR_ENTITY_ID = 'binary_sensor.{}_{}'

NAMESPACES_TO_REMOVE = ["ccdyn", "ad", "dd", "dd2", "pudyn", "psdyn", "xsd", "pscat", "locid"]

IGNORE_ITEMS = [
    "@xsi:schemaLocation",
    "@xmlns:xsd",
    "@xmlns:dd",
    "@xmlns:dd2",
    "@xmlns:ccdyn",
    "@xmlns:xsi",
    "@xmlns:pudyn",
    "@xmlns:ad",
    "@xmlns:psdyn",
    "@xmlns:pscat",
    "@xmlns:locid",
    "PECounter"
]

ARRAY_KEYS = {
    "UsageByMedia": [],
    "SupportedConsumable": ["ConsumableTypeEnum", "ConsumableLabelCode"],
    "SupportedConsumableInfo": ["ConsumableUsageType"]
}

ARRAY_AS_DEFAULT = ["AlertDetailsUserAction", "ConsumableStateAction"]