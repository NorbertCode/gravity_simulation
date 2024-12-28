import argparse
import json
import simulation
import numpy as np
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
input_group = parser.add_mutually_exclusive_group(required=True)
input_group.add_argument("-f", "--file", type=str, nargs=1,
                         help="use the values from .json file")
input_group.add_argument("-i", "--interactive", action="store_true",
                         help="input values manually")
args = parser.parse_args()

sim = simulation.Simulation(args.resolution, args.meters_per_pixel)
if args.file:
    with open(args.file[0], "r") as file:
        sim.init_from_json(json.load(file))
elif args.interactive:
    center_diameter = float(input("Center object's diameters in meters: "))
    center_mass = float(input("Center object's mass in kilograms: "))
    center_obj = CenterObject(center_diameter, center_mass)
    point_objs = []
    n = int(input("Amount of point objects: "))
    for i in range(n):
        point_pos_x = float(input(f"{i} Point object's x position in meters: "))
        point_pos_y = float(input(f"{i} Point object's y position in meters: "))
        point_pos = np.array([point_pos_x, point_pos_y])

        point_mass = float(input(f"{i} Point object's mass in kilograms: "))

        point_vel_x = float(input(f"{i} Point object's x velocity in m/s: "))
        point_vel_y = float(input(f"{i} Point object's y velocity in m/s: "))
        point_vel = np.array([point_vel_x, point_vel_y])

        point_objs.append(PointObject(point_pos, point_mass, point_vel))
    sim.init_objects(center_obj, point_objs)

output = sim.run(args.k)

file_name = None
if args.save:
    file_name = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
print(sim.generate_collision_report(output[1], file_name))
sim.draw(output[0], file_name)
