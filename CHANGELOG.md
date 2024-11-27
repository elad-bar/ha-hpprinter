# Changelog

## 2.0.5

- New feature: Print pages (according to printer's supported jobs) buttons [#161](https://github.com/elad-bar/ha-hpprinter/issues/161)

## 2.0.4

- Fix update data when printer goes online [#161](https://github.com/elad-bar/ha-hpprinter/issues/161)
- Set integration title as `{make_and_model} ({hostname})`

## 2.0.3

- Add support for `inktank` cartridge type [#162](https://github.com/elad-bar/ha-hpprinter/issues/162)
- Add sensor of total printed pages per consumable, available for toner only [#72](https://github.com/elad-bar/ha-hpprinter/issues/72)
- Fix HTTPS requests [#160](https://github.com/elad-bar/ha-hpprinter/issues/160)
- Remove startup blocking call
- Improved diagnostics file output (general and device level) with more details

## 2.0.2

- Use HA client session instead of aiohttp directly
- Improved validation for enum sensors (Status and Consumable Type)
- Set update interval per endpoint (Default - 5m), instead of 5 minutes as configuration

| Endpoint                         | Data                                       | Interval | Times a day |
| -------------------------------- | ------------------------------------------ | -------- | ----------- |
| /DevMgmt/ProductConfigDyn.xml    | Main device details                        | 52w      | 0.0027      |
| /DevMgmt/ProductStatusDyn.xml    | Device status                              | 10s      | 8,640       |
| /DevMgmt/ConsumableConfigDyn.xml | Consumables                                | 5m       | 288         |
| /DevMgmt/ProductUsageDyn.xml     | Consumables, Printer, Scanner, Copier, Fax | 5m       | 288         |
| /ePrint/ePrintConfigDyn.xml      | ePrint                                     | 5m       | 288         |
| /IoMgmt/Adapters                 | Network Adapters                           | 5m       | 288         |
| /DevMgmt/NetAppsSecureDyn.xml    | Wifi                                       | 5m       | 288         |

## 2.0.1

- Set printer status to `Off` when printer is offline, instead of reset data
- Add status sensor for main device
- Add sensor statistics attribute
  - measurement - level, remaining level
  - total_increasing - pages, refills
- Add device hostname to unique ID
- Add support for `tonercartridge` cartridge type
- Add translations for Russian, Ukrainian - Using Google Translate
- Add translations for Greek [PR#142](https://github.com/elad-bar/ha-hpprinter/pull/142) by [@ChriZathens](https://github.com/ChriZathens)
- Improved Dutch translations [PR#118](https://github.com/elad-bar/ha-hpprinter/pull/118) by [@hmmbob](https://github.com/hmmbob)
- Improved German translations [PR#130](https://github.com/elad-bar/ha-hpprinter/pull/130) by [@SukramJ](https://github.com/SukramJ)
- Fix Product Status URL for all translations (For error 404)

## 2.0.0

- Fix "detected blocking call to open inside the event loop by custom integration" error

## 2.0.0b10

- Add support for mapping of multicolor consumable (CyanMagentaYellow)
- Change the matching of consumable to its details by marker color instead of station

## 2.0.0b9

- Add fallback mechanism for consumables, if station is not available, will use color mapping
- Fix hassfest failure caused by invalid enums values for translation

## 2.0.0b8

- Fix async dispatcher send
- Change all sensors with date device class to timestamp [#127](https://github.com/elad-bar/ha-hpprinter/issues/127)
- Add fallback mechanism for consumables, if station is not available, will use color mapping

## 2.0.0b7

- Safe code blocks (try / catch / log) for generating entities
- Fix logic of constructing device name if cartridge type is not available

## 2.0.0b6

- When constructing device name, avoid null parts of it [#113](https://github.com/elad-bar/ha-hpprinter/issues/113)
- Changed the logic of errors from not found endpoints [#120](https://github.com/elad-bar/ha-hpprinter/issues/120)
  - On initial load / setting up integration - one of the endpoints must return valid response, otherwise the integration will fail to load.
  - After the integration loaded, it will update data periodically,
  - If one of the endpoints will return 404 (not found) - the data related to it will get reset, DEBUG message will be logged (instead of ERROR)
  - If printer goes offline, all data will be set as Unknown.

## 2.0.0b5

- Support no prefetch mode
- Fix all translations

## v2.0.0b3

- Fix entity translations
- Fix main device manufacture date

## v2.0.0b2

- Fix wrong library usage for slugify, causing wrong translation key to get picked up

## v2.0.0b1

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
