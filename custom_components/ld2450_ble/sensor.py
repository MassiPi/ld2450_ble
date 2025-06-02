"""LD2450 BLE integration sensor platform."""

import logging
import math
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfLength
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import LD2450BLE, LD2450BLECoordinator
from .const import DOMAIN
from .models import LD2450BLEData

_LOGGER = logging.getLogger(__name__)

TARGET_ONE_X_DESCRIPTION = SensorEntityDescription(
    key="target_one_x",
    translation_key="target_one_x",
    device_class=SensorDeviceClass.DISTANCE,
    entity_registry_enabled_default=False,
    entity_registry_visible_default=False,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
    state_class=SensorStateClass.MEASUREMENT,
)
TARGET_ONE_Y_DESCRIPTION = SensorEntityDescription(
    key="target_one_y",
    translation_key="target_one_y",
    device_class=SensorDeviceClass.DISTANCE,
    entity_registry_enabled_default=False,
    entity_registry_visible_default=False,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
    state_class=SensorStateClass.MEASUREMENT,
)
TARGET_ONE_SPEED_DESCRIPTION = SensorEntityDescription(
    key="target_one_speed",
    translation_key="target_one_speed",
    device_class=None,
    entity_registry_enabled_default=False,
    entity_registry_visible_default=False,
    native_unit_of_measurement="cm/s",
    state_class=SensorStateClass.MEASUREMENT,
)
TARGET_ONE_RESOLUTION_DESCRIPTION = SensorEntityDescription(
    key="target_one_resolution",
    translation_key="target_one_resolution",
    entity_category=EntityCategory.DIAGNOSTIC,
    entity_registry_enabled_default=False,
    entity_registry_visible_default=False,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
)

TARGET_TWO_X_DESCRIPTION = SensorEntityDescription(
    key="target_two_x",
    translation_key="target_two_x",
    device_class=SensorDeviceClass.DISTANCE,
    entity_registry_enabled_default=False,
    entity_registry_visible_default=False,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
    state_class=SensorStateClass.MEASUREMENT,
)
TARGET_TWO_Y_DESCRIPTION = SensorEntityDescription(
    key="target_two_y",
    translation_key="target_two_y",
    device_class=SensorDeviceClass.DISTANCE,
    entity_registry_enabled_default=False,
    entity_registry_visible_default=False,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
    state_class=SensorStateClass.MEASUREMENT,
)
TARGET_TWO_SPEED_DESCRIPTION = SensorEntityDescription(
    key="target_two_speed",
    translation_key="target_two_speed",
    device_class=None,
    entity_registry_enabled_default=False,
    entity_registry_visible_default=False,
    native_unit_of_measurement="cm/s",
    state_class=SensorStateClass.MEASUREMENT,
)
TARGET_TWO_RESOLUTION_DESCRIPTION = SensorEntityDescription(
    key="target_two_resolution",
    translation_key="target_two_resolution",
    entity_category=EntityCategory.DIAGNOSTIC,
    entity_registry_enabled_default=False,
    entity_registry_visible_default=False,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
)

TARGET_THREE_X_DESCRIPTION = SensorEntityDescription(
    key="target_three_x",
    translation_key="target_three_x",
    device_class=SensorDeviceClass.DISTANCE,
    entity_registry_enabled_default=False,
    entity_registry_visible_default=False,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
    state_class=SensorStateClass.MEASUREMENT,
)
TARGET_THREE_Y_DESCRIPTION = SensorEntityDescription(
    key="target_three_y",
    translation_key="target_three_y",
    device_class=SensorDeviceClass.DISTANCE,
    entity_registry_enabled_default=False,
    entity_registry_visible_default=False,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
    state_class=SensorStateClass.MEASUREMENT,
)
TARGET_THREE_SPEED_DESCRIPTION = SensorEntityDescription(
    key="target_three_speed",
    translation_key="target_three_speed",
    device_class=None,
    entity_registry_enabled_default=False,
    entity_registry_visible_default=False,
    native_unit_of_measurement="cm/s",
    state_class=SensorStateClass.MEASUREMENT,
)
TARGET_THREE_RESOLUTION_DESCRIPTION = SensorEntityDescription(
    key="target_three_resolution",
    translation_key="target_three_resolution",
    entity_category=EntityCategory.DIAGNOSTIC,
    entity_registry_enabled_default=False,
    entity_registry_visible_default=False,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
)

