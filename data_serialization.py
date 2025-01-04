import json
from center_object import CenterObject
from point_object import PointObject


def read_state_from_json(data) -> tuple[CenterObject, list[PointObject]]:
    center_obj = CenterObject.from_json(data["center_object"])
    point_objs = [
        PointObject.from_json(obj)
        for obj in data["point_objects"]
    ]
    return (center_obj, point_objs)


def save_state_as_json(path: str, center_obj: CenterObject,
                       point_objs: list[PointObject]):
    data = {
        "center_object": center_obj.serialize(),
        "point_objects": [obj.serialize() for obj in point_objs]
    }
    with open(path, "w") as file:
        json.dump(data, file, indent=4)
