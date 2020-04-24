# Changelog

## 2020-04-24 #4

**Fixed bugs:**

- Fix [\#41](https://github.com/elad-bar/ha-edgeos/issues/41) error while loading entities

## 2020-04-24 #3

**Fixed bugs:**

- Fix saving debug files to save only when `Integration -> Options -> Store...` is checked

## 2020-04-24 #2

**Fixed bugs:**

- Fix [\#40](https://github.com/elad-bar/ha-edgeos/issues/40) returned previous logic of extracting printer status

## 2020-04-24 #1

**Implemented enhancements:**

- Added changelog
- Added ability to configure update entities interval in seconds (Integrations -> Integration Name -> Options)  [\#31](https://github.com/elad-bar/ha-edgeos/issues/31)
- Added validation to add new integration, display error in case printer is unreachable or unsupported [\#15](https://github.com/elad-bar/ha-edgeos/issues/15) [\#11](https://github.com/elad-bar/ha-edgeos/issues/11) 
- Moved code to new file structure
- More logs added for easier debugging
- Removed service `hpprinter.save_debug_data`
- Added option to store debug files from Integration UI -> Option (more details in README)

**Fixed bugs:**

- Fix entities / device / device's area changing names is being reset after restart [\#24](https://github.com/elad-bar/ha-edgeos/issues/24) [\#28](https://github.com/elad-bar/ha-edgeos/issues/28) [\#39](https://github.com/elad-bar/ha-edgeos/issues/39)
- Moved [Updating 2020-04-14 09:21...] to DEBUG [\#39](https://github.com/elad-bar/ha-edgeos/issues/39)

