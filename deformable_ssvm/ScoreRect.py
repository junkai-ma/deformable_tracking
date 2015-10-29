import Rect


class ScoreRect(Rect.Rect):
    def __init__(self, x_min, y_min, width, height, overlap=0, score=0):
        Rect.Rect.__init__(self, x_min, y_min, width, height)
        self.overlap = overlap
        self.score = score

    def SetOverlap(self, overlap):
        self.overlap = overlap

    def SetScore(self, score):
        self.score = score
