"""The ld2450 ble integration models."""

from __future__ import annotations

from dataclasses import dataclass

from .ld2450_ble import LD2450BLE

from .coordinator import LD2450BLECoordinator


@dataclass
class LD2450BLEData:
    """Data for the ld2450 ble integration."""

    title: str
    device: LD2450BLE
    coordinator: LD2450BLECoordinator
