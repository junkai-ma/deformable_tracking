import HaarFeatures


class SupportPattern:
    def __init__(self, sample_list, image_rep, y):
        self.y_candidates = []
        self.AddYCandidate(sample_list)
        self.feature_vectors = self.GetRectFeature(image_rep)
        self.y_best = y
        self.refCount = 0

    def AddYCandidate(self, sample_list):
        # in this function the rectangles should be translate by the coordinate of the center rectangle
        self.y_candidates = sample_list

    def GetRectFeature(self, image_rep):
        features = []
        for each_item in self.y_candidates:
            each_haar = HaarFeatures.HaarFeatures(image_rep, each_item)
            features.append(each_haar.GetFeatureVec())
        return features

    def AddRef(self):
        self.refCount += 1

    def RemoveRef(self):
        self.refCount -= 1

    def SetPVectorIndex(self, ind):
        self.p_vector_index = ind

    def SetNVectorIndex(self, ind):
        self.n_vector_index = ind