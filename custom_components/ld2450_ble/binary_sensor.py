"""LD2450 BLE integration sensor platform."""

import logging
import time

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_call_later
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import LD2450BLE, LD2450BLECoordinator
from .const import DOMAIN
from .models import LD2450BLEData

_LOGGER = logging.getLogger(__name__)

DEFAULT_PRESENCE_TIMEOUT = 5.0
CONF_PRESENCE_TIMEOUT = "presence_timeout"


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

ZONE_ONE_PRESENCE = BinarySensorEntityDescription(
    key="zone_one_presence",
    translation_key="zone_one_presence",
    name="Zone 1 Presence",
    device_class=BinarySensorDeviceClass.OCCUPANCY,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
)
ZONE_TWO_PRESENCE = BinarySensorEntityDescription(
    key="zone_two_presence",
    translation_key="zone_two_presence",
    name="Zone 2 Presence",
    device_class=BinarySensorDeviceClass.OCCUPANCY,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
)
ZONE_THREE_PRESENCE = BinarySensorEntityDescription(
    key="zone_three_presence",
    translation_key="zone_three_presence",
    name="Zone 3 Presence",
    device_class=BinarySensorDeviceClass.OCCUPANCY,
    entity_registry_enabled_default=True,
    entity_registry_visible_default=True,
)

PRESENCE_SENSORS = {
    "any_presence",
    "zone_one_presence",
    "zone_two_presence",
    "zone_three_presence",
}

# Shared timeout storage
_PRESENCE_TIMEOUT = {}  # key: entry_id, value: timeout in seconds

