from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class LD2450BLEState:

    target_one_x: int = 0
    target_one_y: int = 0
    target_one_speed: int = 0
    target_one_resolution: int = 0
    
    target_two_x: int = 0
    target_two_y: int = 0
    target_two_speed: int = 0
    target_two_resolution: int = 0

    target_three_x: int = 0
    target_three_y: int = 0
    target_three_speed: int = 0
    target_three_resolution: int = 0

@dataclass(frozen=True)
class LD2450BLEConfig:
    
    target_mode: int = 0
    
    fw_ver: str = ""
    
    mac_addr: str = ""
    
    area_mode: int = 0
    area_one_first_vertex_x: int = 0
    area_one_first_vertex_y: int = 0
    area_one_second_vertex_x: int = 0
    area_one_second_vertex_y: int = 0
    area_two_first_vertex_x: int = 0
    area_two_first_vertex_y: int = 0
    area_two_second_vertex_x: int = 0
    area_two_second_vertex_y: int = 0
    area_three_first_vertex_x: int = 0
    area_three_first_vertex_y: int = 0
    area_three_second_vertex_x: int = 0
    area_three_second_vertex_y: int = 0