import argparse
import sys
import errors
import numpy as np
from pathlib import Path
from config_data import ConfigData
from simulation import Simulation
from simulation_visualizer import SimulationVisualizer
from center_object import CenterObject
from point_object import PointObject
from datetime import datetime


class CommandLineInterface:
    def __init__(self, args: list[str]):
        """Initialize the program by parsing arguments and running the simulation"""
        self._args = self._parse_args(args)

        # Initialize and run simulation and visualization
        self._start_config_data = self._load_config(self._args)
        sim_objs = self._start_config_data.get_simulation_objects()

        self._sim = Simulation(self._start_config_data.meters_per_pixel,
                               self._start_config_data.close_call_distance,
                               sim_objs[0], sim_objs[1])
        self._output = self._sim.run(self._start_config_data.steps)

        sim_vis = SimulationVisualizer(self._start_config_data.resolution,
                                       self._start_config_data.meters_per_pixel,
                                       tuple(self._args.center_color),
                                       tuple(self._args.step_color),
                                       tuple(self._args.point_color))
        self._output_img = sim_vis.draw(self._sim.center_obj, self._sim.point_objs,
                                        self._output.simulation_steps)
        self._output_col = sim_vis.generate_report(self._output, self._sim.point_objs)

    @staticmethod
    def _parse_args(args: list[str]) -> argparse.Namespace:
        """Parse command line arguments"""
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
                            default=[255, 0, 0],
                            help="color of end states of point objs")
        input_group = parser.add_mutually_exclusive_group(required=True)
        input_group.add_argument("-f", "--file", type=str, nargs=1,
                                help="use the values from .json file")
        input_group.add_argument("-i", "--interactive", action="store_true",
                                help="input values manually")
        return parser.parse_args(args)

    @staticmethod
    def _load_config_from_input() -> ConfigData:
        """Get configuration data from user interactive input"""
        # General output configuration - steps, resolution, meters per pixel
        steps = 0
        resolution = []
        meters_per_pixel = 0.0
        close_call_distance = 0.0
        while True:
            try:
                steps = int(input("Amount of steps (k): "))
                if steps < 0:
                    raise errors.InvalidStepsError
                resolution = int(input("X resolution: ")), int(input("Y resolution: "))
                if resolution[0] <= 0 or resolution[1] <= 0:
                    raise errors.InvalidResolutionError
                meters_per_pixel = float(input("Meters per pixel: "))
                if meters_per_pixel <= 0:
                    raise errors.InvalidMetersPerPixelError
                close_call_distance = float(input("Close call distance in meters: "))
                if close_call_distance <= 0:
                    raise errors.InvalidCloseCallDistanceError
                break
            except (errors.InvalidStepsError, errors.InvalidResolutionError,
                    errors.InvalidMetersPerPixelError,
                    errors.InvalidCloseCallDistanceError) as exc:
                print(exc)
            except ValueError:
                print("This value must be a number.")

        # Center object configuration
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

        # Point objects configuration
        point_objs = []
        while True:
            try:
                n = int(input("Amount of point objects (n): "))
                if n < 0:
                    raise errors.NegativePointObjectAmountError
                break
            except errors.NegativePointObjectAmountError as exc:
                print(exc)
            except ValueError:
                print("This value must be an integer.")
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
        return ConfigData(steps, resolution, meters_per_pixel, close_call_distance,
                          center_obj, point_objs)

    def _load_config(self, args) -> ConfigData:
        """Load configuration data from user input or a json file"""
        config_data = None
        if self._args.file is not None:
            try:
                config_data = ConfigData.from_json(args.file[0])
            except (errors.NegativeMassError, errors.NegativeDiameterError,
                    errors.UnableToOpenConfigError, errors.InvalidStepsError,
                    errors.InvalidResolutionError, errors.InvalidMetersPerPixelError,
                    errors.InvalidCenterObjectDataError,
                    errors.InvalidPointObjectDataError,
                    errors.InvalidCloseCallDistanceError) as exc:
                print(exc)
                exit()
        else:
            config_data = self._load_config_from_input()
        return config_data

    def output_to_console(self):
        """Output the simulation results to the console"""
        if not self._args.quiet:
            print(self._output_col)
            self._output_img.show()

    def output_to_file(self):
        """Output the simulation results to files"""
        if self._args.save:
            file_name = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
            try:
                end_config_data = ConfigData(self._start_config_data.steps,
                                             self._start_config_data.resolution,
                                             self._start_config_data.meters_per_pixel,
                                             self._start_config_data.close_call_distance,
                                             self._sim.center_obj, self._sim.point_objs)
                end_config_data.save_data_to_json(f"{file_name}.json")
                self._output_img.save(f"{file_name}.png")
                with Path.open(f"{file_name}.txt", "w") as file:
                    file.write(self._output_col)
            except PermissionError as exc:
                print(exc)
                exit()


if __name__ == "__main__":
    cli = CommandLineInterface(sys.argv[1:])
    cli.output_to_console()
    cli.output_to_file()
