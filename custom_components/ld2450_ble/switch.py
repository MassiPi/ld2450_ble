"""LD2450 BLE integration sensor platform."""

import logging

from homeassistant.components.switch import SwitchEntity
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

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the platform for LD2450BLE."""
    data: LD2450BLEData = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        LD2450BLESwitch(data.coordinator, data.device, entry.title),
    ]

    async_add_entities(entities)


class LD2450BLESwitch(CoordinatorEntity[LD2450BLECoordinator], SwitchEntity):
    """Generic sensor for LD2450BLE."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: LD2450BLECoordinator,
        device: LD2450BLE,
        name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._device = device
        self._attr_unique_id = f"{device.name}_target_mode"
        self._attr_device_info = DeviceInfo(
            name=name,
            connections={(dr.CONNECTION_BLUETOOTH, device.address)},
            manufacturer="HiLink",
            model="LD2450",
            sw_version=getattr(self._device, "fw_ver"),
        )
        self._attr_native_value = getattr(self._device, "target_mode")

    #@property
    #def name(self):
    #    """Return name."""
    #    return self._name

    @property
    def translation_key(self):
        """Return translation_key."""
        return "target_mode"
        
    @property
    def unique_id(self):
        """Return unique id."""
        return self._attr_unique_id
        
    @property
    def entity_category(self):
        """Return the entity category of the switch."""
        return EntityCategory.CONFIG
        
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = getattr(self._device, "target_mode")
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Unavailable if coordinator isn't connected."""
        return self._coordinator.connected and super().available

    @property
    def is_on(self):
        """Return if multitarget mode is on."""
        if ( self._attr_native_value == 2 ):
            return True
        else:
            return False

    async def async_turn_on(self):
        """Turn on multitarget mode."""
        await self._device._set_target_mode(2)
        
    async def async_turn_off(self):
        """Turn off multitarget mode."""
        await self._device._set_target_mode(1)