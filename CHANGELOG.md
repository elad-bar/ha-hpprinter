# Changelog

## 2020-04-26

**Fixed bugs:**

- Fix disabled entities still being triggered for updates [\#52](https://github.com/elad-bar/ha-hpprinter/issues/52)
- Fix image drum OPC name [\#51](https://github.com/elad-bar/ha-hpprinter/issues/51)
- Fix Sensor 'status' stays on after power off  [\#45](https://github.com/elad-bar/ha-hpprinter/issues/45)

## 2020-04-26

**Fixed bugs:**

- Fix disabled entities are getting enabled after periodic update (update interval)
- Fix offline printer is not updating entities correctly and after restart [\#45](https://github.com/elad-bar/ha-hpprinter/issues/45)  [\#47](https://github.com/elad-bar/ha-hpprinter/issues/47)

## 2020-04-24 #6

**Fixed bugs:**

- Fix [\#39](https://github.com/elad-bar/ha-hpprinter/issues/39) [\#46](https://github.com/elad-bar/ha-hpprinter/issues/46) missing labels
- Fix [\#44](https://github.com/elad-bar/ha-hpprinter/issues/44) by removing dependency on logger component

## 2020-04-24 #5

**Implemented enhancements:**

- Renamed printer status binary sensor to printer connectivity

**Fixed bugs:**

- Fix [\#42](https://github.com/elad-bar/ha-hpprinter/issues/42) printer sensor

## 2020-04-24 #4

**Fixed bugs:**

- Fix [\#41](https://github.com/elad-bar/ha-hpprinter/issues/41) error while loading entities

## 2020-04-24 #3

**Fixed bugs:**

- Fix saving debug files to save only when `Integration -> Options -> Store...` is checked

## 2020-04-24 #2

**Fixed bugs:**

- Fix [\#40](https://github.com/elad-bar/ha-hpprinter/issues/40) returned previous logic of extracting printer status

## 2020-04-24 #1

**Implemented enhancements:**

- Added changelog
- Added ability to configure update entities interval in seconds (Integrations -> Integration Name -> Options)  [\#31](https://github.com/elad-bar/ha-hpprinter/issues/31)
- Added validation to add new integration, display error in case printer is unreachable or unsupported [\#15](https://github.com/elad-bar/ha-hpprinter/issues/15) [\#11](https://github.com/elad-bar/ha-hpprinter/issues/11) 
- Moved code to new file structure
- More logs added for easier debugging
- Removed service `hpprinter.save_debug_data`
- Added option to store debug files from Integration UI -> Option (more details in README)

**Fixed bugs:**

- Fix entities / device / device's area changing names is being reset after restart [\#24](https://github.com/elad-bar/ha-hpprinter/issues/24) [\#28](https://github.com/elad-bar/ha-hpprinter/issues/28) [\#39](https://github.com/elad-bar/ha-hpprinter/issues/39)
- Moved [Updating 2020-04-14 09:21...] to DEBUG [\#39](https://github.com/elad-bar/ha-hpprinter/issues/39)

