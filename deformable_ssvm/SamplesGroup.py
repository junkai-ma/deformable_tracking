import Point

class SamplesGroup:
    def __init__(self, location, height, width):
        self.h = height
        self.w = width
        self.location = location

        self.feature = []

    def GetFeature(self, image_rep):
        self.