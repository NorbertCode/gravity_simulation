import numpy as np
from dataclasses import dataclass
from space_event import SpaceEvent


@dataclass
class SimulationOutput:
    # List of positions for each point object in each step
    simulation_steps: list[list[np.array]]
    collisions = list[SpaceEvent]
