# Integration to HP Printers
integration is using the web API of the printer

## Configuration
```
hpprinter:
   host: hostname / IP
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
```
