from dataclasses import dataclass


@dataclass
class SpaceEvent:
    step: int
    point_obj_indexes: list[int]
