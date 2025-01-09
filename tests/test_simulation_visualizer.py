import numpy as np
from simulation_visualizer import SimulationVisualizer
from center_object import CenterObject
from point_object import PointObject
from collision import Collision


def test_simulation_visualizer_draw():
    sim_vis = SimulationVisualizer([101, 101], 1.0)
    center_obj = CenterObject(50.0)
    sim_steps = [[np.array([48.0, 48.0])]]
    point_obj = PointObject(np.array([50.0, 50.0]))
    output = sim_vis.draw(center_obj, [point_obj], sim_steps)
    pixel_center = (round(output.size[0] / 2), round(output.size[1] / 2))
    assert output.size == (101, 101)
    assert output.getpixel(pixel_center) == (255, 255, 255)
    assert output.getpixel((98, 2)) == (0, 255, 0)
    assert output.getpixel((100, 0)) == (255, 0, 0)


def test_simulation_visualiser_draw_custom_colors():
    sim_vis = SimulationVisualizer([101, 101], 1.0, (128, 128, 128), (1, 2, 3),
                                   (255, 255, 255))
    center_obj = CenterObject(50.0)
    sim_steps = [[np.array([48.0, 48.0])]]
    point_obj = PointObject(np.array([50.0, 50.0]))
    output = sim_vis.draw(center_obj, [point_obj], sim_steps)
    pixel_center = (round(output.size[0] / 2), round(output.size[1] / 2))
    assert output.size == (101, 101)
    assert output.getpixel(pixel_center) == (128, 128, 128)
    assert output.getpixel((98, 2)) == (1, 2, 3)
    assert output.getpixel((100, 0)) == (255, 255, 255)


def test_simulation_visualiser_draw_overloaded_colors():
    sim_vis = SimulationVisualizer([101, 101], 1.0, (300, 300, 300))
    center_obj = CenterObject(50.0)
    output = sim_vis.draw(center_obj, [], [])
    pixel_center = (round(output.size[0] / 2), round(output.size[1] / 2))
    assert output.getpixel(pixel_center) == (255, 255, 255)


def test_simulation_visualiser_draw_negative_colors():
    sim_vis = SimulationVisualizer([101, 101], 1.0, (-1, -1, -1))
    center_obj = CenterObject(50.0)
    output = sim_vis.draw(center_obj, [], [])
    pixel_center = (round(output.size[0] / 2), round(output.size[1] / 2))
    assert output.getpixel(pixel_center) == (0, 0, 0)


def test_simulation_visualiser_generate_report_no_collisions():
    collision_data = []
    sim_steps = [[np.array([48.0, 48.0])]]
    point_objs = [PointObject(np.array([50.0, 50.0]))]
    report = SimulationVisualizer.generate_report(collision_data, sim_steps, point_objs)
    expected_report = ("Objects:\nn=0, start position = (48.0, 48.0), " +
                       "end position = (50.0, 50.0)\n\nCollisions:\n")
    assert report == expected_report


def test_simulation_visualiser_generate_report_collisions():
    collision_data = [Collision(1, [1, 2]), Collision(2, [3])]
    sim_steps = [[np.array([48.0, 48.0])]]
    point_objs = [PointObject(np.array([50.0, 50.0]))]
    report = SimulationVisualizer.generate_report(collision_data, sim_steps, point_objs)
    expected_report = ("Objects:\nn=0, start position = (48.0, 48.0), " +
                       "end position = (50.0, 50.0)\n\nCollisions:\nn=1, " +
                       "n=2 at k=1\nn=3 at k=2\n")
    assert report == expected_report
