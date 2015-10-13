import numpy
import Rect
import ImageRep

class HaarRect:
    def __init__(self,bbox,haartype):
        self.bbox = bbox
        self.haar = haartype
        self.rects = []
        self.weights = []
        if haartype == 0:
            tempRect = Rect.Rect(bbox.x_min,bbox.y_min,bbox.width,int(bbox.height/2))
            self.rects.append(tempRect)
            #tempRect.SetYMin(bbox.y_min+bbox.height/2)
            tempRect = Rect.Rect(bbox.x_min,int(bbox.y_min+bbox.height/2),bbox.width,int(bbox.height/2))
            self.rects.append(tempRect)
            self.weights.append(1.0)
            self.weights.append(-1.0)
            self.factor = 255*1.0/2
        elif haartype == 1:
            tempRect = Rect.Rect(bbox.x_min,bbox.y_min,int(bbox.width/2),bbox.height)
            self.rects.append(tempRect)
            tempRect = Rect.Rect(int(bbox.x_min+bbox.width/2),bbox.y_min,int(bbox.width/2),bbox.height)
            self.rects.append(tempRect)
            self.weights.append(1.0)
            self.weights.append(-1.0)
            self.factor = 255*1.0/2
        elif haartype == 2:
            tempRect = Rect.Rect(bbox.x_min,bbox.y_min,int(bbox.width/3),bbox.height)
            self.rects.append(tempRect)
            #tempRect.SetXMin(bbox.x_min+bbox.width/3)
            tempRect = Rect.Rect(int(bbox.x_min+bbox.width/3),bbox.y_min,int(bbox.width/3),bbox.height)
            self.rects.append(tempRect)
            #tempRect.SetXMin(bbox.x_min+2*bbox.width/3)
            tempRect = Rect.Rect(int(bbox.x_min+2*bbox.width/3),bbox.y_min,int(bbox.width/3),bbox.height)
            self.rects.append(tempRect)
            self.weights.append(1.0)
            self.weights.append(-2.0)
            self.weights.append(1.0)
            self.factor = 255*2.0/3
        elif haartype == 3:
            tempRect = Rect.Rect(bbox.x_min,bbox.y_min,bbox.width,int(bbox.height/3))
            self.rects.append(tempRect)
            #tempRect.SetYMin(bbox.y_min+bbox.height/3)
            tempRect = Rect.Rect(bbox.x_min,int(bbox.y_min+bbox.height/3),bbox.width,int(bbox.height/3))
            self.rects.append(tempRect)
            #tempRect.SetYMin(bbox.y_min+2*bbox.height/3)
            tempRect = Rect.Rect(bbox.x_min,int(bbox.y_min+2*bbox.height/3),bbox.width,int(bbox.height/3))
            self.rects.append(tempRect)
            self.weights.append(1.0)
            self.weights.append(-2.0)
            self.weights.append(1.0)
            self.factor = 255*2.0/3 
        elif haartype == 4:
            tempRect = Rect.Rect(bbox.x_min,bbox.y_min,int(bbox.width/2),int(bbox.height/2))
            self.rects.append(tempRect)
            #tempRect.SetXMin(bbox.x_min+bbox.width/2)
            #tempRect.SetYMin(bbox.y_min+bbox.height/2)
            tempRect = Rect.Rect(int(bbox.x_min+bbox.width/2),int(bbox.y_min+bbox.height/2),
                                 int(bbox.width/2),int(bbox.height/2))
            self.rects.append(tempRect)
            #tempRect.SetXMin(bbox.x_min+bbox.width/2)
            tempRect = Rect.Rect(bbox.x_min,int(bbox.y_min+bbox.height/2),int(bbox.width/2),int(bbox.height/2))
            self.rects.append(tempRect)
            #tempRect.SetYMin(bbox.y_min+bbox.height/2)
            tempRect = Rect.Rect(int(bbox.x_min+bbox.width/2),bbox.y_min,int(bbox.width/2),int(bbox.height/2))
            self.rects.append(tempRect)
            self.weights.append(1.0)
            self.weights.append(1.0)
            self.weights.append(-1.0)
            self.weights.append(-1.0)
            self.factor = 255*1.0/2
        elif haartype == 5:
            tempRect = bbox
            self.rects.append(tempRect)
            tempRect = Rect.Rect(int(bbox.x_min+bbox.width/4),int(bbox.y_min+bbox.height/4),
                                 int(bbox.width/2),int(bbox.height/2))
            self.rects.append(tempRect)
            self.weights.append(1.0)
            self.weights.append(-4.0)
            self.factor = 255*3.0/4

    def __str__(self):
        numRect = len(self.rects)
        s = 'Number of the rects is %d,type of haarfeature is %d.\n'%(numRect,self.haar)
        s += 'The bbox is [%f,%f,%f,%f]\n' % (self.bbox.x_min,self.bbox.y_min,self.bbox.width,self.bbox.height)
        for i in range(numRect):
            s += '[%f,%f,%f,%f],the weight is %f\n' % (self.rects[i].x_min,self.rects[i].y_min,self.rects[i].width,self.rects[i].height,self.weights[i])
        s += 'the factor is %f\n' % (self.factor)
        return s

    def Eval(self,repImage):
        value = 0.0
        for (offset,eachRect) in enumerate(self.rects):
            value += self.weights[offset]*repImage.Sum(eachRect)

        return value/(self.factor*self.bbox.Area())


if __name__ == '__main__':
    import cv2
    test_image = cv2.imread('00000001.jpg')
    newimagerep = ImageRep.ImageRep(test_image)
    box_rect = Rect.Rect(10,10,25,25)
    for i in range(6):
        haarfeature = HaarRect(box_rect,i)
        print haarfeature.Eval(newimagerep)
        print haarfeature
    #haarfeature = HaarFeature(box_rect,5)
    #print haarfeature
