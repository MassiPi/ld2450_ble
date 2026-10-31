"""LD2450 BLE integration sensor platform."""

import logging
from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfLength, UnitOfTime
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.restore_state import RestoreEntity

from . import LD2450BLE, LD2450BLECoordinator
from .const import DOMAIN
from .models import LD2450BLEData

_LOGGER = logging.getLogger(__name__)

PRESENCE_TIMEOUT_DESCRIPTION = NumberEntityDescription(
    key="presence_timeout",
    translation_key="presence_timeout",
    name="Presence Timeout",
    icon="mdi:timer-outline",
    entity_category=EntityCategory.CONFIG,
    mode=NumberMode.BOX,
    native_min_value=0,
    native_max_value=300,
    native_step=1,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement=UnitOfTime.SECONDS,
)

AREA_ONE_FIRST_VERTEX_X_DESCRIPTION = NumberEntityDescription(
    key="area_one_first_vertex_x",
    translation_key="area_one_first_vertex_x",
    device_class=NumberDeviceClass.DISTANCE,
    mode="slider",
    native_min_value=-5000,
    native_max_value=5000,
    native_step=100,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
)
AREA_ONE_FIRST_VERTEX_Y_DESCRIPTION = NumberEntityDescription(
    key="area_one_first_vertex_y",
    translation_key="area_one_first_vertex_y",
    device_class=NumberDeviceClass.DISTANCE,
    mode="slider",
    native_min_value=0,
    native_max_value=7300,
    native_step=100,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
)
AREA_ONE_SECOND_VERTEX_X_DESCRIPTION = NumberEntityDescription(
    key="area_one_second_vertex_x",
    translation_key="area_one_second_vertex_x",
    device_class=NumberDeviceClass.DISTANCE,
    mode="slider",
    native_min_value=-5000,
    native_max_value=5000,
    native_step=100,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
)
AREA_ONE_SECOND_VERTEX_Y_DESCRIPTION = NumberEntityDescription(
    key="area_one_second_vertex_y",
    translation_key="area_one_second_vertex_y",
    device_class=NumberDeviceClass.DISTANCE,
    mode="slider",
    native_min_value=0,
    native_max_value=7300,
    native_step=100,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
)

AREA_TWO_FIRST_VERTEX_X_DESCRIPTION = NumberEntityDescription(
    key="area_two_first_vertex_x",
    translation_key="area_two_first_vertex_x",
    device_class=NumberDeviceClass.DISTANCE,
    mode="slider",
    native_min_value=-5000,
    native_max_value=5000,
    native_step=100,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
)
AREA_TWO_FIRST_VERTEX_Y_DESCRIPTION = NumberEntityDescription(
    key="area_two_first_vertex_y",
    translation_key="area_two_first_vertex_y",
    device_class=NumberDeviceClass.DISTANCE,
    mode="slider",
    native_min_value=0,
    native_max_value=7300,
    native_step=100,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
)
AREA_TWO_SECOND_VERTEX_X_DESCRIPTION = NumberEntityDescription(
    key="area_two_second_vertex_x",
    translation_key="area_two_second_vertex_x",
    device_class=NumberDeviceClass.DISTANCE,
    mode="slider",
    native_min_value=-5000,
    native_max_value=5000,
    native_step=100,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
)
AREA_TWO_SECOND_VERTEX_Y_DESCRIPTION = NumberEntityDescription(
    key="area_two_second_vertex_y",
    translation_key="area_two_second_vertex_y",
    device_class=NumberDeviceClass.DISTANCE,
    mode="slider",
    native_min_value=0,
    native_max_value=7300,
    native_step=100,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
)

AREA_THREE_FIRST_VERTEX_X_DESCRIPTION = NumberEntityDescription(
    key="area_three_first_vertex_x",
    translation_key="area_three_first_vertex_x",
    device_class=NumberDeviceClass.DISTANCE,
    mode="slider",
    native_min_value=-5000,
    native_max_value=5000,
    native_step=100,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
)
AREA_THREE_FIRST_VERTEX_Y_DESCRIPTION = NumberEntityDescription(
    key="area_three_first_vertex_y",
    translation_key="area_three_first_vertex_y",
    device_class=NumberDeviceClass.DISTANCE,
    mode="slider",
    native_min_value=0,
    native_max_value=7300,
    native_step=100,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
)
AREA_THREE_SECOND_VERTEX_X_DESCRIPTION = NumberEntityDescription(
    key="area_three_second_vertex_x",
    translation_key="area_three_second_vertex_x",
    device_class=NumberDeviceClass.DISTANCE,
    mode="slider",
    native_min_value=-5000,
    native_max_value=5000,
    native_step=100,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
)
AREA_THREE_SECOND_VERTEX_Y_DESCRIPTION = NumberEntityDescription(
    key="area_three_second_vertex_y",
    translation_key="area_three_second_vertex_y",
    device_class=NumberDeviceClass.DISTANCE,
    mode="slider",
    native_min_value=0,
    native_max_value=7300,
    native_step=100,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
    native_unit_of_measurement=UnitOfLength.MILLIMETERS,
)

