"""LD2450 BLE integration sensor platform."""

import logging

from homeassistant.components.select import SelectEntity
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
        LD2450BLESelect(data.coordinator, data.device, entry.title),
    ]

    async_add_entities(entities)


class LD2450BLESelect(CoordinatorEntity[LD2450BLECoordinator], SelectEntity):
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
        self._attr_unique_id = f"{device.name}_area_mode"
        self._attr_device_info = DeviceInfo(
            name=name,
            connections={(dr.CONNECTION_BLUETOOTH, device.address)},
            manufacturer="HiLink",
            model="LD2450",
            sw_version=getattr(self._device, "fw_ver"),
        )
        self._attr_options = ["Disable", "Monitor Area", "Ignore Area"]
        self._attr_current_option = "Disable"
        self._attr_native_value = 0

    @property
    def translation_key(self):
        """Return translation_key."""
        return "area_mode"
        
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
        match getattr(self._device, "area_mode"):
            case 0:
                self._attr_current_option = "Disable"
            case 1:
                self._attr_current_option = "Monitor Area"
            case 2:
                self._attr_current_option = "Ignore Area"
            case _:
                _LOGGER.error("Unknown area mode: %s", getattr(self._device, "area_mode"))

        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Unavailable if coordinator isn't connected."""
        return self._coordinator.connected and super().available

    async def async_select_option(self, option: str) -> None:
        match option:
            case "Disable":
                await self._device._set_area(0, 
                    getattr(self._device, "area_one_first_vertex_x"), 
                    getattr(self._device, "area_one_first_vertex_y"), 
                    getattr(self._device, "area_one_second_vertex_x"), 
                    getattr(self._device, "area_one_second_vertex_y"), 
                    getattr(self._device, "area_two_first_vertex_x"), 
                    getattr(self._device, "area_two_first_vertex_y"), 
                    getattr(self._device, "area_two_second_vertex_x"), 
                    getattr(self._device, "area_two_second_vertex_y"), 
                    getattr(self._device, "area_three_first_vertex_x"), 
                    getattr(self._device, "area_three_first_vertex_y"), 
                    getattr(self._device, "area_three_second_vertex_x"), 
                    getattr(self._device, "area_three_second_vertex_y"))
            case "Monitor Area":
                await self._device._set_area(1, 
                    getattr(self._device, "area_one_first_vertex_x"), 
                    getattr(self._device, "area_one_first_vertex_y"), 
                    getattr(self._device, "area_one_second_vertex_x"), 
                    getattr(self._device, "area_one_second_vertex_y"), 
                    getattr(self._device, "area_two_first_vertex_x"), 
                    getattr(self._device, "area_two_first_vertex_y"), 
                    getattr(self._device, "area_two_second_vertex_x"), 
                    getattr(self._device, "area_two_second_vertex_y"), 
                    getattr(self._device, "area_three_first_vertex_x"), 
                    getattr(self._device, "area_three_first_vertex_y"), 
                    getattr(self._device, "area_three_second_vertex_x"), 
                    getattr(self._device, "area_three_second_vertex_y"))
            case "Ignore Area":
                await self._device._set_area(2, 
                    getattr(self._device, "area_one_first_vertex_x"), 
                    getattr(self._device, "area_one_first_vertex_y"), 
                    getattr(self._device, "area_one_second_vertex_x"), 
                    getattr(self._device, "area_one_second_vertex_y"), 
                    getattr(self._device, "area_two_first_vertex_x"), 
                    getattr(self._device, "area_two_first_vertex_y"), 
                    getattr(self._device, "area_two_second_vertex_x"), 
                    getattr(self._device, "area_two_second_vertex_y"), 
                    getattr(self._device, "area_three_first_vertex_x"), 
                    getattr(self._device, "area_three_first_vertex_y"), 
                    getattr(self._device, "area_three_second_vertex_x"), 
                    getattr(self._device, "area_three_second_vertex_y"))
            case _:
                _LOGGER.error("Unknown option: %s", option)
