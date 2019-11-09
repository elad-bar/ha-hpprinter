<h1>Integration to HP Printers</h1>
<p>integration is using the web API of the printer</p>
<br/>
<h2>Configuration</h2>
```
hpprinter:
   host: hostname / IP
   name: printer name (Optional - Default - HP Printer)
```

<h2>Output</h2>
<p>Following sensors will be created</p>
<h3>Printer details</h3>
```
State: # of pages printed
Attributes:
    Color - # of printed documents using color cartridges
    Monochrome - # of printed documents using black cartridges
    Jams - # of print jobs jammed
    Cancelled - # of print jobs that were cancelled
```

<h3>Scanner details</h3>
<p>Will work only when printer is all-in-one</p>
```
State: # of pages scanned
Attributes:
    ADF - # of scanned documents from the ADF
    Duplex - # of scanned documents from the ADF using duplex mode
    Flatbed - # of scanned documents from the flatbed
    Jams - # of scanned jammed
    Mispick - # of scanned documents failed to take the document from the feeder
```

<h3>Cartridges details</h3>
<p>Per cartridge</p>
```
State: Remaining level %
Attributes:
    Color
    Type - Ink / Toner / Print head
    Station - Position of the cartridge
```

