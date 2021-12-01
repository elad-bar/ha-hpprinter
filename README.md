# HP Printer integration for Home Assistant
### Description
Configuration support multiple HP Printer devices through Configuration -> Integrations

[Changelog](https://github.com/elad-bar/ha-hpprinter/blob/master/CHANGELOG.md)

### How to set it up:

Look for "HP Printers Integration" and install

#### Requirements
* HP Printer supporting XML API
  to check printer's compatibility to the component try to get to the printer's XML API (replace placeholder with real IP / Hostname):
  `http://{IP}//DevMgmt/ProductStatusDyn.xml`

#### Basic configuration
* Configuration should be done via Configuration -> Integrations.
* In case you are already using that integration with YAML Configuration - please remove it
* Integration supports **multiple** devices
* In the setup form, the following details are mandatory:
  * Name - Unique
  * Host (or IP)
* Upon submitting the form of creating an integration, a request to the printer will take place and will cause failure in case:
  * Unsupported API
  * Invalid server details - when cannot reach host

#### Settings for Monitoring interfaces, devices, tracked devices and update interval
*Configuration -> Integrations -> {Integration} -> Options* <br />

```
Name - Unique
Host (or IP)
Update Interval: Textbox, number of seconds to update entities, default=60
Log level: Drop-down list, change component's log level (more details below), default=Default
Should store responses?: Check-box, saves XML and JSON files for debugging purpose, default=False
```

###### Log Level's drop-down
New feature to set the log level for the component without need to set log_level in `customization:` and restart or call manually `logger.set_level` and loose it after restart.

Upon startup or integration's option update, based on the value chosen, the component will make a service call to `logger.set_level` for that component with the desired value,

In case `Default` option is chosen, flow will skip calling the service, after changing from any other option to `Default`, it will not take place automatically, only after restart

###### Store responses
Stores the XML and JSON of each request and final JSON to files, Path in CONFIG_PATH/*,
Files that will be generated (Prefix to the file is name of the integration):
 - ProductUsageDyn.XML - Raw XML from HP Printer of Usage Details
 - ProductUsageDyn.json - JSON based on the Raw XML of Usage Details after transformed by the component
 - ConsumableConfigDyn.XML - Raw XML from HP Printer of consumable details
 - ConsumableConfigDyn.json - JSON based on the Raw XML of consumable details after transformed by the component
 - ProductConfigDyn.XML - Raw XML from HP Printer of Config Details
 - ProductConfigDyn.json - JSON based on the Raw XML of Config Details after transformed by the component
 - Final.json - JSON based on the 2 JSONs above, merged into simpler data structure for the HA to create sensor based on

## Components:
#### Device status - Binary Sensor
```
State: connected?
```

#### Printer details - Sensor
```
State: # of pages printed
Attributes:
    Color - # of printed documents using color cartridges
    Monochrome - # of printed documents using black cartridges
    Jams - # of print jobs jammed
    Cancelled - # of print jobs that were cancelled
```

#### Scanner details - Sensor (For AIO only)
```
State: # of pages scanned
Attributes:
    ADF - # of scanned documents from the ADF
    Duplex - # of scanned documents from the ADF using duplex mode
    Flatbed - # of scanned documents from the flatbed
    Jams - # of scanned jammed
    Mispick - # of scanned documents failed to take the document from the feeder
```

#### Cartridges details - Sensor (Per cartridge)
```
State: Remaining level %
Attributes:
    Color
    Type - Ink / Toner / Print head
    Station - Position of the cartridge
    Product Number
    Serial Number
    Manufactured By
    Manufactured At
    Warranty Expiration Date
    Installed At
```
