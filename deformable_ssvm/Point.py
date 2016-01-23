import numpy as np
import Displacement
import Coordinate


class Point(Coordinate.Coordinate):
    def __init__(self, x, y):
        Coordinate.Coordinate.__init__(self, x, y)

    def distance_from(self, sec_point):
        # P is another point
        dx = sec_point.x - self.x
        dy = sec_point.y - self.y

        return np.sqrt(np.square(dx), np.square(dy))

    def translate(self, t):
        self.x += t.x
        self.y += t.y

    def __sub__(self, other):
        return Displacement.Displacement(self.x-other.x, self.y-other.y)

if __name__ == '__main__':
    p = Point(10, 10)
    print p
    t = Displacement.Displacement(10, 10)
    p.translate(t)
    print p
    p1 = Point(10, 10)
    p2 = Point(20, 20)
    p3 = p2-p1
    print p3.__class__
    print p3
    print p3.distance()
    matrix_a = np.random.randint(0, 16, (3, 4))
    print matrix_a
    matrix_a *= 3
    print matrix_a
    max_ind = np.argmax(matrix_a)
    print max_ind
    r = max_ind//4
    c = max_ind % 4
    print (r, c)