SENSOR_DESCRIPTIONS = (
    [
        ANY_PRESENCE,
        ONE_TARGET,
        TWO_TARGET,
        THREE_TARGET,
        ONE_MOVING,
        TWO_MOVING,
        THREE_MOVING,
        ZONE_ONE_PRESENCE,
        ZONE_TWO_PRESENCE,
        ZONE_THREE_PRESENCE,
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
            entry.entry_id,
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
        config_entry_id: str,
        description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._device = device
        self._config_entry_id = config_entry_id
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
        self._last_presence_time = time.monotonic()
        self._clear_timer = None
        self._pending_off = False

    @property
    def unique_id(self):
        """Return unique id."""
        return self._attr_unique_id

    def _target_in_zone(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        """Check if any target is inside the given zone rectangle."""
        zx1, zx2 = min(x1, x2), max(x1, x2)
        zy1, zy2 = min(y1, y2), max(y1, y2)
        # Check all three targets
        for target_num in ("one", "two", "three"):
            tx = getattr(self._device, f"target_{target_num}_x", 0)
            ty = getattr(self._device, f"target_{target_num}_y", 0)
            if tx == 0 and ty == 0:
                continue  # no target present
            if tx >= zx1 and tx <= zx2 and ty >= zy1 and ty <= zy2:
                return True
        return False

    def _get_presence_timeout(self) -> float:
        """Get presence clear timeout from this integration config entry."""
        try:
            entity_registry = er.async_get(self.hass)

            # Config-entry association is reliable even if entity/device names
            # are customized and avoids assuming a Bluetooth identifier is unique.
            entries = er.async_entries_for_config_entry(
                entity_registry, self._config_entry_id
            )
            for entry in entries:
                if entry.domain != "number" or not entry.unique_id.endswith(
                    f"_{CONF_PRESENCE_TIMEOUT}"
                ):
                    continue

                state = self.hass.states.get(entry.entity_id)
                if state is None or state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
                    _LOGGER.debug(
                        "%s: timeout entity %s has no usable state",
                        self._device.name, entry.entity_id,
                    )
                    continue

                try:
                    timeout = float(state.state)
                    _LOGGER.debug(
                        "%s: using presence timeout %.1fs from %s",
                        self._device.name, timeout, entry.entity_id,
                    )
                    return timeout
                except (ValueError, TypeError):
                    _LOGGER.warning(
                        "%s: invalid timeout value %r in %s",
                        self._device.name, state.state, entry.entity_id,
                    )

            _LOGGER.warning(
                "%s: no presence_timeout number found for config entry %s; "
                "using default %.1fs",
                self._device.name, self._config_entry_id, DEFAULT_PRESENCE_TIMEOUT,
            )
        except Exception:
            _LOGGER.exception(
                "%s: error looking up presence timeout; using default %.1fs",
                self._device.name, DEFAULT_PRESENCE_TIMEOUT,
            )

        return DEFAULT_PRESENCE_TIMEOUT

    def _cancel_timer(self):
        """Cancel pending clear timer."""
        if self._clear_timer:
            self._clear_timer()
            self._clear_timer = None
        self._pending_off = False

    def _schedule_clear(self):
        """Schedule clearing presence after timeout."""
        timeout = self._get_presence_timeout()
        if timeout <= 0:
            self._set_off()
            return
        self._cancel_timer()
        self._pending_off = True
        self._clear_timer = async_call_later(self.hass, timeout, self._async_clear_timeout)

    @callback
    def _async_clear_timeout(self, _now):
        """Clear presence after timeout expired."""
        self._clear_timer = None
        self._pending_off = False
        self._attr_native_value = False
        self.async_write_ha_state()

    def _set_off(self):
        """Set presence to off immediately."""
        self._cancel_timer()
        if self._attr_native_value:
            self._attr_native_value = False
            self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        raw_presence = False

        match self._key:
            case "any_presence":
                raw_presence = bool(getattr(self._device, "target_one_y") > 0)
            case "one_target":
                raw_presence = bool(getattr(self._device, "target_one_y") > 0 and getattr(self._device, "target_two_y") == 0)
            case "two_target":
                raw_presence = bool(getattr(self._device, "target_two_y") > 0 and getattr(self._device, "target_three_y") == 0)
            case "three_target":
                raw_presence = bool(getattr(self._device, "target_three_y") > 0)
            case "one_moving":
                raw_presence = bool(getattr(self._device, "target_one_speed") > 0)
            case "two_moving":
                raw_presence = bool(getattr(self._device, "target_two_speed") > 0)
            case "three_moving":
                raw_presence = bool(getattr(self._device, "target_three_speed") > 0)
            case "zone_one_presence":
                raw_presence = self._target_in_zone(
                    getattr(self._device, "area_one_first_vertex_x", 0),
                    getattr(self._device, "area_one_first_vertex_y", 0),
                    getattr(self._device, "area_one_second_vertex_x", 0),
                    getattr(self._device, "area_one_second_vertex_y", 0),
                )
            case "zone_two_presence":
                raw_presence = self._target_in_zone(
                    getattr(self._device, "area_two_first_vertex_x", 0),
                    getattr(self._device, "area_two_first_vertex_y", 0),
                    getattr(self._device, "area_two_second_vertex_x", 0),
                    getattr(self._device, "area_two_second_vertex_y", 0),
                )
            case "zone_three_presence":
                raw_presence = self._target_in_zone(
                    getattr(self._device, "area_three_first_vertex_x", 0),
                    getattr(self._device, "area_three_first_vertex_y", 0),
                    getattr(self._device, "area_three_second_vertex_x", 0),
                    getattr(self._device, "area_three_second_vertex_y", 0),
                )
            case _:
                _LOGGER.error("Wrong KEY for binary sensor: %s", self._key)
                self.async_write_ha_state()
                return

        if self._key in PRESENCE_SENSORS:
            if raw_presence:
                self._last_presence_time = time.monotonic()
                self._cancel_timer()
                if not self._attr_native_value:
                    self._attr_native_value = True
                    self.async_write_ha_state()
                else:
                    self.async_write_ha_state()
            else:
                if self._attr_native_value and not self._pending_off:
                    self._schedule_clear()
                    self.async_write_ha_state()
                elif self._attr_native_value and self._pending_off:
                    self.async_write_ha_state()
                else:
                    self.async_write_ha_state()
        else:
            if raw_presence != self._attr_native_value:
                self._attr_native_value = raw_presence
            self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Unavailable if coordinator isn't connected."""
        return self._coordinator.connected and super().available

    @property
    def is_on(self):
        """Return if sensor is on."""
        return bool(self._attr_native_value)
