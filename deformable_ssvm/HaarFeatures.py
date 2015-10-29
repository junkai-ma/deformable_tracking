import HaarRect
import Rect
import numpy


class HaarFeatures:
    def __init__(self,repImage,bbox):
        self.featureCount = 192
        self.features = []
        self.featVec = []

        x = bbox.x_min
        y = bbox.y_min
        width = bbox.width
        height = bbox.height

        dx = [0.2,0.4,0.6,0.8]
        dy = [0.2,0.4,0.6,0.8]
        s = [0.2,0.4]

        for iy in dy:
            for ix in dx:
                for iw in s:
                    r = Rect.Rect(x+(ix-iw/2)*width,y+(iy-iw/2)*height,iw*width,iw*height)
                    for it in range(6):
                        self.features.append(HaarRect.HaarRect(r,it))

        for eachfeature in self.features:
            self.featVec.append(eachfeature.Eval(repImage))

    def GetFeatureVec(self):
        return numpy.array(self.featVec)

    def WriteHaarFeatures(self,filename):
        result = open(filename,'w')
        for (i,eachHaar) in enumerate(self.features):
            result.write(eachHaar.__str__())
            result.write('the value of the haar is %f\n' % self.featVec[i] )

if __name__ == '__main__':
    import ImageRep
    import cv2
    import Rect
    testImage = cv2.imread('00000001.jpg')
    newImageRep = ImageRep.ImageRep(testImage)
    testRect = Rect.Rect(148, 90, 35, 55)
    a = HaarFeatures(newImageRep,testRect)
    #print a.featVec
    a.WriteHaarFeatures('HaarFeatureforDebug.txt')
