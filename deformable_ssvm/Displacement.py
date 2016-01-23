import numpy as np
import Coordinate


class Displacement(Coordinate.Coordinate):
    def __init__(self, x, y):
        Coordinate.Coordinate.__init__(self, x, y)

    def distance(self):
        return np.sqrt(np.square(self.x)+np.square(self.y))

    def __mul__(self, scale):
        return Displacement(self.x*scale, self.y*scale)


if __name__ == '__main__':
    a = [Displacement(1, 2), Displacement(3, 4)]
    for i in range(len(a)):
        a[i] *= 3

    for each in a:
        print each
