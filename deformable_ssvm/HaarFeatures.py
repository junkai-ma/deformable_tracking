import HaarRect
import numpy
import Rect

class HaarFeatures:
    def __init__(self, image_rep, bbox):
        self.featureCount = 192
        self.feature_rect = []
        self.feature = []

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
                    r = Rect.Rect(x+(ix-iw/2)*width, y+(iy-iw/2)*height, iw*width, iw*height)
                    for it in range(6):
                        self.feature_rect.append(HaarRect.HaarRect(r, it))

        for each_feature in self.feature_rect:
            self.feature.append(each_feature.Eval(image_rep))

    def GetFeatureVec(self):
        return numpy.array(self.feature)

    def WriteHaarFeatures(self,filename):
        result = open(filename,'w')
        for (i,eachHaar) in enumerate(self.features):
            result.write(eachHaar.__str__())
            result.write('the value of the haar is %f\n' % self.featVec[i] )

if __name__ == '__main__':
    import ImageRep
    import cv2
    import Kernel
    import matplotlib.pyplot as plt
    import SampleLoc

    testImage = cv2.imread('00062.jpg')
    newImageRep = ImageRep.ImageRep(testImage)
    testRect = Rect.Rect(58, 100, 85, 122)
    a = HaarFeatures(newImageRep, testRect).GetFeatureVec()
    samples = SampleLoc.PixelSample(testRect, 10)
    sample_kernel_value = numpy.zeros(len(samples))
    distance_kernel_value = numpy.zeros(len(samples))
    distance_group = []
    for (i, each_samples) in enumerate(samples):
        dx = each_samples.x_min - testRect.x_min
        dy = each_samples.y_min - testRect.y_min
        dxs = dx*dx
        dys = dy*dy
        temp_dis = numpy.array([dx, dy, dxs, dys])
        distance_group.append(temp_dis)
        temp_feature = HaarFeatures(newImageRep, each_samples).GetFeatureVec()
        sample_kernel_value[i] = Kernel.GaussianKernel_CalPro(a, temp_feature)
        distance_kernel_value[i] = Kernel.GaussianKernel_CalPro(numpy.zeros(4), temp_dis)

    plt.figure(1)
    plt.subplot(211)
    plt.plot(distance_kernel_value)
    plt.subplot(212)
    plt.plot(sample_kernel_value)
    plt.show()