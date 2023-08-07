from dataclasses import dataclass
import numpy as np

STROKE_WIDTH = 0.1
SIMULATION_SPEED = 5000
BASE_TRANSMISSION_CHANCE = 0.005


@dataclass
class Positions:
    school: np.ndarray
    housing: np.ndarray
    work: np.ndarray
    retirement_home: np.ndarray
    sports_centre: np.ndarray
    shops: np.ndarray
    bar: np.ndarray
    restaurant: np.ndarray
    club: np.ndarray
    theatre: np.ndarray
    clock: np.ndarray


positions = Positions(
    school=np.array([-4.25, 2.1, 0]),
    housing=np.array([-4.25, -1.7, 0]),
    work=np.array([2.73, 2.085, 0]),
    retirement_home=np.array([-0.03, -0.68, 0]),
    sports_centre=np.array([-0.03, -2.70, 0]),
    shops=np.array([2.75, -0.66, 0]),
    bar=np.array([2.20, -2.72, 0]),
    restaurant=np.array([3.85, -2.72, 0]),
    club=np.array([5.50, -2.72, 0]),
    theatre=np.array([5.50, -0.68, 0]),
    clock=np.array([-6.5, 3.7, 0]),
)
