# Changelog

## 2.0.0b1

- Refactor to full HP Printer EWS support

## v1.0.12

- Fix missing references [Issue #103](https://github.com/elad-bar/ha-hpprinter/issues/103)
- Fix breaking change to ConfigEntry

## v1.0.11

_Minimum HA Version: 2024.1.0b0_

- Set minimum HA version for component to 2024.1.0b0

## 1.0.10

- Fix manifest

## 1.0.9

_Minimum HA Version: 2024.1.0_

- Adjust code to HA 2024.1.0
- Update pre-commit packages

## 1.0.8

- Device and Entity registry - `async_get_registry` is deprecated, change to `async_get`

## 1.0.7

- Added Brazilian Portuguese support, thanks to [@LeandroIssa](https://github.com/LeandroIssa)

## 1.0.6

- Removed entity / device delete upon restarting HA
-

## 1.0.5

- Added support for long term statistics

## 1.0.4

- Upgraded code to support breaking changes of HA v2012.12.0

## 1.0.3

**Implemented enhancements:**

- Added support for VSCode pre-commit

## 1.0.2

**Implemented enhancements:**

- Add configuration URL to add VISIT DEVICE link in device page

## 2020-07-21

**Fixed bugs:**

- Don't block startup of Home Assistant

## 2020-05-29

**Fixed bugs:**

- Ignore cartridge with not enough data (avoid cartridges with N/A)

## 2020-05-18

**Fixed bugs:**

- Logger component is now part of after_dependencies

## 2020-05-06 #2

**Fixed bugs:**

- Upgrade xmltodict to 0.12.0 [\#60](https://github.com/elad-bar/ha-hpprinter/issues/60)

## 2020-05-06 #1

**Fixed bugs:**

- Fix Log is filling with errors [\#57](https://github.com/elad-bar/ha-hpprinter/issues/57)

**Implemented enhancements:**

- More descriptive error message when unable to access printer's API at setup or changing options

## 2020-04-30

**Implemented enhancements:**

- More enhancements to options, ability to change setup details (Edit name and hostname)
- Support new translation format of HA 0.109.0

## 2020-04-28

**Fixed bugs:**

- Fix disabled entity check throws an exception in logs

## 2020-04-27

**Fixed bugs:**

- Fix disabled entities still being triggered for updates [\#52](https://github.com/elad-bar/ha-hpprinter/issues/52)
- Fix image drum OPC name [\#51](https://github.com/elad-bar/ha-hpprinter/issues/51)
- Fix Sensor 'status' stays on after power off [\#45](https://github.com/elad-bar/ha-hpprinter/issues/45)

## 2020-04-26

**Fixed bugs:**

- Fix disabled entities are getting enabled after periodic update (update interval)
- Fix offline printer is not updating entities correctly and after restart [\#45](https://github.com/elad-bar/ha-hpprinter/issues/45) [\#47](https://github.com/elad-bar/ha-hpprinter/issues/47)

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
- Added ability to configure update entities interval in seconds (Integrations -> Integration Name -> Options) [\#31](https://github.com/elad-bar/ha-hpprinter/issues/31)
- Added validation to add new integration, display error in case printer is unreachable or unsupported [\#15](https://github.com/elad-bar/ha-hpprinter/issues/15) [\#11](https://github.com/elad-bar/ha-hpprinter/issues/11)
- Moved code to new file structure
- More logs added for easier debugging
- Removed service `hpprinter.save_debug_data`
- Added option to store debug files from Integration UI -> Option (more details in README)

**Fixed bugs:**

- Fix entities / device / device's area changing names is being reset after restart [\#24](https://github.com/elad-bar/ha-hpprinter/issues/24) [\#28](https://github.com/elad-bar/ha-hpprinter/issues/28) [\#39](https://github.com/elad-bar/ha-hpprinter/issues/39)
- Moved [Updating 2020-04-14 09:21...] to DEBUG [\#39](https://github.com/elad-bar/ha-hpprinter/issues/39)
