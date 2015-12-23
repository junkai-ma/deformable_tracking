import HaarFeatures


class SupportPattern:
    def __init__(self, sample_list, image_rep, y):
        self.y_candidates = []
        self.AddYCandidate(sample_list)
        self.feature_vectors = []
        self.GetRectFeature(image_rep)
        # if use part-based model, y is a list
        self.y_best = y
        self.refCount = 0
        self.part_location = []
        root = sample_list[0][y[0]]
        for i in range(1, len(y)):
            each_rect = sample_list[i][y[i]]
            temp_dis = [each_rect[0]-root[0], each_rect[1]-root[1]]
            self.part_location.append(temp_dis)


    def AddYCandidate(self, sample_list):
        # in this function the rectangles should be translate by the coordinate of the center rectangle
        self.y_candidates = sample_list

    def GetRectFeature(self, image_rep):
        for each_list in self.y_candidates:
            each_part_feature = []
            for each_item in each_list:
                each_haar = HaarFeatures.HaarFeatures(image_rep, each_item)
                each_part_feature.append(each_haar.GetFeatureVec())
            self.feature_vectors.append(each_part_feature)

    def AddRef(self):
        self.refCount += 1

    def RemoveRef(self):
        self.refCount -= 1

    def GetFeatureGroup(self, part_indexes):
        if len(part_indexes) == len(self.y_candidates):
            feature_group = []
            for (i, each_index) in enumerate(part_indexes):
                feature_group.append(self.feature_vectors[i][each_index])

            return feature_group
