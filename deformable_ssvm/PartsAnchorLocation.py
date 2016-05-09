import Point
import Rect


class PartsAnchorLocation:
    def __init__(self, parts_rect):
        # location is a list of rectangle, the first is the root and others is each part
        self.parts_rects = parts_rect
        parts_location = [Point.Point(each_rect.x_min, each_rect.y_min) for each_rect in parts_rect]
        self.root_location = parts_location[0]
        self.anchor_location = []
        for LocIdx in range(1, len(parts_location)):
            self.anchor_location.append(parts_location[LocIdx] - self.root_location)

    def LocationScale(self, beta):
        for each_anchor in self.anchor_location:
            each_anchor *= beta

    def add_new(self, new_other):
        for idx in range(len(self.anchor_location)):
            self.anchor_location[idx] = self.anchor_location[idx] + new_other.anchor_location[idx]

    def __mul__(self, scale):
        new_instance = PartsAnchorLocation(self.parts_rects)
        for ind in range(len(self.anchor_location)):
            new_instance.anchor_location[ind] = self.anchor_location[ind]*scale
        return new_instance

    def __str__(self):
        s = ''
        for each in self.anchor_location:
            s += each.__str__()
            s += '\n'
        return s

    def SetToZero(self):
        for each_point in self.anchor_location:
            each_point.SetZero()

    def Update_Rects(self):
        root_x = self.parts_rects[0].x_min
        root_y = self.parts_rects[0].y_min
        for ind in range(len(self.anchor_location)):
            self.parts_rects[ind+1].SetXMin(root_x+self.anchor_location[ind].x)
            self.parts_rects[ind+1].SetYMin(root_y+self.anchor_location[ind].y)

        return self.parts_rects

if __name__ == '__main__':
    loc_a = [Rect.Rect(i, i, i, i) for i in range(5)]
    a = PartsAnchorLocation(loc_a)
    loc_b = [Rect.Rect(i, i, i, i) for i in range(6, 11)]
    b = PartsAnchorLocation(loc_b)

    print a
    print b
    c = b*5
    print c

    a.add_new(c)

    print a

    print 'Ok'

    list_a = [8, 7, 1, 9]

    print list_a
