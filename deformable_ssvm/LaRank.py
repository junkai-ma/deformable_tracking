import SupportVector
import SupportPattern
import numpy

class LaRank:
    def __init__(self, svMax):
        self.sps = []
        self.svs = []
        self.m_K = numpy.ndarray(shape=(svMax, svMax), dtype=float)

    def AddSupportVector(self, patter_index, y, g):
        new_support_vector = SupportVector.SupportVector(patter_index, y, 0, g)
        self.svs.append(new_support_vector)

    def Update(self, sample_list, ):
        new_support_pattern=SupportPattern.SupportPattern(sample_list)