import Displacement
import SamplesGroup
import AuxFunction
import PartsAnchorLocation
import Point

class SupportPattern:
    def __init__(self, all_parts_samples, y, im):
        # instance of y:
        self.samples = all_parts_samples
        # for (i, each_sample_part) in enumerate(all_parts_samples):
        #     self.samples.append(SamplesGroup.SamplesGroup(each_sample_part))
        #     self.samples[i].CalFeatureFromImg(image_rep)
        # if use part-based model, y is a list
        self.y_best = y
        self.refCount = 0
        self.best_rect = []
        for i in range(0, len(y)):
            self.best_rect.append(self.samples[i].GetRectByIndex(y[i]))
        # self.part_location = AuxFunction.CalDistanceFromRect(self.best_rect)
        # part_top_left = [Point.Point(each_rect.x_min, each_rect.y_min) for each_rect in self.best_rect]
        self.part_location = PartsAnchorLocation.PartsAnchorLocation(self.best_rect)

        # for debug:
        self.im = im

    def AddRef(self):
        self.refCount += 1

    def RemoveRef(self):
        self.refCount -= 1

    def GetFeatureGroup(self, part_indexes):
        feature_group = []
        for (i, each_index) in enumerate(part_indexes):
            feature_group.append(self.samples[i].GetFeatureByIndex(each_index))

        return feature_group

    def GetFeatureSingle(self, idx, coordinate):
        return self.samples[idx].GetFeatureByIndex(coordinate)
