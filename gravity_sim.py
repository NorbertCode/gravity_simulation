import argparse
import json
import errors
import numpy as np
import data_serialization
from pathlib import Path
from simulation import Simulation
from simulation_visualizer import SimulationVisualizer
from center_object import CenterObject
from point_object import PointObject
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("k", type=int, help="the amount of simulation steps")
parser.add_argument("-r", "--resolution", type=int, nargs=2,
                    default=(512, 512), help="resolution of output in pixels")
parser.add_argument("-p", "--meters-per-pixel", type=int,
                    default=55000, help="meters per pixel")
parser.add_argument("-s", "--save", action="store_true",
                    help="save output as files")
parser.add_argument("-q", "--quiet", action="store_true",
                    help="don't show output")
parser.add_argument("--center-color", type=int, nargs=3,
                    default=[255, 255, 255], help="color of the center object")
parser.add_argument("--step-color", type=int, nargs=3,
                    default=[0, 255, 0], help="color of each step")
parser.add_argument("--point-color", type=int, nargs=3,
                    default=[255, 0, 0], help="color of end state for each point obj")
input_group = parser.add_mutually_exclusive_group(required=True)
input_group.add_argument("-f", "--file", type=str, nargs=1,
                         help="use the values from .json file")
input_group.add_argument("-i", "--interactive", action="store_true",
                         help="input values manually")
args = parser.parse_args()

sim_objs = None
if args.file is not None:
    with Path.open(args.file[0], "r") as file:
        sim_objs = data_serialization.read_state_from_json(json.load(file))
elif args.interactive:
    try:
        center_diameter = float(input("Center object's diameters in meters: "))
        center_mass = float(input("Center object's mass in kilograms: "))
    except ValueError as exc:
        raise errors.IncorrectCenterObjectValuesError from exc
    center_obj = CenterObject(center_diameter, center_mass)
    point_objs = []
    n = int(input("Amount of point objects: "))
    for i in range(n):
        try:
            point_pos_x = float(input(f"n={i} Point object's x position in meters: "))
            point_pos_y = float(input(f"n={i} Point object's y position in meters: "))

            point_mass = float(input(f"n={i} Point object's mass in kilograms: "))

            point_vel_x = float(input(f"n={i} Point object's x velocity in m/s: "))
            point_vel_y = float(input(f"n={i} Point object's y velocity in m/s: "))
        except ValueError as exc:
            raise errors.IncorrectPointObjectValuesError from exc

        point_pos = np.array([point_pos_x, point_pos_y])
        point_vel = np.array([point_vel_x, point_vel_y])

        point_objs.append(PointObject(point_pos, point_mass, point_vel))
    sim_objs = (center_obj, point_objs)

sim = Simulation(args.meters_per_pixel, sim_objs[0], sim_objs[1])
sim_vis = SimulationVisualizer(args.resolution, args.meters_per_pixel,
                               tuple(args.center_color), tuple(args.step_color),
                               tuple(args.point_color))
output = sim.run(args.k)
output_img = sim_vis.draw(sim.center_obj, sim.point_objs, output[0])
output_col = sim_vis.generate_collision_report(output[1])

if not args.quiet:
    print(output_col)
    output_img.show()

if args.save:
    file_name = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    data_serialization.save_state_as_json(f"{file_name}.json", sim.center_obj,
                                          sim.point_objs)
    output_img.save(f"{file_name}.png")
    with Path.open(f"{file_name}.txt", "w") as file:
        file.write(output_col)
