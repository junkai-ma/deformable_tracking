import cv2
import Rect
import numpy
import PARAMETER
import ObjectParts


class ImageRep:
    def __init__(self, image, needIntegral = True, needGray = True):
        height, width, channels = image.shape
        
        self.originalImage = image

        if needGray:
            self.gray_image = []
            if channels == 1:
                self.gray_image.append(image)
            elif channels == 3:
                self.gray_image.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))

        if needIntegral:
            self.integralImages = []
            for i in range(len(self.gray_image)):
                self.integralImages.append(cv2.integral(self.gray_image[i]))
                
    def Sum(self, rect, channel=0):
        result = (self.integralImages[channel][rect.y_max, rect.x_max] -
                  self.integralImages[channel][rect.y_max, rect.x_min] -
                  self.integralImages[channel][rect.y_min, rect.x_max] +
                  self.integralImages[channel][rect.y_min, rect.x_min])

        return result

    def TargetVisible(self, target):
        img = self.originalImage.copy()
        cv2.rectangle(img, target.rootLoc.TopLeft(), target.rootLoc.BottomRight(), PARAMETER.GREEN)
        for (i, item) in enumerate(target.partsList):
            cv2.rectangle(img, item.TopLeft(), item.BottomRight(), PARAMETER.COLORLIST[i % PARAMETER.COLORLISTNUM])
        cv2.imshow('target', img)
        cv2.waitKey(0)
    '''
    def Hist(self,rect):
        #hist = numpy.zeros((self.kNumBins,1))
        hist = [0]*self.kNumBins
        norm = rect.Area()
        for p in range(self.kNumBins):
            sum_p = (self.integralHistImages[p][rect.y_max,rect.x_max] -
                     self.integralHistImages[p][rect.y_max,rect.x_min] -
                     self.integralHistImages[p][rect.y_min,rect.x_max] +
                     self.integralHistImages[p][rect.y_min,rect.x_min])
            hist[p] = sum_p/norm
        return hist
    
    def GetImage(self,channel = 0):
        return self.images[channel]

    def GetRect(self):
        return self.rect
    '''

if __name__ =='__main__':
    test_image = cv2.imread('00000001.jpg')
    newimagerep = ImageRep(test_image)
    test_rect = Rect.Rect(4, 4, 3, 3)
    cv2.imshow('first', newimagerep.images[0])
    cv2.waitKey(0)
    testSumRect = newimagerep.Sum(test_rect)
    print testSumRect
    imageRegion = newimagerep.images[0][test_rect.y_min:test_rect.y_min+test_rect.height,test_rect.x_min:test_rect.x_min+test_rect.width]
    print imageRegion
    print newimagerep.images[0][0, 0]
    print sum(newimagerep.integralImages[0][0, :])

    root1 = Rect.Rect(30, 30, 50, 50)
    parts = []
    for i in range(5):
        parts.append(Rect.Rect(i, i, i, i))

    Object = ObjectParts.ObjectParts(root1, parts)

    print Object
    
    newimagerep.TargetVisible(Object)
