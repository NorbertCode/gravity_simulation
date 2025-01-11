import numpy as np
from point_object import PointObject
from center_object import CenterObject
from space_event import SpaceEvent
from simulation_output import SimulationOutput
from copy import copy


class Simulation:
    def __init__(self, meters_per_pixel: float, close_call_distance: float,
                 center_obj: CenterObject, point_objs: list[PointObject]):
        self._meters_per_pixel = meters_per_pixel
        self._close_call_distance = close_call_distance

        self._center_obj = center_obj
        self._point_objs = point_objs

        self._G_CONST = 6.67430e-11
        self._TIME_STEP = 1.0

    @property
    def center_obj(self) -> CenterObject:
        return self._center_obj

    @property
    def point_objs(self) -> list[PointObject]:
        return self._point_objs

    def _calculate_acceleration(self, point_obj: PointObject) -> np.array:
        """Calculate the acceleration vector (m/s) based on the current values"""
        dist_vector = self._center_obj.position - point_obj.position
        dist = np.linalg.norm(dist_vector)
        dist_norm = dist_vector / dist

        force = (self._center_obj.mass * point_obj.mass * self._G_CONST) / (dist**2)
        force_vector = force * dist_norm
        accel_vector = force_vector / point_obj.mass

        return accel_vector

    def _calculate_next(self, point_obj: PointObject) -> np.array:
        """
        Runs a single simulation step for a PointObject. Doesn't modify
        the point object. Returns the new position.
        """
        accel_vector = self._calculate_acceleration(point_obj)

        point_obj.set_velocity(point_obj.velocity + (accel_vector * self._TIME_STEP))
        new_position = point_obj.position + (point_obj.velocity * self._TIME_STEP)

        return new_position

    def _check_for_center_obj_collision(self, position: np.array) -> bool:
        """
        Returns true if the point object on the given position is colliding
        with the center object - if the distance between them is smaller than the
        center object's radius.
        """
        dist_to_center = np.linalg.norm(self._center_obj.position - position)
        return dist_to_center <= self._center_obj.diameter / 2

    def _check_for_collisions(self, positions: list[np.array]) -> list[int]:
        """
        Gets a list of positions of point objects and returns indexes of ones,
        which are currently colliding.
        Since a collision is defined as two objects on the same pixel this
        converts the space positions to positions in pixel space and
        checks for duplicates.
        """
        pixel_positions = []
        for pos in positions:
            # np.nan is used to mark a point object as already having collided before,
            # so there is no need to run any calculations for it.
            if pos is not np.nan:
                pixel_positions.append((pos / self._meters_per_pixel).round())
            else:
                pixel_positions.append(np.array([np.nan, np.nan]))

        _, inverse, count = np.unique(pixel_positions, return_inverse=True,
                                      return_counts=True, axis=0)
        duplicate_indexes = np.where(count[inverse] > 1)[0]
        return duplicate_indexes.tolist()

    def _check_for_close_calls(self, point_obj: PointObject) -> list[int]:
        """
        Returns a list of indexes of point objects, which are within close call distance
        """
        close_call_indexes = []
        for index, obj in enumerate(self._point_objs):
            dist = np.linalg.norm(obj.position - point_obj.position)
            if dist <= self._close_call_distance and obj != point_obj:
                close_call_indexes.append(index)
        return close_call_indexes

    def run(self, steps: int) -> SimulationOutput:
        """
        Runs the simulation for the given amount of steps.
        Returns a tuple, where the first element is a list of point objects' position
        per step (for example the position of the third object at the second step
        would be run()[0][1][2]) and the second is a list of collisions, which occured.
        """
        sim_steps = [[copy(obj.position) for obj in self._point_objs]]
        collisions = []
        close_calls = []
        blacklist = []  # List of indexes of objects, which have already collided
        for step in range(steps):
            indexes = self._check_for_collisions(sim_steps[-1])
            if len(indexes) > 0:
                collisions.append(SpaceEvent(step, indexes))
            blacklist.extend(indexes)

            # Position of (np.nan, np.nan) indicates an object has already collided
            # It's overridden with the next position if an object's index is
            # not in the blacklist
            positions = [np.array([np.nan, np.nan])] * len(self._point_objs)
            for index in range(len(self._point_objs)):
                if index not in blacklist:
                    cc_for_obj = self._check_for_close_calls(self._point_objs[index])
                    if len(cc_for_obj) > 0:
                        cc_for_obj.append(index)
                        cc_for_obj.sort()
                        cc_event = SpaceEvent(step, sorted(cc_for_obj))
                        if cc_event not in close_calls:
                            close_calls.append(cc_event)
                    pos = self._calculate_next(self._point_objs[index])
                    if self._check_for_center_obj_collision(pos):
                        collisions.append(SpaceEvent(step, [index]))
                        blacklist.append(index)
                    else:
                        positions[index] = pos
                        self._point_objs[index].set_position(pos)

            sim_steps.append(positions)
        return SimulationOutput(sim_steps, collisions, close_calls)
