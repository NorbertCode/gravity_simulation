import argparse
import errors
import numpy as np
from pathlib import Path
from config_data import ConfigData
from simulation import Simulation
from simulation_visualizer import SimulationVisualizer
from center_object import CenterObject
from point_object import PointObject
from datetime import datetime


def input_objects() -> ConfigData:
    steps = 0
    resolution = []
    meters_per_pixel = 0.0
    while True:
        try:
            steps = int(input("Amount of steps (k): "))
            resolution = int(input("X resolution: ")), int(input("Y resolution: "))
            meters_per_pixel = float(input("Meters per pixel: "))
            break
        except ValueError:
            print("This value must be a number.")
    center_obj = None
    while True:
        try:
            center_diameter = float(input("Center object's diameters in meters: "))
            center_mass = float(input("Center object's mass in kilograms: "))
            center_obj = CenterObject(center_diameter, center_mass)
            break
        except (errors.NegativeDiameterError, errors.NegativeMassError) as exc:
            print(exc)
        except ValueError:
            print("This value must be a number.")

    point_objs = []
    n = int(input("Amount of point objects (n): "))
    for i in range(n):
        while True:
            try:
                point_pos_x = float(input(f"X position of n={i} in meters: "))
                point_pos_y = float(input(f"Y position of n={i} in meters: "))

                point_vel_x = float(input(f"X velocity of n={i} in m/s: "))
                point_vel_y = float(input(f"Y velocity of n={i} in m/s: "))

                point_mass = float(input(f"Mass of n={i} in kilograms: "))

                point_pos = np.array([point_pos_x, point_pos_y])
                point_vel = np.array([point_vel_x, point_vel_y])

                point_objs.append(PointObject(point_pos, point_mass, point_vel))
                break
            except errors.NegativeMassError as exc:
                print(exc)
            except ValueError:
                print("This value must be a number.")
    return ConfigData(steps, resolution, meters_per_pixel, center_obj, point_objs)


def load_config_data(args) -> ConfigData:
    config_data = None
    if args.file is not None:
        try:
            config_data = ConfigData.from_json(args.file[0])
        except (errors.NegativeMassError, errors.NegativeDiameterError,
                errors.UnableToOpenConfigError, errors.InvalidStepsError,
                errors.InvalidResolutionError, errors.InvalidMetersPerPixelError,
                errors.InvalidCenterObjectDataError,
                errors.InvalidPointObjectDataError) as exc:
            print(exc)
            exit()
    else:
        user_input = input_objects()
        config_data = ConfigData(user_input.steps, user_input.resolution,
                                       user_input.meters_per_pixel,
                                       user_input.center_obj, user_input.point_objs)
    return config_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--save", action="store_true",
                        help="save output as files")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="don't show output")
    parser.add_argument("--center-color", type=int, nargs=3,
                        default=[255, 255, 255], help="color of the center object")
    parser.add_argument("--step-color", type=int, nargs=3,
                        default=[0, 255, 0], help="color of each step")
    parser.add_argument("--point-color", type=int, nargs=3,
                        default=[255, 0, 0], help="color of end states of point objs")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-f", "--file", type=str, nargs=1,
                             help="use the values from .json file")
    input_group.add_argument("-i", "--interactive", action="store_true",
                             help="input values manually")
    args = parser.parse_args()

    start_config_data = load_config_data(args)
    sim_objs = start_config_data.get_simulation_objects()
    sim = Simulation(start_config_data.meters_per_pixel, sim_objs[0], sim_objs[1])
    sim_vis = SimulationVisualizer(start_config_data.resolution,
                                   start_config_data.meters_per_pixel,
                                   tuple(args.center_color), tuple(args.step_color),
                                   tuple(args.point_color))
    output = sim.run(start_config_data.steps)
    output_img = sim_vis.draw(sim.center_obj, sim.point_objs, output[0])
    output_col = sim_vis.generate_report(output[1], output[0], sim.point_objs)

    if not args.quiet:
        print(output_col)
        output_img.show()

    if args.save:
        file_name = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        try:
            end_config_data = ConfigData(start_config_data.steps,
                                         start_config_data.resolution,
                                         start_config_data.meters_per_pixel,
                                         sim.center_obj, sim.point_objs)
            end_config_data.save_data_to_json(f"{file_name}.json")
            output_img.save(f"{file_name}.png")
            with Path.open(f"{file_name}.txt", "w") as file:
                file.write(output_col)
        except PermissionError as exc:
            print(exc)
            exit()


if __name__ == "__main__":
    main()