#calculated
TARGET_ONE_DISTANCE_DESCRIPTION = SensorEntityDescription(
    key="target_one_distance",
    translation_key="target_one_distance",
    device_class=SensorDeviceClass.DISTANCE,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
    state_class=SensorStateClass.MEASUREMENT,
)
TARGET_TWO_DISTANCE_DESCRIPTION = SensorEntityDescription(
    key="target_two_distance",
    translation_key="target_two_distance",
    device_class=SensorDeviceClass.DISTANCE,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
    state_class=SensorStateClass.MEASUREMENT,
)
TARGET_THREE_DISTANCE_DESCRIPTION = SensorEntityDescription(
    key="target_three_distance",
    translation_key="target_three_distance",
    device_class=SensorDeviceClass.DISTANCE,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
    state_class=SensorStateClass.MEASUREMENT,
)
TARGET_ONE_ANGLE_DESCRIPTION = SensorEntityDescription(
    key="target_one_angle",
    translation_key="target_one_angle",
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement="°",
    state_class=SensorStateClass.MEASUREMENT,
)
TARGET_TWO_ANGLE_DESCRIPTION = SensorEntityDescription(
    key="target_two_angle",
    translation_key="target_two_angle",
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement="°",
    state_class=SensorStateClass.MEASUREMENT,
)
TARGET_THREE_ANGLE_DESCRIPTION = SensorEntityDescription(
    key="target_three_angle",
    translation_key="target_three_angle",
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement="°",
    state_class=SensorStateClass.MEASUREMENT,
)


SENSOR_DESCRIPTIONS = (
    [
        TARGET_ONE_X_DESCRIPTION,
        TARGET_ONE_Y_DESCRIPTION,
        TARGET_ONE_SPEED_DESCRIPTION,
        TARGET_ONE_RESOLUTION_DESCRIPTION,
        
        TARGET_TWO_X_DESCRIPTION,
        TARGET_TWO_Y_DESCRIPTION,
        TARGET_TWO_SPEED_DESCRIPTION,
        TARGET_TWO_RESOLUTION_DESCRIPTION,

        TARGET_THREE_X_DESCRIPTION,
        TARGET_THREE_Y_DESCRIPTION,
        TARGET_THREE_SPEED_DESCRIPTION,
        TARGET_THREE_RESOLUTION_DESCRIPTION,
        
        TARGET_ONE_DISTANCE_DESCRIPTION,
        TARGET_TWO_DISTANCE_DESCRIPTION,
        TARGET_THREE_DISTANCE_DESCRIPTION,

        TARGET_ONE_ANGLE_DESCRIPTION,
        TARGET_TWO_ANGLE_DESCRIPTION,
        TARGET_THREE_ANGLE_DESCRIPTION        
    ]
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the platform for LD2450BLE."""
    data: LD2450BLEData = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        LD2450BLESensor(
            data.coordinator,
            data.device,
            entry.title,
            description,
        )
        for description in SENSOR_DESCRIPTIONS
    )


class LD2450BLESensor(CoordinatorEntity[LD2450BLECoordinator], SensorEntity):
    """Generic sensor for LD2450BLE."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: LD2450BLECoordinator,
        device: LD2450BLE,
        name: str,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._device = device
        self._key = description.key
        self.entity_description = description
        self._attr_unique_id = f"{name}_{self._key}"
        self._attr_device_info = DeviceInfo(
            name=name,
            connections={(dr.CONNECTION_BLUETOOTH, device.address)},
            manufacturer="HiLink",
            model="LD2450",
            sw_version=getattr(self._device, "fw_ver"),
        )
        self._attr_native_value = 0

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        match self._key:
            case "target_one_distance":
                self._attr_native_value = int(math.hypot(getattr(self._device, "target_one_x"), getattr(self._device, "target_one_y")))
            case "target_two_distance":
                self._attr_native_value = int(math.hypot(getattr(self._device, "target_two_x"), getattr(self._device, "target_two_y")))
            case "target_three_distance":
                self._attr_native_value = int(math.hypot(getattr(self._device, "target_three_x"), getattr(self._device, "target_three_y")))
            case "target_one_angle":
                self._attr_native_value = int(math.degrees(math.atan2(getattr(self._device, "target_one_x"), getattr(self._device, "target_one_y"))))
            case "target_two_angle":
                self._attr_native_value = int(math.degrees(math.atan2(getattr(self._device, "target_two_x"), getattr(self._device, "target_two_y"))))
            case "target_three_angle":
                self._attr_native_value = int(math.degrees(math.atan2(getattr(self._device, "target_three_x"), getattr(self._device, "target_three_y"))))
            case _:
                #if not in calculated sensors, just get the value from sensor's state
                self._attr_native_value = getattr(self._device, self._key)
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Unavailable if coordinator isn't connected."""
        return self._coordinator.connected and super().available