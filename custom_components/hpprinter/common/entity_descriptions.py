from dataclasses import dataclass
from typing import Callable

from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.components.number import NumberEntityDescription
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.const import Platform
from homeassistant.helpers.entity import EntityDescription


@dataclass(frozen=True, kw_only=True)
class IntegrationEntityDescription(EntityDescription):
    platform: Platform | None = None
    device_type: str | None = None
    data_point_section: str | None = None
    data_point_key: str | None = None
    data_point_item_key: str | None = None
    filter: Callable[[dict | None], bool] | None = lambda d: True


@dataclass(frozen=True, kw_only=True)
class IntegrationBinarySensorEntityDescription(
    BinarySensorEntityDescription, IntegrationEntityDescription
):
    platform: Platform | None = Platform.BINARY_SENSOR
    on_value: str | bool | None = None
    attributes: list[str] | None = None


@dataclass(frozen=True, kw_only=True)
class IntegrationSensorEntityDescription(
    SensorEntityDescription, IntegrationEntityDescription
):
    platform: Platform | None = Platform.SENSOR


@dataclass(frozen=True, kw_only=True)
class IntegrationNumberEntityDescription(
    NumberEntityDescription, IntegrationEntityDescription
):
    platform: Platform | None = Platform.NUMBER


DEFAULT_ENTITY_DESCRIPTIONS: list[IntegrationEntityDescription] = [
    IntegrationSensorEntityDescription(
        key="printer_total_pages_printed",
        device_type="Printer",
        data_point_section="Printer",
        data_point_key="Total pages printed",
        native_unit_of_measurement="pages",
    ),
    IntegrationSensorEntityDescription(
        key="printer_total_black_and_white_pages_printed",
        device_type="Printer",
        data_point_section="Printer",
        data_point_key="Total black-and-white pages printed",
        native_unit_of_measurement="pages",
    ),
    IntegrationSensorEntityDescription(
        key="printer_total_color_pages_printed",
        device_type="Printer",
        data_point_section="Printer",
        data_point_key="Total color pages printed",
        native_unit_of_measurement="pages",
    ),
    IntegrationSensorEntityDescription(
        key="printer_total_single_sided_pages_printed",
        device_type="Printer",
        data_point_section="Printer",
        data_point_key="Total single-sided pages printed",
        native_unit_of_measurement="pages",
    ),
    IntegrationSensorEntityDescription(
        key="printer_total_double_sided_pages_printed",
        device_type="Printer",
        data_point_section="Printer",
        data_point_key="Total double-sided pages printed",
        native_unit_of_measurement="pages",
    ),
    IntegrationSensorEntityDescription(
        key="printer_total_jams",
        device_type="Printer",
        data_point_section="Printer",
        data_point_key="Total jams",
        native_unit_of_measurement="pages",
    ),
    IntegrationSensorEntityDescription(
        key="printer_miss_picks",
        device_type="Printer",
        data_point_section="Printer",
        data_point_key="Total miss picks",
        native_unit_of_measurement="pages",
    ),
    IntegrationSensorEntityDescription(
        key="scanner_total_scanned_pages",
        device_type="Scanner",
        data_point_section="Scanner",
        data_point_key="Total scanned pages",
        native_unit_of_measurement="pages",
    ),
    IntegrationSensorEntityDescription(
        key="scanner_total_scanned_pages_from_adf",
        device_type="Scanner",
        data_point_section="Scanner",
        data_point_key="Total scanned pages from ADF",
        native_unit_of_measurement="pages",
    ),
    IntegrationSensorEntityDescription(
        key="scanner_total_pages_from_scanner_glass",
        device_type="Scanner",
        data_point_section="Scanner",
        data_point_key="Total pages from scanner glass",
        native_unit_of_measurement="pages",
    ),
    IntegrationSensorEntityDescription(
        key="scanner_total_double_sided_pages_scanned",
        device_type="Scanner",
        data_point_section="Scanner",
        data_point_key="Total double-sided pages scanned",
        native_unit_of_measurement="pages",
    ),
    IntegrationSensorEntityDescription(
        key="scanner_total_jams",
        device_type="Scanner",
        data_point_section="Scanner",
        data_point_key="Total jams",
        native_unit_of_measurement="pages",
    ),
    IntegrationSensorEntityDescription(
        key="scanner_miss_picks",
        device_type="Scanner",
        data_point_section="Scanner",
        data_point_key="Total miss picks",
        native_unit_of_measurement="pages",
    ),
    IntegrationSensorEntityDescription(
        key="copy_total_copies",
        device_type="Copy",
        data_point_section="Copy",
        data_point_key="Total copies",
        native_unit_of_measurement="pages",
    ),
    IntegrationSensorEntityDescription(
        key="copy_total_copies_from_adf",
        device_type="Copy",
        data_point_section="Copy",
        data_point_key="Total copies from ADF",
        native_unit_of_measurement="pages",
    ),
    IntegrationSensorEntityDescription(
        key="copy_total_pages_from_scanner_glass",
        device_type="Copy",
        data_point_section="Copy",
        data_point_key="Total pages from scanner glass",
        native_unit_of_measurement="pages",
    ),
    IntegrationSensorEntityDescription(
        key="copy_total_black_and_white_copies",
        device_type="Copy",
        data_point_section="Copy",
        data_point_key="Total black-and-white copies",
        native_unit_of_measurement="pages",
    ),
    IntegrationSensorEntityDescription(
        key="copy_total_color_copies",
        device_type="Copy",
        data_point_section="Copy",
        data_point_key="Total color copies",
        native_unit_of_measurement="pages",
    ),
    IntegrationSensorEntityDescription(
        key="fax_total_faxed",
        device_type="Fax",
        data_point_section="Fax",
        data_point_key="Total faxed",
        native_unit_of_measurement="pages",
    ),
    IntegrationBinarySensorEntityDescription(
        key="eprint_registration_state",
        device_type="Main",
        data_point_section="ePrint",
        data_point_key="Registration State",
        on_value="registered",
    ),
    IntegrationBinarySensorEntityDescription(
        key="eprint_status",
        device_type="Main",
        data_point_section="ePrint",
        data_point_key="Status",
        on_value="enabled",
    ),
]

