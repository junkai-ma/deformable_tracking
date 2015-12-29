import numpy as np
import Coordinate


class Point(Coordinate.Coordinate):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_from(self, sec_point):
        # P is another point
        dx = sec_point.x - self.x
        dy = sec_point.y - self.y

        return np.sqrt(np.square(dx), np.square(dy))

    def translate(self, t):
        self.x += t.x
        self.y += t.y

    def __str__(self):
        return '(%d,%d)' % (self.x, self.y)

if __name__ == '__main__':
    import Displacement
    p = Point(10, 10)
    print p
    t = Displacement.Displacement(10, 10)
    p.translate(t)
    print p
