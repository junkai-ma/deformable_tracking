class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '(%d, %d)' % (self.x, self.y)

    def __sub__(self, other):
        return Coordinate(self.x-other.x, self.y-other.y)

    def __add__(self, other):
        return Coordinate(self.x+other.x, self.y+other.y)

    def __mul__(self, scale):
        return Coordinate(self.x*scale, self.y*scale)

    def __eq__(self, other):
        if other.x == self.x and other.y == self.y:
            return True
        else:
            return False

    def SetZero(self):
        self.x = 0
        self.y = 0

if __name__ == '__main__':
    first = Coordinate(10, 20)
    second = Coordinate(5, 8)
    first_list = [first, second]
    second_list = [first, second]
    print first == second
    print first_list == second_list
    second_list[1] = Coordinate(2, 8)
    print first_list == second_list
