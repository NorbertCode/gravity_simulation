import argparse
import simulation
import json

parser = argparse.ArgumentParser()
parser.add_argument("k", type=int, help="the amount of simulation steps")
parser.add_argument("-r", "--resolution", type=int, nargs=2,
                    default=(512, 512), help="resolution of output in pixels")
parser.add_argument("-p", "--meters-per-pixel", type=int,
                    default=27500, help="meters per pixel")
input_group = parser.add_mutually_exclusive_group(required=True)
input_group.add_argument("-f", "--file", type=str, nargs=1,
                         help="use the values from .json file")
input_group.add_argument("-v", "--values", nargs="*", help="input values manually")
args = parser.parse_args()

sim = simulation.Simulation(args.resolution, args.meters_per_pixel)
if args.file:
    with open(args.file[0], "r") as file:
        sim.init_from_json(json.load(file))
else:
    print(args.values)
output = sim.run(args.k)
sim.draw(output[0])
