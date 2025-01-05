from dataclasses import dataclass


@dataclass
class Collision:
    step: int
    point_obj_indexes: list[int]
