import numpy as np
import cv2
import Rect
import ImageRep
import Config
import SampleLoc
import HaarFeatures
import LaRank
import AuxFunction
import SamplesGroup
import time
import Coordinate
import draw_debug

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
start_time = time.clock()
Para = Config.Config('mytext.txt')

print Para.config_paras

num_of_parts = Para.config_paras['partsNum']

imagePath = Para.config_paras['sequencePath']
targetRegion = Para.config_paras['initBBox']
# rootBox = Para.config_paras['rootBox']
# rootRect = Rect.Rect(rootBox[0], rootBox[1], rootBox[2]-rootBox[0], rootBox[3]-rootBox[1])
startFrame = Para.config_paras['startFrame']
endFrame = Para.config_paras['endFrame']
img = cv2.imread(imagePath.format(startFrame))
imageRep = ImageRep.ImageRep(img)
imageIntegral = imageRep.integralImages[0]
image_size = img.shape
image_height = image_size[0]
image_width = image_size[1]

expand_factor = 0.05
search_expend_w = int(image_width*expand_factor)
search_expand_h = int(image_height*expand_factor)

kernel_score_w = Para.config_paras['score_w']
sv_size = Para.config_paras['svmBudgetSize']

targetRect = AuxFunction.TwoPointRegion2Rect(targetRegion)
distance = AuxFunction.CalDistanceFromRect(targetRect)
end_time = time.clock()-start_time
print '1st step time is %f' % end_time

start_time = time.clock()
samples_update = SampleLoc.PartsSample(targetRect, search_expend_w, search_expand_h)
rect_feature_group = [SamplesGroup.SamplesGroup(each_rect_group) for each_rect_group in samples_update]
for each_group in rect_feature_group:
    each_group.CalFeatureFromImg(imageIntegral)
end_time = time.clock()-start_time
print '2nd step time is %f' % end_time

img = AuxFunction.AddPartRegionOnImage(img, targetRect)
cv2.namedWindow('img')
cv2.imshow('img', img)
cv2.waitKey(0)

print 'step2'

initial_best_coordinate = [Coordinate.Coordinate(search_expend_w+1, search_expand_h+1)]*(len(targetRect))

learner = LaRank.LaRank(targetRect, Para.config_paras['debug_mode'], kernel_score_w, sv_size)
im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
learner.Update(rect_feature_group, initial_best_coordinate, im_gray)
targetRect, targetCoordinate = learner.MatchBestCandidate(rect_feature_group)

result_file = open('result.txt', 'w')
result_file.write('%d %d %d %d\n' % (targetRect[0].x_min,
                                     targetRect[0].y_min,
                                     targetRect[0].x_max,
                                     targetRect[0].y_max))

'''
samples = SampleLoc.RadialSample(targetRect,10,8)

samplesFeature = []
for eachRect in samples:
    candidate = HaarFeatures.HaarFeatures(imageRep,eachRect)
    samplesFeature.append(candidate.GetFeatureVec()) 


cv2.imshow('img',img)
cv2.waitKey(0)
'''

p_vector_im = np.zeros((600, 600), dtype=np.uint8)
n_vector_im = np.zeros_like(p_vector_im, dtype=np.uint8)

for num in range(startFrame+1, endFrame+1):
    start_time = time.clock()
    img = cv2.imread(imagePath.format(num))
    imageRep = ImageRep.ImageRep(img)
    imageIntegral = imageRep.integralImages[0]

    sample_rects = learner.relocation_sample_rests(targetRect)
    samples_update = SampleLoc.PartsSample(sample_rects, search_expend_w, search_expand_h)
    # samples_update = SampleLoc.PartsSample(targetRect, search_expend_w, search_expand_h)
    rect_feature_group = [SamplesGroup.SamplesGroup(each_rect_group) for each_rect_group in samples_update]
    for each_group in rect_feature_group:
        each_group.CalFeatureFromImg(imageIntegral)

    # debug mode
    debug_data = []
    for part_num in range(1, len(rect_feature_group)):
        # scores_list = []
        debug_data.append(learner.BestScoreMap(part_num, rect_feature_group[part_num]))

    if num == 45:
        print 'pause'

    targetRect, targetCoordinate = learner.MatchBestCandidate(rect_feature_group)
    im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    learner.Update(rect_feature_group, targetCoordinate, im_gray)
    learner.sv_output(p_vector_im, n_vector_im)

    img = AuxFunction.AddPartRegionOnImage(img, targetRect)
    cv2.imshow('img', img)
    cv2.waitKey(100)

    """
    cv2.imshow('debug_p_vector', learner.p_vector_debug)
    cv2.waitKey(100)
    cv2.imshow('debug_n_vector', learner.n_vector_debug)
    cv2.imshow(100)
    """

    # debug mode
    # b, g, r = cv2.split(img)
    # img_for_debug = cv2.merge([r, g, b])
    # debug_win = draw_debug.DrawDebug()
    # debug_win.show_data(img_for_debug, debug_data)

    cv2.imshow('debug_p_vector', p_vector_im)
    cv2.waitKey(100)
    cv2.imshow('debug_n_vector', n_vector_im)
    cv2.waitKey(100)

    # debug mode end

    if num%8 == 0:
        print "the 8th frame"

    end_time = time.clock()-start_time
    print '- -  '*10
    print 'Cost time is %f' % end_time
    print 'current frame is the %d th\n' % num
    print 'the has %d patterns.\n' % len(learner.sps)
    print 'the has %d vectors.\n' % len(learner.svs)

    # write the result to a text
    result_file.write('%d %d %d %d\n' % (targetRect[0].x_min,
                                         targetRect[0].y_min,
                                         targetRect[0].x_max,
                                         targetRect[0].y_max))

    """
    for i in range(num_of_parts-1):
        output_file.write(targetRect[i].Rect2Str())
        output_file.write(',')
    output_file.write(targetRect[num_of_parts-1].Rect2Str())
    output_file.write('\n')
    """

    """
    if Para.config_paras['debug_mode']:
        learner.debug_output(debug_file)
    """

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

result_file.close()
print 'Ok'
# debug_file.close()