SENSOR_DESCRIPTIONS = (
    [
        PRESENCE_TIMEOUT_DESCRIPTION,
        AREA_ONE_FIRST_VERTEX_X_DESCRIPTION,
        AREA_ONE_FIRST_VERTEX_Y_DESCRIPTION,
        AREA_ONE_SECOND_VERTEX_X_DESCRIPTION,
        AREA_ONE_SECOND_VERTEX_Y_DESCRIPTION,
        AREA_TWO_FIRST_VERTEX_X_DESCRIPTION,
        AREA_TWO_FIRST_VERTEX_Y_DESCRIPTION,
        AREA_TWO_SECOND_VERTEX_X_DESCRIPTION,
        AREA_TWO_SECOND_VERTEX_Y_DESCRIPTION,
        AREA_THREE_FIRST_VERTEX_X_DESCRIPTION,
        AREA_THREE_FIRST_VERTEX_Y_DESCRIPTION,
        AREA_THREE_SECOND_VERTEX_X_DESCRIPTION,
        AREA_THREE_SECOND_VERTEX_Y_DESCRIPTION,
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
        LD2450BLENumber(
            data.coordinator,
            data.device,
            entry.title,
            description,
        )
        for description in SENSOR_DESCRIPTIONS
    )


class LD2450BLENumber(CoordinatorEntity[LD2450BLECoordinator], NumberEntity, RestoreEntity):
    """Generic sensor for LD2450BLE."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: LD2450BLECoordinator,
        device: LD2450BLE,
        name: str,
        description: NumberEntityDescription,
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
        if self._key == "presence_timeout":
            self._attr_native_value = 5
        else:
            self._attr_native_value = 0

    async def async_added_to_hass(self) -> None:
        """Restore the timeout value after Home Assistant reloads."""
        await super().async_added_to_hass()
        if self._key == "presence_timeout":
            last_state = await self.async_get_last_state()
            if last_state is not None:
                try:
                    restored_value = float(last_state.state)
                    if self.entity_description.native_min_value <= restored_value <= self.entity_description.native_max_value:
                        self._attr_native_value = restored_value
                except (ValueError, TypeError):
                    _LOGGER.warning(
                        "Could not restore presence timeout from state %r",
                        last_state.state,
                    )
            self.async_write_ha_state()

    @property
    def unique_id(self):
        """Return unique id."""
        return self._attr_unique_id

    @property
    def entity_category(self):
        """Return the entity category of the switch."""
        if self._key == "presence_timeout":
            return EntityCategory.CONFIG
        return EntityCategory.CONFIG

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self._key == "presence_timeout":
            return
        self._attr_native_value = getattr(self._device, self._key)
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Unavailable if coordinator isn't connected."""
        if self._key == "presence_timeout":
            return True
        return self._coordinator.connected and super().available

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        if self._key == "presence_timeout":
            self._attr_native_value = int(value)
            self.async_write_ha_state()
            return
        await self._device._set_area(
            getattr(self._device, "area_mode"),
            int(value) if self._key == "area_one_first_vertex_x" else getattr(self._device, "area_one_first_vertex_x"),
            int(value) if self._key == "area_one_first_vertex_y" else getattr(self._device, "area_one_first_vertex_y"),
            int(value) if self._key == "area_one_second_vertex_x" else getattr(self._device, "area_one_second_vertex_x"),
            int(value) if self._key == "area_one_second_vertex_y" else getattr(self._device, "area_one_second_vertex_y"),
            int(value) if self._key == "area_two_first_vertex_x" else getattr(self._device, "area_two_first_vertex_x"),
            int(value) if self._key == "area_two_first_vertex_y" else getattr(self._device, "area_two_first_vertex_y"),
            int(value) if self._key == "area_two_second_vertex_x" else getattr(self._device, "area_two_second_vertex_x"),
            int(value) if self._key == "area_two_second_vertex_y" else getattr(self._device, "area_two_second_vertex_y"),
            int(value) if self._key == "area_three_first_vertex_x" else getattr(self._device, "area_three_first_vertex_x"),
            int(value) if self._key == "area_three_first_vertex_y" else getattr(self._device, "area_three_first_vertex_y"),
            int(value) if self._key == "area_three_second_vertex_x" else getattr(self._device, "area_three_second_vertex_x"),
            int(value) if self._key == "area_three_second_vertex_y" else getattr(self._device, "area_three_second_vertex_y"),
        )
