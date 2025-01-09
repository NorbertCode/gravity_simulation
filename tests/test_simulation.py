import numpy as np
from center_object import CenterObject
from point_object import PointObject
from simulation import Simulation


def test_simulation_calculate_acceleration():
    center_obj = CenterObject(1.0, 1.0e20)
    point_obj = PointObject(np.array([5000.0, 0.0]), 1.0e3, np.array([0.0, 0.0]))
    simulation = Simulation(1.0, center_obj, [point_obj])
    np.testing.assert_almost_equal(simulation.calculate_acceleration(point_obj),
                                   np.array([-266.952, 0.0]), 1)


def test_simulation_calculate_acceleration_diagonal():
    center_obj = CenterObject(1, 1e20)
    point_obj = PointObject(np.array([5000, 5000]), 1e3, np.array([0, 0]))
    simulation = Simulation(1, center_obj, [point_obj])
    np.testing.assert_almost_equal(simulation.calculate_acceleration(point_obj),
                                   np.array([-94.38885579, -94.38885579]), 1)


def test_simulation_calculate_next():
    center_obj = CenterObject(1.0, 1.0e20)
    point_obj = PointObject(np.array([5000.0, 0.0]), 1.0e3, np.array([0.0, 0.0]))
    simulation = Simulation(1.0, center_obj, [point_obj])
    next_position = simulation.calculate_next(point_obj)
    np.testing.assert_almost_equal(next_position, np.array([5000 - 266.952, 0]), 1)


def test_simulation_calculate_next_diagonal():
    center_obj = CenterObject(1.0, 1.0e20)
    point_obj = PointObject(np.array([5000.0, 5000.0]), 1.0e3, np.array([0.0, 0.0]))
    simulation = Simulation(1.0, center_obj, [point_obj])
    next_position = simulation.calculate_next(point_obj)
    np.testing.assert_almost_equal(next_position, np.array([5000 - 94.38885579,
                                                            5000 - 94.38885579]), 1)


def test_simulation_calculate_next_already_moving():
    center_obj = CenterObject(1.0, 1.0e20)
    point_obj = PointObject(np.array([5000.0, 0.0]), 1.0e3, np.array([100.0, 0.0]))
    simulation = Simulation(1.0, center_obj, [point_obj])
    next_position = simulation.calculate_next(point_obj)
    np.testing.assert_almost_equal(next_position,
                                   np.array([5000 + 100 - 266.952, 0]), 1)


def test_simulation_check_for_center_obj_collision():
    center_obj = CenterObject(1000.0, 1.0)
    inner_point_obj = PointObject(np.array([500.0, 0.0]), 1.0e3, np.array([0.0, 0.0]))
    outer_point_obj = PointObject(np.array([1500.0, 0.0]), 1.0e3, np.array([0.0, 0.0]))
    simulation = Simulation(1.0, center_obj, [inner_point_obj])
    assert simulation.check_for_center_obj_collision(inner_point_obj.position)
    assert not simulation.check_for_center_obj_collision(outer_point_obj.position)


def test_simulation_check_for_collisions():
    simulation = Simulation(32.0, CenterObject(), [PointObject()])
    positions = [np.array([0.0, 0.0]), np.array([10.0, 10.0]),
                 np.array([128.0, 10.0]), np.array([130.0, 15.0]),
                 np.array([256.0, 256.0])]
    assert simulation.check_for_collisions(positions) == [0, 1, 2, 3]


def test_simulation_check_for_collisions_with_nan():
    simulation = Simulation(32.0, CenterObject(), [PointObject()])
    positions = [np.array([0.0, 0.0]), np.array([10.0, 10.0]),
                 np.array([np.nan, np.nan]), np.array([np.nan, np.nan]),
                 np.array([256.0, 256.0])]
    assert simulation.check_for_collisions(positions) == [0, 1]
