import numpy as np
from point_object import PointObject
from center_object import CenterObject
from collision import Collision
from copy import copy


class Simulation:
    def __init__(self, meters_per_pixel: float, center_obj: CenterObject,
                 point_objs: list[PointObject]):
        self._meters_per_pixel = meters_per_pixel

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

    def _simulate_step(self, point_obj: PointObject) -> np.array:
        """
        Run a single simulation step for a PointObject. Modifies the object's
        position and returns a copy of it.
        """
        accel_vector = self._calculate_acceleration(point_obj)

        point_obj.set_velocity(point_obj.velocity + (accel_vector * self._TIME_STEP))
        point_obj.update_position(self._TIME_STEP)

        # Return a copy, so it doesn't pass a reference and modify the current position
        return copy(point_obj.position)

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

    def run(self, steps: int) -> tuple[list[list[np.array]], list[Collision]]:
        """
        Runs the simulation for the given amount of steps.
        Returns a tuple, wherethe first element is a list of point objects' position
        per step (for example the position of the third object at the second step
        would be run()[0][1][2]) and the second is a list of collisions, which occured.
        """
        sim_steps = [[copy(obj.position) for obj in self._point_objs]]
        collisions = []
        blacklist = []  # List of indexes of objects, which have already collided
        for step in range(steps):
            # Position of (np.nan, np.nan) indicates an object has already collided
            # it's overridden if an object's index is not in blacklist
            positions = [np.array([np.nan, np.nan])] * len(self._point_objs)
            for index in range(len(self._point_objs)):
                if index not in blacklist:
                    pos = self._simulate_step(self._point_objs[index])
                    if self._check_for_center_obj_collision(pos):
                        collisions.append(Collision(step, [index]))
                        blacklist.append(index)
                    else:
                        positions[index] = pos

            indexes = self._check_for_collisions(positions)
            if len(indexes) > 0:
                collisions.append(Collision(step, indexes))
            blacklist.extend(indexes)

            sim_steps.append(positions)
        return sim_steps, collisions
