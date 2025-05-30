"""LD2450 BLE integration sensor platform."""

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfLength
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import EntityCategory

from . import LD2450BLE, LD2450BLECoordinator
from .const import DOMAIN
from .models import LD2450BLEData

_LOGGER = logging.getLogger(__name__)


ANY_PRESENCE = BinarySensorEntityDescription(
    key="any_presence",
    translation_key="any_presence",
    device_class=BinarySensorDeviceClass.OCCUPANCY,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
)
ONE_TARGET = BinarySensorEntityDescription(
    key="one_target",
    translation_key="one_target",
    device_class=BinarySensorDeviceClass.OCCUPANCY,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
)
TWO_TARGET = BinarySensorEntityDescription(
    key="two_target",
    translation_key="two_target",
    device_class=BinarySensorDeviceClass.OCCUPANCY,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
)
THREE_TARGET = BinarySensorEntityDescription(
    key="three_target",
    translation_key="three_target",
    device_class=BinarySensorDeviceClass.OCCUPANCY,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
)

ONE_MOVING = BinarySensorEntityDescription(
    key="one_moving",
    translation_key="one_moving",
    device_class=BinarySensorDeviceClass.MOVING,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
)
TWO_MOVING = BinarySensorEntityDescription(
    key="two_moving",
    translation_key="two_moving",
    device_class=BinarySensorDeviceClass.MOVING,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
)
THREE_MOVING = BinarySensorEntityDescription(
    key="three_moving",
    translation_key="three_moving",
    device_class=BinarySensorDeviceClass.MOVING,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
)

SENSOR_DESCRIPTIONS = (
    [
        ANY_PRESENCE,
        ONE_TARGET,
        TWO_TARGET,
        THREE_TARGET,
        
        ONE_MOVING,
        TWO_MOVING,
        THREE_MOVING,
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
        LD2450BLEBinary(
            data.coordinator,
            data.device,
            entry.title,
            description,
        )
        for description in SENSOR_DESCRIPTIONS
    )


class LD2450BLEBinary(CoordinatorEntity[LD2450BLECoordinator], BinarySensorEntity):
    """Generic sensor for LD2450BLE."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: LD2450BLECoordinator,
        device: LD2450BLE,
        name: str,
        description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._device = device
        self._key = description.key
        self.entity_description = description
        self._attr_unique_id = f"{device.name}_{self._key}"
        self._attr_device_info = DeviceInfo(
            name=name,
            connections={(dr.CONNECTION_BLUETOOTH, device.address)},
            manufacturer="HiLink",
            model="LD2450",
            sw_version=getattr(self._device, "fw_ver"),
        )
        self._attr_native_value = False

    #@property
    #def name(self):
    #    """Return name."""
    #    return self._name

    @property
    def unique_id(self):
        """Return unique id."""
        return self._attr_unique_id
        
    #@property
    #def entity_category(self):
    #    """Return the entity category of the switch."""
    #    return EntityCategory.SENSOR
        
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        match self._key:
            case "any_presence":
                if ( getattr(self._device, "target_one_y") > 0 ):
                    self._attr_native_value = True
                else:
                    self._attr_native_value = False
            case "one_target":
                if ( getattr(self._device, "target_one_y") > 0 and getattr(self._device, "target_two_y") == 0):
                    self._attr_native_value = True
                else:
                    self._attr_native_value = False
            case "two_target":
                if ( getattr(self._device, "target_two_y") > 0 and getattr(self._device, "target_three_y") == 0):
                    self._attr_native_value = True
                else:
                    self._attr_native_value = False
            case "three_target":
                if ( getattr(self._device, "target_three_y") > 0 ):
                    self._attr_native_value = True
                else:
                    self._attr_native_value = False
            case "one_moving":
                if ( getattr(self._device, "target_one_speed") > 0 ):
                    self._attr_native_value = True
                else:
                    self._attr_native_value = False
            case "two_moving":
                if ( getattr(self._device, "target_two_speed") > 0 ):
                    self._attr_native_value = True
                else:
                    self._attr_native_value = False
            case "three_moving":
                if ( getattr(self._device, "target_three_speed") > 0 ):
                    self._attr_native_value = True
                else:
                    self._attr_native_value = False
            case _:
                _LOGGER.error("Wronk KEY for binary sensor: %s", self._key)

        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Unavailable if coordinator isn't connected."""
        return self._coordinator.connected and super().available

    @property
    def is_on(self):
        """Return if multitarget mode is on."""
        return self._attr_native_value