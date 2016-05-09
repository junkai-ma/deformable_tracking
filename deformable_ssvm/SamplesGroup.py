import numpy as np
import HaarFeatures
import Point
import C_GetFeature


class SamplesGroup:
    def __init__(self, rects):
        self.rect_h = rects[0][0].height
        self.rect_w = rects[0][0].width
        self.row_num = len(rects)
        self.column_num = len(rects[0])
        self.rects = rects
        self.location_x = np.zeros((self.row_num, self.column_num), dtype=np.int32)
        self.location_y = np.zeros_like(self.location_x)
        self.toplefts = np.zeros((self.row_num, self.column_num, 2), dtype=np.int32)
        for i in range(self.row_num):
            for j in range(self.column_num):
                self.location_x[i, j] = rects[i][j].Center().x
                self.location_y[i, j] = rects[i][j].Center().y
                self.toplefts[i, j, 0] = rects[i][j].x_min
                self.toplefts[i, j, 1] = rects[i][j].y_min

        # the third parameter is dependent on the type of feature
        self.feature = np.empty((self.row_num, self.column_num, 192), dtype=np.float32)
        # self.feature_py = np.empty((self.row_num, self.column_num, 192), dtype=np.float32)

    def CalFeatureFromImg(self, integralImg):
        C_GetFeature.GetGroupFeature_fun(integralImg, self.toplefts, self.feature, self.rect_w, self.rect_h)

    '''
    def CalFeatureFromImg_py(self, image_rep):
        for i in range(self.row_num):
            for j in range(self.column_num):
                self.feature_py[i, j, :] = HaarFeatures.HaarFeatures(image_rep,
                                                                  self.rects[i][j]).GetFeatureVec()
    '''

    def GetFeatureByIndex(self, coordinate):
        return self.feature[coordinate.x, coordinate.y, :]

    def GetRectCenterByIndex(self, coordinate):
        x = self.location_x[coordinate.x, coordinate.y]
        y = self.location_y[coordinate.x, coordinate.y]
        return Point.Point(x, y)

    def GetRectByIndex(self, coordinate):
        return self.rects[coordinate.x][coordinate.y]

    def __str__(self):
        return 'The number of rows is %d and column is %d' % (self.row_num, self.column_num)


if __name__ == '__main__':
    import ImageRep
    import cv2
    import Rect
    import Coordinate

    testImage = cv2.imread('00062.jpg')
    newImageRep = ImageRep.ImageRep(testImage)
    integralImgIns = newImageRep.integralImages[0]
    testRect = [[Rect.Rect(58, 100, 30, 30), Rect.Rect(60, 120, 40, 40)],
                [Rect.Rect(58, 100, 30, 30), Rect.Rect(60, 120, 40, 40)]]

    sample = SamplesGroup(testRect)
    print sample
    sample.CalFeatureFromImg_py(newImageRep)
    print sample.feature[0, 0, 1]
    sample.CalFeatureFromImg(integralImgIns)
    print sample.rects[1][1]
    index = Coordinate.Coordinate(1, 1)
    aaa = sample.GetFeatureByIndex(index)
    print aaa
    bbb = sample.GetRectCenterByIndex(index)
    print bbb
    ind_rect = sample.GetRectByIndex(index)
    print ind_rect
