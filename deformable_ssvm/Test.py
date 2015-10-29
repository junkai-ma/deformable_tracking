import numpy
import cv2
import Rect
import ImageRep
import ObjectParts
import PartSamples
import Config
import SampleLoc
import HaarFeatures
import LaRank

'''
testImage = cv2.imread('00000001.jpg')
newImagerep = ImageRep.ImageRep(testImage)
rootRect = Rect.Rect(10,10,24,32)
partList = []
partList.append(Rect.Rect(16,14,6,8))
partList.append(Rect.Rect(14,20,8,10))
partList.append(Rect.Rect(23,18,10,8))

target = ObjectParts.ObjectParts(rootRect,partList)

targetCand = PartSamples.PartSamples(target,'pixel')

print len(targetCand.parts)

targetCand.GetFeatureGroup(newImagerep)

for item in targetCand.featureGroup:
    print len(item)

newImagerep.TargetVisible(target)
'''

# below is to read a sequence of images an input
Para = Config.Config('mytext.txt')

print Para.config_paras

imagePath = Para.config_paras['sequencePath']
targetRegion = Para.config_paras['initBBox']
startFrame = Para.config_paras['startFrame']
endFrame = Para.config_paras['endFrame']
img = cv2.imread(imagePath.format(startFrame))
imageRep = ImageRep.ImageRep(img)
targetRect = Rect.Rect(targetRegion[0], targetRegion[1],
                       targetRegion[2]-targetRegion[0], targetRegion[3]-targetRegion[1])
targetHaar = HaarFeatures.HaarFeatures(imageRep, targetRect)
targetFeature = targetHaar.GetFeatureVec() 
cv2.rectangle(img, (targetRegion[0], targetRegion[1]), (targetRegion[2], targetRegion[3]), (0, 255, 0))
cv2.imshow('img', img)
cv2.waitKey(0)

leaner = LaRank.LaRank()
samples_update = SampleLoc.RadialSample(targetRect, 10, 8, 20)
leaner.Update(samples_update, imageRep, 0)

output_file = open('result.txt', 'w')
'''
samples = SampleLoc.RadialSample(targetRect,10,8)

samplesFeature = []
for eachRect in samples:
    candidate = HaarFeatures.HaarFeatures(imageRep,eachRect)
    samplesFeature.append(candidate.GetFeatureVec()) 


cv2.imshow('img',img)
cv2.waitKey(0)
'''
for num in range(startFrame, endFrame):
    img = cv2.imread(imagePath.format(num))
    imageRep = ImageRep.ImageRep(img)
    output_file.write('current frame is the %d th :' % (num))

    samples = SampleLoc.PixelSample(targetRect, 20, False)
    samples_feature = []
    for each_rect in samples:
        candidate = HaarFeatures.HaarFeatures(imageRep, each_rect)
        samples_feature.append(candidate.GetFeatureVec())

    best_index = leaner.MatchBestCandidate(samples_feature)
    targetRect = samples[best_index]

    samples_update = SampleLoc.RadialSample(targetRect, 10, 8, 20)
    leaner.Update(samples_update, imageRep, 0)

    print 'current frame is the %d th\n' % num
    print 'the has %d patterns.\n' % len(leaner.sps)
    print 'the has %d vectors.\n' % len(leaner.svs)

    cv2.rectangle(img,(targetRect.x_min,targetRect.y_min),(targetRect.x_max,targetRect.y_max),(0,255,0))

    cv2.imshow('img', img)
    cv2.waitKey(100)

    output_file.write(targetRect.Rect2Str())
    output_file.write('\n')
    """
    # below is the tracking algorithm do not use the structure svm
    samples = SampleLoc.RadialSample(targetRect, 10, 8, 30)
    samplesFeature = []
    for eachRect in samples:
        candidate = HaarFeatures.HaarFeatures(imageRep, eachRect)
        samplesFeature.append(candidate.GetFeatureVec())

    samplesFeature = numpy.array(samplesFeature)
    # samplesFeature = samplesFeature.transpose()
    print 'current frame is the %d th' % (num)
    print samplesFeature.shape

    samplesPro = numpy.dot(samplesFeature, targetFeature)
    
    maxIndex = numpy.argmax(samplesPro)
    print maxIndex
    targetRect = samples[maxIndex]
    print targetRect 
    imageRep = ImageRep.ImageRep(img)
    targetHaar = HaarFeatures.HaarFeatures(imageRep,targetRect)
    targetFeature = targetHaar.GetFeatureVec() 
    cv2.rectangle(img,(targetRect.x_min,targetRect.y_min),(targetRect.x_max,targetRect.y_max),(0,255,0))

    cv2.imshow('img', img)
    cv2.waitKey(100)
    """
output_file.close()
