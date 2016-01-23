import cv2
import ImageRep
import SupportVector
import SupportPattern
import SamplesGroup
import SampleLoc
import Rect
import Coordinate
import numpy as np
import Distance_transform
import Kernel


def CalScoreFunction(feature_map, feature_vector):
    score = np.zeros((feature_map.row_num, feature_map.column_num))
    for i in range(feature_map.row_num):
        for j in range(feature_map.column_num):
            score[i, j] = Kernel.GaussianKernel_CalPro(feature_map.feature[i, j, :], feature_vector)
    return score


def update_anchor_location(self, sv_num):
    current_sv = self.svs[sv_num]
    temp_factor = self.anchor_normal_factor
    temp_factor += current_sv.beta
    self.anchor_location *= (self.anchor_normal_factor/temp_factor)
    self.anchor_location += (current_sv.beta/temp_factor)*current_sv.part_anchor_location


def BestScoreMap(the_num, sample_map):
    # sample_map is a SamplesGroup
    score_map = np.zeros((sample_map.row_num, sample_map.column_num))
    for each_vector in svs:
        sp_index = each_vector.pattern_index
        y_index = each_vector.y_index[the_num]
        sv_feature = sps[sp_index].samples[the_num].GetFeatureByIndex(y_index)
        score_map += each_vector.beta*CalScoreFunction(sample_map, sv_feature)
    return score_map


def MatchBestCandidate(all_parts_samples, W):
    root_score_map = BestScoreMap(0, all_parts_samples[0])

    part_location_r = []
    part_location_c = []

    for part_index in range(1, len(all_parts_samples)):
        # scores_list = []
        scores = BestScoreMap(part_index, all_parts_samples[part_index])
        scores = scores*W
        (max_map, r_index, c_index) = Distance_transform.Distance_Transform_L1(scores)

        # translate the coordinates of each part into the corresponding of root
        root_score_map += max_map
        part_location_r.append(r_index)
        part_location_c.append(c_index)

    best_root = np.argmax(root_score_map)
    best_root_r = best_root//all_parts_samples[0].column_num
    best_root_c = best_root % all_parts_samples[0].row_num

    best_rects = []
    best_coordinate = Coordinate.Coordinate(best_root_r, best_root_c)
    best_rects.append(all_parts_samples[0].GetRectByIndex(best_coordinate))
    for i in range(1, len(all_parts_samples)):
        best_rects.append(all_parts_samples[i].GetRectByIndex(best_coordinate))

    return best_rects


image_path = 'E:\\track_dataset\Board\Board\img\{:05d}.jpg'
a = cv2.imread(image_path.format(2))
cv2.namedWindow('img')
cv2.imshow('img', a)
cv2.waitKey(0)

part_amount = 4
sps = []
svs = []

# read the text file which has the part rectangles
part_rect = 'part_rects.txt'
frame_nums = []
rect_in_frame = []
for each_line in open(part_rect, 'r'):
    each_num = each_line.split(',')
    frame_nums.append(int(each_num[0]))
    img = cv2.imread(image_path.format(int(each_num[0])))
    new_img_rep = ImageRep.ImageRep(img)

    temp_rect = []
    for part_num in range(part_amount+1):
        x_min = int(each_num[part_num*4+1])
        y_min = int(each_num[part_num*4+2])
        width = int(each_num[part_num*4+3])
        height = int(each_num[part_num*4+4])
        temp_rect.append(Rect.Rect(x_min, y_min, width, height))

    rect_in_frame.append(temp_rect)
    for each_part in temp_rect:
        cv2.rectangle(img, (each_part.x_min, each_part.y_min),
                      (each_part.x_max, each_part.y_max), (255, 0, 0))

    cv2.namedWindow('img_ex')
    cv2.imshow('img_ex', img)
    cv2.waitKey(100)

    parts_sample_group = SampleLoc.PartsSample(temp_rect, 2, 2)
    parts_feature_group = []
    good_coordinate = []
    for each_sample_group in parts_sample_group:
        temp_feature_group = SamplesGroup.SamplesGroup(each_sample_group)
        temp_feature_group.CalFeatureFromImg(new_img_rep)
        temp_coordinate = Coordinate.Coordinate(2, 2)
        good_coordinate.append(temp_coordinate)
        parts_feature_group.append(temp_feature_group)

    temp_sp = SupportPattern.SupportPattern(parts_feature_group, good_coordinate)
    sps.append(temp_sp)
    svs.append(SupportVector.SupportVector(len(sps)-1, good_coordinate, temp_sp.part_location, 1, 0, 'p'))

test_frame_num = 27
img_test = cv2.imread(image_path.format(test_frame_num))
test_img_rep = ImageRep.ImageRep(img_test)
test_part_location = [[176, 158, 220, 189],
                      [330, 177, 55, 40],
                      [224, 253, 22, 26],
                      [267, 294, 24, 35],
                      [273, 227, 25, 24]]

test_part_rect = [Rect.Rect(m[0], m[1], m[2], m[3]) for m in test_part_location]

test_sample = SampleLoc.PartsSample(test_part_rect, 10, 10)
to_be_detected = []
for each in test_sample:
    temp_group = SamplesGroup.SamplesGroup(each)
    temp_group.CalFeatureFromImg(test_img_rep)
    to_be_detected.append(temp_group)

ok_rect = MatchBestCandidate(to_be_detected, 8)
for each_rect in ok_rect:
    cv2.rectangle(img_test, (each_rect.x_min, each_rect.y_min), (each_rect.x_max, each_rect.y_max), (0, 255, 0))

cv2.namedWindow('img_r')
cv2.imshow('img_r', img_test)
cv2.waitKey(0)

print('ok')








