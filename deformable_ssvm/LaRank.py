import SupportVector
import SupportPattern
import numpy as np
import Kernel
import random


class LaRank:
    def __init__(self, num, debug_mode, svBudgetSize=200):
        self.sps = []
        self.svs = []
        sv_max = svBudgetSize+2
        self.m_K = np.ndarray(shape=(sv_max, sv_max), dtype=float)
        self.sv_budget_size = svBudgetSize
        self.MAX_VALUE = 1000.0
        self.m_C = 100.0
        self.parts_num = num
        self.debug_mode = debug_mode
        if self.debug_mode:
            self.debug_inf = ''

    def Evaluate(self, vector_feature_list):
        # the parameter should be a list that indicate the index of each part in support pattern
        g = 0.0
        # calculate the similar function
        for each_item in self.svs:
            kernel_value = 0.0
            support_pattern = self.sps[each_item.pattern_index]
            for (i, each_index) in enumerate(each_item.y_index):
                kernel_value += Kernel.GaussianKernel_CalPro(vector_feature_list[i],
                                                             support_pattern.feature_vectors[i][each_index])
            g += each_item.beta * kernel_value
        return g

    def AddSupportVector(self, pattern_index, y, g):
        new_support_vector = SupportVector.SupportVector(pattern_index, y, 0, g)
        ind = len(self.svs)  # The ind means the index of the added new vector in the self.svs
        self.svs.append(new_support_vector)
        self.sps[pattern_index].AddRef()

        # update the kernel matrix m_K
        current_feature = self.sps[pattern_index].GetFeatureGroup(y)
        for i in range(ind):
            temp_feature = self.sps[self.svs[i].pattern_index].GetFeatureGroup(self.svs[i].y_index)
            self.m_K[(i, ind)] = self.CalTwoFeatureKernel(temp_feature, current_feature)
            self.m_K[(ind, i)] = self.m_K[(i, ind)]

        self.m_K[(ind, ind)] = self.CalOneFeatureNorm(current_feature)

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

    def Update(self, sample_list, image, y):
        new_support_pattern = SupportPattern.SupportPattern(sample_list, image, y)
        self.sps.append(new_support_pattern)

        self.ProcessNew(len(self.sps) - 1)
        self.BudgetMaintenance()

        for i in range(10):
            self.Reprocess()
            self.BudgetMaintenance()

    def ProcessNew(self, ind):
        p_index = self.AddSupportVector(ind, self.sps[ind].y_best,
                                        self.Evaluate(self.sps[ind].GetFeatureGroup(self.sps[ind].y_best)))
        ind_grad_pair = self.MinGradient(ind)
        n_index = self.AddSupportVector(ind, ind_grad_pair['index'], ind_grad_pair['gradient'])
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

        self.svs[p_index].beta += self.svs[n_index].beta

        self.RemoveSupportVector(n_index)
        if p_index == len(self.svs):
            p_index = n_index

        if self.svs[p_index].beta < 1e-6:
            self.RemoveSupportVector(p_index)

        for vector in self.svs:
            this_ps = self.sps[vector.pattern_index]
            vector.gradient = - self.Loss(this_ps.y_candidates[vector.y_index], this_ps.y_candidates[this_ps.y_best]) \
                              - self.Evaluate(self.sps[vector.pattern_index].feature_vectors[vector.y_index])

    def MinGradient(self, ind):
        pair = {'index': [], 'gradient': 0.0}
        current_sp = self.sps[ind]
        for i in range(self.parts_num):
            sep_gradient = 100.0
            sep_index = -1
            for (j, each_item) in enumerate(current_sp.y_candidates[i]):
                grad = -self.Loss(each_item, current_sp.y_candidates[i][current_sp.y_best[i]]) - \
                        self.Evaluate(current_sp.feature_vectors[i][j])
                if grad < sep_gradient:
                    sep_gradient = grad
                    sep_index = j

            if sep_index != -1:
                pair['gradient'] += sep_gradient
                pair['index'].append(sep_index)

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
            i_n = self.AddSupportVector(ind, ind_grad_pair['index'], ind_grad_pair['gradient'])

        self.SMOStep(i_p, i_n)

    def Optimize(self):
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

    def Reprocess(self):
        self.ProcessOld()
        for i in range(10):
            self.Optimize()

    def MatchBestCandidate(self, sample_list):
        best_index = []
        for i in range(len(sample_list)):
            # scores_list = []
            scores_list = np.zeros(len(sample_list[i]))
            for (j, each_sample) in enumerate(sample_list[i]):
                for each_vector in self.svs:
                    sp = self.sps[each_vector.pattern_index]
                    scores_list[j] += each_vector.beta * \
                                      Kernel.GaussianKernel_CalPro(sp.feature_vectors[i][each_vector.y_index[i]],
                                                                   each_sample)

            if self.debug_mode:
                self.debug_inf += '%f\t' % scores_list.max()

            best_index.append(np.argmax(scores_list))

        if self.debug_mode:
            self.debug_inf += '\n'

        return best_index

    def debug_output(self, file_name):
        file_name.write(self.debug_inf)
        self.debug_inf = ''
