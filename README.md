# HP Printer integration for Home Assistant

### 📌 Maintenance Notice

This integration is no longer actively developed, as I no longer have access to an HP printer for testing.  
However, I will review and approve community contributions (issues and pull requests) if they are tested and confirmed to work.  

If you rely on this integration, please consider contributing fixes and improvements.  
pull requests are welcome!

### Description

Configuration support multiple HP Printer devices through Configuration -> Integrations

[Changelog](https://github.com/elad-bar/ha-hpprinter/blob/master/CHANGELOG.md)

## How to

### Requirements

- HP Printer with EWS (Embedded Web Server) support

### Installations via HACS [![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

- In HACS, look for "HP Printer" and install and restart
- If integration was not found, please add custom repository `elad-bar/hpprinter` as integration
- In Settings --> Devices & Services - (Lower Right) "Add Integration"

### Setup

To add integration use Configuration -> Integrations -> Add `HP Printer`
Integration supports **multiple** accounts and devices

| Fields name | Type    | Required | Default | Description                                  |
| ----------- | ------- | -------- | ------- | -------------------------------------------- |
| Host        | Textbox | +        | -       | Defines hostname or IP of the HP Printer EWS |
| Port        | Textbox | +        | 80      | Defines port of the HP Printer EWS           |
| Is SSL      | Boolean | +        | False   | Defines which protocol to use HTTP/S         |

It is also possible to change configuration after setting up using integration configuration.

#### Validation errors

| Errors                                                 |
| ------------------------------------------------------ |
| Invalid parameters provided                            |
| HP Printer Embedded Web Server (EWS) not was not found |

## Devices

Will extract data of the relevant devices, devices that are not available will be ignored.

### Main device

Device that holds entities related to the integration and relations to other sub devices as described below.

_Binary Sensor_

- ePrint Registered
- ePrint Status

_Sensor_

- Manufacture Date

### Printer

Device holds entities of sensors related to number of pages printed and relation to sub devices of consumables

_Sensor_

- Total pages printed
- Total black-and-white pages printed
- Total color pages printed
- Total single-sided pages printed
- Total double-sided pages printed
- Total jams
- Total miss picks

### Scanner

Device holds entities of sensors related to number of pages scanned

_Sensor_

- Total scanned pages
- Total scanned pages from ADF
- Total double-sided pages scanned
- Total pages from scanner glass
- Total jams
- Total miss picks

### Copy

Device holds entities of sensors related to number of pages copied

_Sensor_

- Total copies
- Total copies from ADF
- Total pages from scanner glass
- Total black-and-white copies
- Total color copies

### Fax

Device holds entities of sensors related to number of pages faxed

_Sensor_

- Total faxed

### Consumable

Devices (device per consumable) holds entities related to consumable (Ink, Toner, Printhead) of a printer device

_Binary Sensor_

- Status

_Sensor_

- Station
- Type
- Installation Date
- Level (will not be available for Printhead)
- Expiration Date (will not be available for Printhead)
- Remaining (will not be available for Printhead)
- Counterfeit Refilled
- Genuine Refilled
- Manufacture Date

## Troubleshooting

Before opening an issue, please provide logs and diagnostic file data related to the issue.

### Logs

For debug log level, please add the following to your config.yaml

```yaml
logger:
  default: warning
  logs:
    custom_components.hpprinter: debug
```

Or use the HA capability in device page:

1. Settings
2. Devices & Services
3. HP Printer
4. 3 dots menu
5. Enable debug logging

When done and would like to extract the log, repeat steps, in step #5 - Disable debug logging

### Diagnostic details

Please attach also diagnostic details of the integration, available in:

1. Settings
2. Devices & Services
3. HP Printer
4. 3 dots menu
5. Download diagnostics

Diagnostic file contains 3 section related to data extracted from the device:

- data.debug.rawData - Raw data extracted from all endpoints of the device, from that source you can extract ideas for additional entities to suggest
- data.debug.devicesConfig - Configuration of mapping to convert data from HP Printer EWS to HA devices and entities, that will be the section that new entities will be added
- data.debug.devicesData - Data extracted for HA entities, just relevant data points, according to mapped objects available in section `data.debug.devicesConfig`

## Translations

Integration translated from English to:

- German
- Danish
- Spanish
- French
- Dutch
- Norwegian
- Polish
- Portuguese

Translation is being auto-generated from Google Translate using `utils/generate_translations.py` script,

```json
{
  "en": "en",
  "de": "de",
  "dk": "da",
  "es": "es",
  "fr": "fr",
  "nb": "no",
  "nl": "nl",
  "pl": "pl",
  "pt-BR": "pt"
}
```

If you would like to add new translation language, please add to the `DESTINATION_LANGUAGES` constant the relevant language,
format is:

```json
{
  "HA language": "Google Translate language"
}
```

Script is translating only, new missing values, it will not override translated values.
