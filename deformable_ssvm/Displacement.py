import numpy as np
import Coordinate


class Displacement(Coordinate.Coordinate):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self):
        return np.sqrt(np.square(self.x)+np.square(self.y))
