import numpy as np
import cv2
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

exp_r_dic = {'0.02': '1', '0.03': '2', '0.04': '3', '0.05': '4', '0.06': '5', '0.07': '6',
             '0.08': '7', '0.09': '8', '0.1': '9', '0.11': '10', '0.12': '11', '0.13': '12'}

loss_w_dic = {'0.3': '1', '0.5': '2', '0.7': '3', '0.9': '4', '1.1': '5', '1.3': '6',
              '1.5': '7', '1.7': '8', '1.9': '9'}


def DPM_Tracker(Para):
    start_time = time.clock()

    imagePath = Para.config_paras['img_path']
    seq_path = Para.seq_path
    targetRegion = Para.config_paras['initBBox']

    startFrame = Para.config_paras['startFrame']
    endFrame = Para.config_paras['endFrame']
    img = cv2.imread(imagePath.format(startFrame))
    imageRep = ImageRep.ImageRep(img)
    imageIntegral = imageRep.integralImages[0]
    image_size = img.shape
    image_height = image_size[0]
    image_width = image_size[1]

    expand_factor = Para.config_paras['expand_r']
    search_expend_w = int(image_width*expand_factor)
    search_expand_h = int(image_height*expand_factor)

    sample_skip = 1

    kernel_score_w = Para.config_paras['score_w']
    sv_size = Para.config_paras['svmBudgetSize']
    loss_w = Para.config_paras['loss_w']

    targetRect = AuxFunction.TwoPointRegion2Rect(targetRegion)
    # distance = AuxFunction.CalDistanceFromRect(targetRect)
    end_time = time.clock()-start_time
    print '1st step time is %f' % end_time

    start_time = time.clock()
    samples_update = SampleLoc.PartsSample(targetRect, search_expend_w, search_expand_h, sample_step=sample_skip)
    rect_feature_group = [SamplesGroup.SamplesGroup(each_rect_group) for each_rect_group in samples_update]
    for each_group in rect_feature_group:
        each_group.CalFeatureFromImg(imageIntegral)
    end_time = time.clock()-start_time
    print '2nd step time is %f' % end_time

    img = AuxFunction.AddPartRegionOnImage(img, targetRect)
    cv2.namedWindow('img')
    cv2.imshow('img', img)
    cv2.waitKey(100)

    print 'step2'

    initial_best_coordinate = [Coordinate.Coordinate(int(search_expend_w/sample_skip)+1,
                                                     int(search_expand_h/sample_skip)+1)]*(len(targetRect))

    learner = LaRank.LaRank(targetRect, Para.config_paras['debug_mode'], kernel_score_w, loss_w, sv_size)
    im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    learner.Update(rect_feature_group, initial_best_coordinate, im_gray)
    targetRect, targetCoordinate = learner.MatchBestCandidate(rect_feature_group)

    result_name = seq_path+'result'+'_B'+str(sv_size)+'_Lw'+loss_w_dic[str(loss_w)]+ \
                  '_Er'+exp_r_dic[str(expand_factor)]+'.txt'
    result_file = open(result_name, 'w')
    result_file.write('%d %d %d %d\n' % (targetRect[0].x_min,
                                         targetRect[0].y_min,
                                         targetRect[0].width,
                                         targetRect[0].height))


    # p_vector_im = np.zeros((600, 600), dtype=np.uint8)
    # n_vector_im = np.zeros_like(p_vector_im, dtype=np.uint8)

    for num in range(startFrame+1, endFrame+1):
        start_time = time.clock()
        img = cv2.imread(imagePath.format(num))
        imageRep = ImageRep.ImageRep(img)
        imageIntegral = imageRep.integralImages[0]

        sample_rects = learner.relocation_sample_rests(targetRect)
        samples_update = SampleLoc.PartsSample(sample_rects, search_expend_w, search_expand_h, sample_step=sample_skip)
        # samples_update = SampleLoc.PartsSample(targetRect, search_expend_w, search_expand_h)
        rect_feature_group = [SamplesGroup.SamplesGroup(each_rect_group) for each_rect_group in samples_update]
        for each_group in rect_feature_group:
            each_group.CalFeatureFromImg(imageIntegral)

        # debug mode
        debug_data = []
        for part_num in range(1, len(rect_feature_group)):
            # scores_list = []
            debug_data.append(learner.BestScoreMap(part_num, rect_feature_group[part_num]))

        # if num == 10:
        #    print 'pause'

        targetRect, targetCoordinate = learner.MatchBestCandidate(rect_feature_group)
        im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        learner.Update(rect_feature_group, targetCoordinate, im_gray)
        # learner.sv_output(p_vector_im, n_vector_im)

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

        # cv2.imshow('debug_p_vector', p_vector_im)
        # cv2.waitKey(100)
        # cv2.imshow('debug_n_vector', n_vector_im)
        # cv2.waitKey(100)

        # debug mode end

        end_time = time.clock()-start_time
        print '- -  '*10
        print 'Cost time is %f' % end_time
        print 'current frame is the %d th\n' % num
        # print 'the has %d patterns.\n' % len(learner.sps)
        # print 'the has %d vectors.\n' % len(learner.svs)

        # write the result to a text
        result_file.write('%d %d %d %d\n' % (targetRect[0].x_min,
                                             targetRect[0].y_min,
                                             targetRect[0].width,
                                             targetRect[0].height))

    result_file.close()
    print 'Ok'

