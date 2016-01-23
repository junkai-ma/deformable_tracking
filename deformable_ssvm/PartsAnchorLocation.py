import Point


class PartsAnchorLocation:
    def __init__(self, parts_location):
        # location is a list of points, the first is the root location and others is each part location
        self.root_location = parts_location[0]
        self.anchor_location = []
        for LocIdx in range(1,len(parts_location)):
            self.anchor_location.append(parts_location[LocIdx] - self.root_location)

    def LocationScale(self, beta):
        for each_anchor in self.anchor_location:
            each_anchor *= beta

    def __add__(self, other):
        num_of_part = len(self.anchor_location)
        new_anchor_location = PartsAnchorLocation([Point.Point(0, 0)]*(num_of_part+1))
        for idx in range(len(self.anchor_location)):
            new_anchor_location.anchor_location[idx] = self.anchor_location[idx] + other.anchor_location[idx]

        return new_anchor_location

    def __str__(self):
        s = ''
        for each in self.anchor_location:
            s += each.__str__()
            s += '\n'
        return s

if __name__ == '__main__':
    loc_a = [Point.Point(i, i) for i in range(5)]
    a = PartsAnchorLocation(loc_a)
    loc_b = [Point.Point(i, i) for i in range(6, 11)]
    b = PartsAnchorLocation(loc_b)

    print a
    print b

    c = a+b

    print c

    print 'Ok'
