class SupportVector:
    def __init__(self, p_index, y, b, g):
        # parameter describe
        # pIndex : which SupportPattern this SupportVector belongs to
        # y      : the index of the feature which indicates the best y
        # b      : beta value of each SupportVector
        # g      : the gradient of the
        self.pattern_index = p_index
        self.y_index = y
        self.beta = b
        self.gradient = g
