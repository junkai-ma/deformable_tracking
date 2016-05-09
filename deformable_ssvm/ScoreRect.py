import Point
import Rect
import HaarFeatures


class ScoreRect(Rect.Rect):
    def __init__(self, r):
        Rect.Rect.__init__(self, r.x_min, r.y_min, r.width, r.height)
        self.center = self.Center()
        self.feature = []

    def Center(self):
        center_x = self.x_min+self.width/2
        center_y = self.y_min+self.height/2
        return Point.Point(center_x, center_y)

    def Feature(self, image_rep):
        self.feature = HaarFeatures.HaarFeatures(image_rep, self).GetFeatureVec()


if __name__ == '__main__':
    import ImageRep
    import cv2
    import Rect

    testImage = cv2.imread('00062.jpg')
    newImageRep = ImageRep.ImageRep(testImage)
    testRect = Rect.Rect(58, 100, 85, 122)

    ScoreR = ScoreRect(testRect)
    print ScoreR.feature
    ScoreR.Feature(newImageRep)
    print type(ScoreR.feature)