CARTRIDGE_ENTITY_DESCRIPTIONS: list[IntegrationEntityDescription] = [
    IntegrationSensorEntityDescription(
        key="cartridges_consumable_type_enum",
        device_type="Cartridge",
        data_point_section="Cartridges",
        data_point_item_key="Label Code",
        data_point_key="Consumable Type Enum",
    ),
    IntegrationSensorEntityDescription(
        key="cartridges_installation_date",
        device_type="Cartridge",
        data_point_section="Cartridges",
        data_point_item_key="Label Code",
        data_point_key="Installation Date",
    ),
    IntegrationSensorEntityDescription(
        key="cartridges_warranty_expiration_date",
        device_type="Cartridge",
        data_point_section="Cartridges",
        data_point_item_key="Label Code",
        data_point_key="Warranty Expiration Date",
        filter=lambda d: d.get("Consumable Type Enum") != "printhead",
    ),
    IntegrationSensorEntityDescription(
        key="cartridges_consumable_percentage_level_remaining",
        device_type="Cartridge",
        data_point_section="Cartridges",
        data_point_item_key="Label Code",
        data_point_key="Consumable Percentage Level Remaining",
        native_unit_of_measurement="%",
        filter=lambda d: d.get("Consumable Type Enum") != "printhead",
    ),
    IntegrationSensorEntityDescription(
        key="cartridges_estimated_pages_remaining",
        device_type="Cartridge",
        data_point_section="Cartridges",
        data_point_item_key="Label Code",
        data_point_key="Estimated Pages Remaining",
        native_unit_of_measurement="pages",
        filter=lambda d: d.get("Consumable Type Enum") != "printhead",
    ),
    IntegrationSensorEntityDescription(
        key="cartridges_counterfeit_refilled_count",
        device_type="Cartridge",
        data_point_section="Cartridges",
        data_point_item_key="Label Code",
        data_point_key="Counterfeit Refilled Count",
        native_unit_of_measurement="refill",
    ),
    IntegrationSensorEntityDescription(
        key="cartridges_genuine_refilled_count",
        device_type="Cartridge",
        data_point_section="Cartridges",
        data_point_item_key="Label Code",
        data_point_key="Genuine Refilled Count",
        native_unit_of_measurement="refill",
    ),
    IntegrationBinarySensorEntityDescription(
        key="cartridges_consumable_state",
        device_type="Cartridge",
        data_point_section="Cartridges",
        data_point_item_key="Label Code",
        data_point_key="ConsumableState",
        on_value="ok",
    ),
]

ADAPTER_ENTITY_DESCRIPTIONS: list[IntegrationEntityDescription] = [
    IntegrationSensorEntityDescription(
        key="adapters_device_connectivity_port_type",
        device_type="Main",
        data_point_section="Adapters",
        data_point_item_key="Name",
        data_point_key="DeviceConnectivityPortType",
    ),
    IntegrationBinarySensorEntityDescription(
        key="adapters_is_connected",
        device_type="Main",
        data_point_section="Adapters",
        data_point_item_key="Name",
        data_point_key="IsConnected",
        on_value="true",
    ),
]
