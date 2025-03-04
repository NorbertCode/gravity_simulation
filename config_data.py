import json
import errors
from pathlib import Path
from center_object import CenterObject
from point_object import PointObject


class ConfigData:
    def __init__(self, steps: int, resolution: list[int], meters_per_pixel: float,
                 close_call_distance: float, center_obj: CenterObject,
                 point_objs: list[PointObject]):
        self._steps = steps
        self._resolution = resolution
        self._meters_per_pixel = meters_per_pixel
        self._close_call_distance = close_call_distance
        self._center_obj = center_obj
        self._point_objs = point_objs

    @property
    def steps(self) -> int:
        return self._steps

    @property
    def resolution(self) -> list[int]:
        return self._resolution

    @property
    def meters_per_pixel(self) -> float:
        return self._meters_per_pixel

    @property
    def close_call_distance(self) -> float:
        return self._close_call_distance

    @property
    def center_obj(self) -> CenterObject:
        return self._center_obj

    @property
    def point_objs(self) -> list[PointObject]:
        return self._point_objs

    def get_simulation_objects(self) -> tuple[CenterObject, list[PointObject]]:
        return self._center_obj, self._point_objs

    @classmethod
    def from_json(cls, path: Path):
        """Create an object from the given json data"""
        try:
            with path.open("r") as file:
                data = json.load(file)

                steps = data["steps"]
                resolution = data["resolution"]
                meters_per_pixel = data["meters_per_pixel"]
                close_call_distance = data["close_call_distance"]

                if type(steps) is not int or steps < 0:
                    raise errors.InvalidStepsError
                if (len(resolution) != 2
                    or type(resolution[0]) is not int
                    or type(resolution[1]) is not int
                    or resolution[0] <= 0
                    or resolution[1] <= 0):
                    raise errors.InvalidResolutionError
                if (not isinstance(meters_per_pixel, (int, float))
                    or meters_per_pixel <= 0):
                    raise errors.InvalidMetersPerPixelError
                if (not isinstance(close_call_distance, (int, float))
                    or close_call_distance <= 0):
                    raise errors.InvalidCloseCallDistanceError

                center_obj = CenterObject.from_json(data["center_object"])
                point_objs = [PointObject.from_json(obj)
                              for obj in data["point_objects"]]

                return cls(steps, resolution, meters_per_pixel, close_call_distance,
                           center_obj, point_objs)
        except (FileNotFoundError, PermissionError, json.JSONDecodeError) as exc:
            raise errors.UnableToOpenConfigError from exc

    def save_data_to_json(self, path: Path):
        """Save this object's data to a json file"""
        data = {
            "steps": self._steps,
            "resolution": self._resolution,
            "meters_per_pixel": self._meters_per_pixel,
            "close_call_distance": self._close_call_distance,
            "center_object": self._center_obj.serialize(),
            "point_objects": [obj.serialize() for obj in self._point_objs]
        }
        with path.open("w") as file:
            json.dump(data, file, indent=4)
