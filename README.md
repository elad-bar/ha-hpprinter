# Integration to HP Printers
integration is using the web API of the printer

## Configuration
```
hpprinter:
    devies:
        - host: hostname / IP
          name: printer name (Optional - Default - HP Printer)
```

## Output
Following sensors will be created

### Printer details
```
State: # of pages printed
Attributes:
    Color - # of printed documents using color cartridges
    Monochrome - # of printed documents using black cartridges
    Jams - # of print jobs jammed
    Cancelled - # of print jobs that were cancelled
```

### Scanner details
Will work only when printer is all-in-one

```
State: # of pages scanned
Attributes:
    ADF - # of scanned documents from the ADF
    Duplex - # of scanned documents from the ADF using duplex mode
    Flatbed - # of scanned documents from the flatbed
    Jams - # of scanned jammed
    Mispick - # of scanned documents failed to take the document from the feeder
```

### Cartridges details
Per cartridge
   
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

## Services:
### hpprinter.save_debug_data
Stores the XML and JSON of each request and final JSON to files, Path in CONFIG_PATH/*,
Files that will be generated:
 - ProductUsageDyn.XML - Raw XML from HP Printer of Usage Details
 - ProductUsageDyn.json - JSON based on the Raw XML after transformed by the component
 - ConsumableConfigDyn.XML - Raw XML from HP Printer of consumable details
 - ConsumableConfigDyn.json - JSON based on the Raw XML after transformed by the component
 - Final.json - JSON based on the 2 JSONs above, merged into simpler data structure for the HA to create sensor based on