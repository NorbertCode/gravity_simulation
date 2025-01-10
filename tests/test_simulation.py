import numpy as np
from center_object import CenterObject
from point_object import PointObject
from simulation import Simulation


def test_simulation_calculate_acceleration():
    center_obj = CenterObject(1.0, 1.0e20)
    point_obj = PointObject(np.array([5000.0, 0.0]), 1.0e3, np.array([0.0, 0.0]))
    simulation = Simulation(1.0, center_obj, [point_obj])
    np.testing.assert_almost_equal(simulation._calculate_acceleration(point_obj),
                                   np.array([-266.952, 0.0]), 1)


def test_simulation_calculate_acceleration_diagonal():
    center_obj = CenterObject(1, 1e20)
    point_obj = PointObject(np.array([5000, 5000]), 1e3, np.array([0, 0]))
    simulation = Simulation(1, center_obj, [point_obj])
    np.testing.assert_almost_equal(simulation._calculate_acceleration(point_obj),
                                   np.array([-94.38885579, -94.38885579]), 1)


def test_simulation_calculate_next():
    center_obj = CenterObject(1.0, 1.0e20)
    point_obj = PointObject(np.array([5000.0, 0.0]), 1.0e3, np.array([0.0, 0.0]))
    simulation = Simulation(1.0, center_obj, [point_obj])
    next_position = simulation._simulate_step(point_obj)
    np.testing.assert_almost_equal(next_position, np.array([5000 - 266.952, 0]), 1)


def test_simulation_calculate_next_diagonal():
    center_obj = CenterObject(1.0, 1.0e20)
    point_obj = PointObject(np.array([5000.0, 5000.0]), 1.0e3, np.array([0.0, 0.0]))
    simulation = Simulation(1.0, center_obj, [point_obj])
    next_position = simulation._simulate_step(point_obj)
    np.testing.assert_almost_equal(next_position, np.array([5000 - 94.38885579,
                                                            5000 - 94.38885579]), 1)


def test_simulation_calculate_next_already_moving():
    center_obj = CenterObject(1.0, 1.0e20)
    point_obj = PointObject(np.array([5000.0, 0.0]), 1.0e3, np.array([100.0, 0.0]))
    simulation = Simulation(1.0, center_obj, [point_obj])
    next_position = simulation._simulate_step(point_obj)
    np.testing.assert_almost_equal(next_position,
                                   np.array([5000 + 100 - 266.952, 0]), 1)


def test_simulation_check_for_center_obj_collision():
    center_obj = CenterObject(1000.0, 1.0)
    inner_point_obj = PointObject(np.array([500.0, 0.0]), 1.0e3, np.array([0.0, 0.0]))
    outer_point_obj = PointObject(np.array([1500.0, 0.0]), 1.0e3, np.array([0.0, 0.0]))
    simulation = Simulation(1.0, center_obj, [inner_point_obj])
    assert simulation._check_for_center_obj_collision(inner_point_obj.position)
    assert not simulation._check_for_center_obj_collision(outer_point_obj.position)


def test_simulation_check_for_collisions():
    simulation = Simulation(32.0, CenterObject(), [PointObject()])
    positions = [np.array([0.0, 0.0]), np.array([10.0, 10.0]),
                 np.array([128.0, 10.0]), np.array([130.0, 15.0]),
                 np.array([256.0, 256.0])]
    assert simulation._check_for_collisions(positions) == [0, 1, 2, 3]


def test_simulation_check_for_collisions_with_nan():
    simulation = Simulation(32.0, CenterObject(), [PointObject()])
    positions = [np.array([0.0, 0.0]), np.array([10.0, 10.0]),
                 np.array([np.nan, np.nan]), np.array([np.nan, np.nan]),
                 np.array([256.0, 256.0])]
    assert simulation._check_for_collisions(positions) == [0, 1]


def test_simulation_run():
    simulation = Simulation(1.0, CenterObject(10.0, 1e12),
                            [PointObject(np.array([0.0, 20.0]))])
    sim_steps, collisions = simulation.run(20)
    assert len(sim_steps) == 21
    np.testing.assert_array_equal(sim_steps[0][0], np.array([0.0, 20.0]))
    np.testing.assert_array_equal(sim_steps[-1][0], np.array([np.nan, np.nan]))
    assert len(collisions) == 1
    assert collisions[0].point_obj_indexes == [0]
    assert collisions[0].step == 11
