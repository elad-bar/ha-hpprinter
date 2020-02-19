# Integration to HP Printers

#### Configuration
Configuration support multiple HP Printer devices through Configuration -> Integrations

\* Custom component doesn't support YAML configuration!, in case you have used it via configuration.yaml, please remove it <br/>
\* In case labels in Configuration -> Integrations -> Add new are note being displayed, please delete the custom component and re-download it   

#### Troubleshooting
Before open an issue, please generate all debug XML / JSON files and attached them to the issue,
to generate debug files, please use `hpprinter.save_debug_data` service (details below)

#### Components:
###### Device status - Binary Sensor
```
State: connected?
```

###### Printer details - Sensor
```
State: # of pages printed
Attributes:
    Color - # of printed documents using color cartridges
    Monochrome - # of printed documents using black cartridges
    Jams - # of print jobs jammed
    Cancelled - # of print jobs that were cancelled
```

###### Scanner details - Sensor (For AIO only)
```
State: # of pages scanned
Attributes:
    ADF - # of scanned documents from the ADF
    Duplex - # of scanned documents from the ADF using duplex mode
    Flatbed - # of scanned documents from the flatbed
    Jams - # of scanned jammed
    Mispick - # of scanned documents failed to take the document from the feeder
```

###### Cartridges details - Sensor (Per cartridge)
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

#### Services:
###### hpprinter.save_debug_data
Stores the XML and JSON of each request and final JSON to files, Path in CONFIG_PATH/*,
Files that will be generated:
 - ProductUsageDyn.XML - Raw XML from HP Printer of Usage Details
 - ProductUsageDyn.json - JSON based on the Raw XML of Usage Details after transformed by the component
 - ConsumableConfigDyn.XML - Raw XML from HP Printer of consumable details
 - ConsumableConfigDyn.json - JSON based on the Raw XML of consumable details after transformed by the component
 - ProductConfigDyn.XML - Raw XML from HP Printer of Config Details
 - ProductConfigDyn.json - JSON based on the Raw XML of Config Details after transformed by the component
 - Final.json - JSON based on the 2 JSONs above, merged into simpler data structure for the HA to create sensor based on
