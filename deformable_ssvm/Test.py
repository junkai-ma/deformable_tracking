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

num_of_parts = Para.config_paras['partsNum']

imagePath = Para.config_paras['sequencePath']
targetRegion = Para.config_paras['initBBox']
rootBox = Para.config_paras['rootBox']
rootRect = Rect.Rect(rootBox[0], rootBox[1], rootBox[2]-rootBox[0], rootBox[3]-rootBox[1])
startFrame = Para.config_paras['startFrame']
endFrame = Para.config_paras['endFrame']
img = cv2.imread(imagePath.format(startFrame))
imageRep = ImageRep.ImageRep(img)

'''
targetRect = Rect.Rect(targetRegion[0], targetRegion[1],
                       targetRegion[2]-targetRegion[0], targetRegion[3]-targetRegion[1])
targetHaar = HaarFeatures.HaarFeatures(imageRep, targetRect)
targetFeature = targetHaar.GetFeatureVec()
'''
targetRect = []
distance = []
for each_region in targetRegion:
    target_temp = Rect.Rect(each_region[0],
                            each_region[1],
                            each_region[2] - each_region[0],
                            each_region[3] - each_region[1])
    targetRect.append(target_temp)
    cv2.rectangle(img, (each_region[0], each_region[1]), (each_region[2], each_region[3]), (0, 255, 0))
    temp_dis = [each_region[0]-rootRect[0], each_region[1]-rootRect[1]]
    distance.append(temp_dis)
cv2.rectangle(img, (rootBox[0], rootBox[1]), (rootBox[2], rootBox[3]), (255, 0, 0))
cv2.namedWindow('img')
cv2.imshow('img', img)
cv2.waitKey(0)

learner = LaRank.LaRank(num_of_parts, Para.config_paras['debug_mode'])
samples_update = []
for i in range(num_of_parts):
    # samples_update.append(SampleLoc.RadialSample(targetRect[i], 10, 8, 20)) # old sample method,comment 1
    samples_update.append(SampleLoc.RegionSample(rootRect, targetRect[i], 2, 2, 10, 10))
learner.Update(samples_update, imageRep, [0]*num_of_parts)

output_file = open('result.txt', 'w')
debug_file = open('debug.txt', 'w')
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

    samples = []
    for i in range(num_of_parts):
        samples.append(SampleLoc.RegionSample(rootRect, targetRect[i], 2, 2, 20, 20))
        # samples.append(SampleLoc.PixelSample(targetRect[i], 20, False)) # comment 1

    samples_feature_group = []
    for i in range(num_of_parts):
        samples_feature = []
        for each_rect in samples[i]:
            candidate = HaarFeatures.HaarFeatures(imageRep, each_rect)
            samples_feature.append(candidate.GetFeatureVec())
        samples_feature_group.append(samples_feature)

    best_index = learner.MatchBestCandidate(samples_feature_group)
    # calculate the root_rect
    dx = 0
    dy = 0
    for i in range(num_of_parts):
        old_best_part = targetRect[i]
        new_best_part = samples[i][best_index[i]]
        old_center_x, old_center_y = old_best_part.GetCenter()
        new_center_x, new_center_y = new_best_part.GetCenter()
        dx += (new_center_x-old_center_x)
        dy += (new_center_y-old_center_y)

    dx = dx/num_of_parts
    dy = dy/num_of_parts

    rootRect.Translate(dx, dy)

    targetRect = []
    for i in range(num_of_parts):
        targetRect.append(samples[i][best_index[i]])

    samples_update = []
    for i in range(num_of_parts):
        samples_update.append(SampleLoc.RegionSample(rootRect, targetRect[i], 2, 2, 10, 10))
        # samples_update.append(SampleLoc.RadialSample(targetRect[i], 10, 8, 20)) # comment 1

    learner.Update(samples_update, imageRep, [0]*num_of_parts)

    print 'current frame is the %d th\n' % num
    print 'the has %d patterns.\n' % len(learner.sps)
    print 'the has %d vectors.\n' % len(learner.svs)

    for i in range(num_of_parts):
        cv2.rectangle(img, (targetRect[i].x_min, targetRect[i].y_min), (targetRect[i].x_max, targetRect[i].y_max),
                      (0, 255, 0))

    cv2.rectangle(img, (rootRect.x_min, rootRect.y_min), (rootRect.x_max, rootRect.y_max), (255, 0, 0))
    cv2.imshow('img', img)
    cv2.waitKey(100)

    for i in range(num_of_parts-1):
        output_file.write(targetRect[i].Rect2Str())
        output_file.write(',')
    output_file.write(targetRect[num_of_parts-1].Rect2Str())
    output_file.write('\n')

    if Para.config_paras['debug_mode']:
        learner.debug_output(debug_file)
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
debug_file.close()
