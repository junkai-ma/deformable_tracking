import SupportVector
import SupportPattern
import numpy as np
import Kernel
import random
import Distance_transform
import Point
import Coordinate
import PartsAnchorLocation
import AuxFunction
import Rect
import C_FilterResponse
import cv2


class LaRank:
    def __init__(self, part_model, debug_mode, weight_feature, svBudgetSize=50):
        self.sps = []
        self.svs = []
        sv_max = svBudgetSize+2
        self.m_K = np.zeros(shape=(sv_max, sv_max), dtype=float)
        # self.m_K = np.ndarray(shape=(sv_max, sv_max), dtype=float)
        self.sv_budget_size = svBudgetSize
        self.MAX_VALUE = 100000.0
        self.m_C = 100.0
        self.w_feature = weight_feature
        self.parts_num = len(part_model)-1
        self.debug_mode = debug_mode
        if self.debug_mode:
            self.debug_inf = ''
        self.anchor_location = PartsAnchorLocation.PartsAnchorLocation(part_model)
        self.anchor_normal_factor = 0.0
        # for debug
        self.object_function_value = 0.0

    def Evaluate(self, vector_feature_list):
        # the parameter should be a list that indicate the index of each part in support pattern
        g = 0.0
        # calculate the similar function
        for each_item in self.svs:
            kernel_value = 0.0
            support_pattern = self.sps[each_item.pattern_index]
            for (i, each_index) in enumerate(each_item.y_index):
                kernel_value += Kernel.GaussianKernel_CalPro(vector_feature_list[i],
                                                             support_pattern.GetFeatureSingle(i, each_index))
            g += each_item.beta * kernel_value
        return g

    def AddSupportVector(self, pattern_index, y, anchor_l, g, mode):
        new_support_vector = SupportVector.SupportVector(pattern_index, y, anchor_l, 0, g, mode)
        ind = len(self.svs)  # The ind means the index of the added new vector in the self.svs
        self.svs.append(new_support_vector)
        self.sps[pattern_index].AddRef()

        # update the kernel matrix m_K
        current_feature = self.sps[pattern_index].GetFeatureGroup(y)
        for i in range(ind):
            temp_feature = self.sps[self.svs[i].pattern_index].GetFeatureGroup(self.svs[i].y_index)
            self.m_K[(i, ind)] = self.CalTwoFeatureKernel(temp_feature, current_feature)/self.parts_num
            self.m_K[(ind, i)] = self.m_K[(i, ind)]

        self.m_K[(ind, ind)] = self.CalOneFeatureNorm(current_feature)/self.parts_num

        return ind

    def CalTwoFeatureKernel(self, feature_list1, feature_list2):
        if len(feature_list1) != len(feature_list2):
            # there should be a 'try' statement
            return

        res = 0.0
        for i in range(len(feature_list2)):
            res += Kernel.GaussianKernel_CalPro(feature_list1[i], feature_list2[i])

        return res

    def CalOneFeatureNorm(self, feature_list):
        res = 0.0
        for i in range(len(feature_list)):
            res += Kernel.GaussianKernel_CalNorm(feature_list[i])
        return res

    def Update(self, sample_list, y, im):
        new_support_pattern = SupportPattern.SupportPattern(sample_list, y, im)
        self.sps.append(new_support_pattern)

        self.ProcessNew(len(self.sps) - 1)
        self.BudgetMaintenance()

        for i in range(10):
            self.Reprocess()
            self.BudgetMaintenance()

        self.update_anchor_location()

    def GetCandidateSamplesRect(self):
        return self.anchor_location.Update_Rects()

    def ProcessNew(self, ind):
        p_index = self.AddSupportVector(ind, self.sps[ind].y_best, self.sps[ind].part_location,
                                        self.Evaluate(self.sps[ind].GetFeatureGroup(self.sps[ind].y_best)),
                                        'p')
        ind_grad_pair = self.MinGradient(ind)
        n_index = self.AddSupportVector(ind, ind_grad_pair['index'],
                                        ind_grad_pair['anchor_location'],
                                        ind_grad_pair['gradient'], 'n')
        self.SMOStep(p_index, n_index)

    def BudgetMaintenance(self):
        if self.sv_budget_size < len(self.svs):
            self.BudgetMaintenanceRemove()

    def BudgetMaintenanceRemove(self):
        min_value = self.MAX_VALUE
        p_index = -1
        n_index = -1

        for (temp_i, vector) in enumerate(self.svs):
            if vector.beta < 0:
                # if beta is less than zero, the vector is a negative vector
                for (j, second_vector) in enumerate(self.svs):
                    if second_vector.beta > 0 and vector.pattern_index == second_vector.pattern_index:
                        temp_j = j
                        break

                val = vector.beta * vector.beta * (self.m_K[temp_i, temp_i] +
                                                   self.m_K[temp_j, temp_j] -
                                                   2 * self.m_K[temp_i, temp_j])

                if val < min_value:
                    p_index = temp_j
                    n_index = temp_i
                    min_value = val

        # build the relationship of the sv and sp
        sp_table = [[] for i in range(len(self.sps))]
        for vector_num, each_vector in enumerate(self.svs):
            sp_table[each_vector.pattern_index].append(vector_num)

        # update the beta of the positive vector
        if self.svs[p_index].y_index == self.sps[self.svs[p_index].pattern_index].y_best:
            delta = 1
        else:
            delta = 0

        self.svs[p_index].beta += max(0, min(self.svs[n_index].beta, self.m_C * delta - self.svs[p_index].beta))

        temp_beta = self.svs[n_index].beta
        score_kernel_with_vector = self.m_K[n_index, :]
        temp_value = score_kernel_with_vector[n_index]
        # score_kernel_with_vector[n_index] = score_kernel_with_vector[len(self.svs)]
        try:
            score_kernel_with_vector[n_index] = score_kernel_with_vector[len(self.svs)-1]
        except IndexError:
            print(str(n_index))
            print(str(len(self.svs)))
        finally:
            score_kernel_with_vector[n_index] = score_kernel_with_vector[len(self.svs)-1]
        score_kernel_with_vector[len(self.svs)-1] = temp_value
        self.RemoveSupportVector(n_index)
        if p_index == len(self.svs):
            p_index = n_index

        # update the gradient of each support vector
        for (i, each_vector) in enumerate(self.svs):
            each_vector.gradient += temp_beta*score_kernel_with_vector[i]

        if len(sp_table[self.svs[p_index].pattern_index]) == 2 or self.svs[p_index].beta < 1e-6:
            temp_beta = self.svs[p_index].beta
            score_kernel_with_vector = self.m_K[p_index, :]
            temp_value = score_kernel_with_vector[p_index]
            score_kernel_with_vector[p_index] = score_kernel_with_vector[len(self.svs)-1]
            score_kernel_with_vector[len(self.svs)-1] = temp_value
            self.RemoveSupportVector(p_index)

        # update the gradient of each support vector
        for (i, each_vector) in enumerate(self.svs):
            each_vector.gradient += temp_beta*score_kernel_with_vector[i]


        """
        sp_table = [[] for i in range(len(self.sps))]
        for vector_num, each_vector in enumerate(self.svs):
            sp_table[each_vector.pattern_index].append(vector_num)


        remove_list = []
        for each_sp_group in sp_table:
            if len(each_sp_group) == 1:
                remove_list.append(each_sp_group[0])
        """

    def MinGradient(self, ind):
        pair = {'index': [], 'gradient': 0.0}
        current_sp = self.sps[ind]

        score_map, location_row, location_column = self.CalDiscriminantFunction(current_sp.samples)

        root_rect_group = current_sp.samples[0].rects
        best_rect = current_sp.samples[0].GetRectByIndex(current_sp.y_best[0])
        lost_function_map = self.CalLostFunction(root_rect_group, best_rect)

        # normalize the score_map and the lost_function_map
        max_loss_value = np.max(lost_function_map)
        min_loss_value = np.min(lost_function_map)

        max_score_value = np.max(score_map)
        min_score_value = np.min(score_map)

        loss_factor = 1.5*(max_score_value-min_score_value)/(max_loss_value-min_loss_value)

        if loss_factor == 0:
            loss_factor = 1

        sum_score = score_map+lost_function_map*loss_factor

        the_best = np.argmax(sum_score)

        best_root_r = the_best//sum_score.shape[1]
        best_root_c = the_best % sum_score.shape[1]

        pair['gradient'] = -sum_score[best_root_r, best_root_c]

        pair['index'].append(Coordinate.Coordinate(best_root_r, best_root_c))

        for i in range(1, len(current_sp.samples)):
            best_r = location_row[i-1][best_root_r, best_root_c]
            best_c = location_column[i-1][best_root_r, best_root_c]
            best_coordinate = Coordinate.Coordinate(best_r, best_c)
            pair['index'].append(best_coordinate)

        parts_rect = [current_sp.samples[i].GetRectByIndex(pair['index'][i]) for i in range(len(current_sp.samples))]
        # pair['anchor_location'] = AuxFunction.CalDistanceFromRect(parts_rect)
        pair['anchor_location'] = PartsAnchorLocation.PartsAnchorLocation(parts_rect)

        return pair

    def SMOStep(self, i_p, i_n):
        if i_p == i_n:
            return
        p_vector = self.svs[i_p]
        n_vector = self.svs[i_n]

        if p_vector.pattern_index != n_vector.pattern_index:
            return

        current_sp = self.sps[p_vector.pattern_index]

        if p_vector.gradient - n_vector.gradient > 1e-5:
            kii = self.m_K[i_p, i_p] + self.m_K[i_n, i_n] - 2 * self.m_K[i_p, i_n]
            lu = (p_vector.gradient - n_vector.gradient) / kii
            if p_vector.y_index == current_sp.y_best:
                delta_y = 1
            else:
                delta_y = 0
            l = max(0, min(lu, self.m_C * delta_y - p_vector.beta))

            p_vector.beta += l
            n_vector.beta -= l

            # update gradient
            for (temp_i, each_vector) in enumerate(self.svs):
                each_vector.gradient -= l * (self.m_K[temp_i, i_p] - self.m_K[temp_i, i_n])

        if abs(p_vector.beta) < 1e-8:
            self.RemoveSupportVector(i_p)
            if i_n == len(self.svs):
                i_n = i_p

        if abs(n_vector.beta) < 1e-8:
            self.RemoveSupportVector(i_n)

    def Loss(self, rect1, rect2):
        return 1 - rect1.Overlap(rect2)

    def RemoveSupportVector(self, ind):
        # ind :the index of the support vector
        self.sps[self.svs[ind].pattern_index].RemoveRef()
        if self.sps[self.svs[ind].pattern_index].refCount == 0:
            # refCount equals to 0 means this support pattern will not provide support vector any more
            self.sps.pop(self.svs[ind].pattern_index)
            for vector in self.svs:
                if vector.pattern_index > self.svs[ind].pattern_index:
                    vector.pattern_index -= 1

        if ind < len(self.svs) - 1:
            self.SwapSupportVectors(ind, len(self.svs) - 1)
            ind = len(self.svs) - 1

        self.svs.pop(ind)

    def SwapSupportVectors(self, ind1, ind2):
        self.svs[ind1], self.svs[ind2] = self.svs[ind2], self.svs[ind1]

        temp_row = self.m_K[ind1, :]
        self.m_K[ind1, :] = self.m_K[ind2, :]
        self.m_K[ind2, :] = temp_row

        temp_col = self.m_K[:, ind1]
        self.m_K[:, ind1] = self.m_K[:, ind2]
        self.m_K[:, ind2] = temp_col

    def ProcessOld(self):
        if len(self.sps) == 0:
            return
        ind = int(random.random() * len(self.sps))

        i_p = -1
        max_gradient = -self.MAX_VALUE

        for (temp_i, vector) in enumerate(self.svs):
            if vector.pattern_index != ind:
                continue

            if vector.y_index == self.sps[ind].y_best:
                is_equal = 1
            else:
                is_equal = 0

            if vector.gradient > max_gradient and vector.beta < self.m_C * is_equal:
                i_p = temp_i
                max_gradient = vector.gradient

        if i_p == -1:
            return

        ind_grad_pair = self.MinGradient(ind)
        i_n = -1

        for (temp_i, vector) in enumerate(self.svs):
            if vector.pattern_index != ind:
                continue

            if vector.y_index == ind_grad_pair['index']:
                i_n = temp_i
                break
        if i_n == -1:
            i_n = self.AddSupportVector(ind, ind_grad_pair['index'],
                                        ind_grad_pair['anchor_location'],
                                        ind_grad_pair['gradient'], 'n')

        self.SMOStep(i_p, i_n)

    def Optimize(self):
        self.object_function_value = self.object_function_debug()
        if len(self.sps) == 0:
            return

        ind = int(random.random() * len(self.sps))
        i_p = -1
        i_n = -1
        max_gradient = -self.MAX_VALUE
        min_gradient = self.MAX_VALUE

        for (temp_i, vector) in enumerate(self.svs):
            if vector.pattern_index != ind:
                continue

            if vector.y_index == self.sps[ind].y_best:
                is_equal = 1
            else:
                is_equal = 0

            if vector.gradient > max_gradient and vector.beta < self.m_C * is_equal:
                i_p = temp_i
                max_gradient = vector.gradient

            if vector.gradient < min_gradient:
                i_n = temp_i
                min_gradient = vector.gradient

        if i_p == -1 or i_n == -1:
            return

        self.SMOStep(i_p, i_n)
        self.object_function_value = self.object_function_debug()

    def Reprocess(self):
        self.ProcessOld()
        for i in range(10):
            self.Optimize()

    def MatchBestCandidate(self, all_parts_samples):
        root_score_map, part_location_r, part_location_c = self.CalDiscriminantFunction(all_parts_samples)

        best_root = np.argmax(root_score_map)
        best_root_r = best_root//all_parts_samples[0].column_num
        best_root_c = best_root % all_parts_samples[0].column_num

        best_rects = []
        best_coordinate = []
        best_coordinate.append(Coordinate.Coordinate(best_root_r, best_root_c))
        best_rects.append(all_parts_samples[0].GetRectByIndex(best_coordinate[0]))
        for i in range(1, len(all_parts_samples)):
            best_r = part_location_r[i-1][best_root_r, best_root_c]
            best_c = part_location_c[i-1][best_root_r, best_root_c]
            best_coordinate.append(Coordinate.Coordinate(best_r, best_c))
            best_rects.append(all_parts_samples[i].GetRectByIndex(best_coordinate[i]))

        return best_rects, best_coordinate

    def debug_output(self, file_name):
        file_name.write(self.debug_inf)
        self.debug_inf = ''

    def CalDiscriminantFunction(self, all_parts):
        score_map = self.BestScoreMap(0, all_parts[0])

        location_r = []
        location_c = []

        for part_num in range(1, len(all_parts)):
            # scores_list = []
            scores = self.BestScoreMap(part_num, all_parts[part_num])
            scores = scores*self.w_feature
            (max_map, r_index, c_index) = Distance_transform.Distance_Transform_L1(scores)

            # translate the coordinates of each part into the corresponding of root
            score_map += max_map
            location_r.append(r_index)
            location_c.append(c_index)

        return score_map, location_r, location_c

    def BestScoreMap(self, part_num, sample_map):
        # sample_map is a SamplesGroup
        score_map = np.zeros((sample_map.row_num, sample_map.column_num))
        for each_vector in self.svs:
            sp_index = each_vector.pattern_index
            y_index = each_vector.y_index[part_num]
            sv_feature = self.sps[sp_index].samples[part_num].GetFeatureByIndex(y_index)
            score_map += each_vector.beta*self.CalScoreFunction(sample_map, sv_feature)
        return score_map

    def CalScoreFunction(self, feature_map, feature_vector):
        score = np.empty((feature_map.row_num, feature_map.column_num), dtype=np.float32)
        C_FilterResponse.filter_response_gauss(feature_map.feature, feature_vector, score, 0.2)
        """
        for i in range(feature_map.row_num):
            for j in range(feature_map.column_num):
                score[i, j] = Kernel.GaussianKernel_CalPro(feature_map.feature[i, j, :], feature_vector)

        score_add = np.empty((feature_map.row_num, feature_map.column_num), dtype=np.float32)
        """
        return score

    def update_anchor_location(self):
        self.anchor_location.SetToZero()
        normalize_factor = 0
        for current_sv in self.svs:
            # only use the positive vector
            if current_sv.beta > 0:
                temp_anchor = current_sv.part_anchor_location*current_sv.beta
                self.anchor_location.add_new(temp_anchor)
                normalize_factor += current_sv.beta

        self.anchor_location *= (1/normalize_factor)

    def CalLostFunction(self, rect_group, ori_rect):
        rows = len(rect_group)
        columns = len(rect_group[0])
        lose_score = np.zeros((rows, columns))

        for row_num in range(rows):
            for column_num in range(columns):
                lose_score[row_num, column_num] = 1-ori_rect.Overlap(rect_group[row_num][column_num])

        return lose_score

    def relocation_sample_rests(self, rects):
        new_rect_locations = [rects[0], ]
        # new_rect_locations.append(rects[0])
        root_x = rects[0].x_min
        root_y = rects[0].y_min
        ind = 0
        for each_anchor in self.anchor_location.anchor_location:
            ind += 1
            new_x = root_x+each_anchor.x
            new_y = root_y+each_anchor.y
            new_rect_locations.append(Rect.Rect(new_x, new_y, rects[ind].width, rects[ind].height))

        return new_rect_locations

    def object_function_debug(self):
        value = 0.0
        for (i, each_vector) in enumerate(self.svs):
            pattern_index = each_vector.pattern_index
            rect_ori = self.sps[pattern_index].best_rect[0]
            rect_each = self.sps[pattern_index].samples[0].GetRectByIndex(each_vector.y_index[0])
            value -= each_vector.beta*self.Loss(rect_ori, rect_each)
            for (j, each_vector_2) in enumerate(self.svs):
                value -= 0.5*each_vector.beta*each_vector_2.beta*self.m_K[i, j]

        return value

    def sv_output(self, p_im, n_im):
        n_index = 0
        p_index = 0
        new_s = 60
        part_num = 1
        for each_sv in self.svs:
            sp = self.sps[each_sv.pattern_index]
            if each_sv.type == 'p':
                # draw a p vector
                roi = sp.samples[part_num].GetRectByIndex(each_sv.y_index[part_num])
                p_im_patch = cv2.resize(sp.im[roi.y_min:roi.y_min+roi.height, roi.x_min:roi.x_min+roi.width],
                                        (new_s, new_s))
                start_row = (p_index//10)*new_s
                start_col = (p_index%10)*new_s
                p_im[start_row:start_row+new_s, start_col:start_col+new_s] = p_im_patch
                p_index += 1

            if each_sv.type == 'n':
                # draw a p vector
                roi = sp.samples[part_num].GetRectByIndex(each_sv.y_index[part_num])
                n_im_patch = cv2.resize(sp.im[roi.y_min:roi.y_min+roi.height, roi.x_min:roi.x_min+roi.width],
                                        (new_s, new_s))
                start_row = (n_index//10)*new_s
                start_col = (n_index%10)*new_s
                n_im[start_row:start_row+new_s, start_col:start_col+new_s] = n_im_patch
                n_index += 1
