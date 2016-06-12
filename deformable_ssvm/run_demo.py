import DPM_Tracker
import Config

seq_path = 'E:\\track_dataset\\Human7\\'
seq_name = 'Human7'
config_file = seq_path+seq_name+'_cfg.txt'

# exp_r_list = [0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13]
exp_r_list = [0.08, 0.10, 0.12, 0.13]
# exp_r_list = [0.13]
# loss_w_list = [0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9]
loss_w_list = [0.9, 1.3, 1.5]
# loss_w_list = [1.5]

parameter = Config.Config(config_file)
for i in range(len(exp_r_list)):
    parameter.config_paras['expand_r'] = exp_r_list[i]
    for j in range(len(loss_w_list)):
        parameter.config_paras['loss_w'] = loss_w_list[j]
        DPM_Tracker.DPM_Tracker(parameter)
'''

parameter = Config.Config(config_file)
DPM_Tracker.DPM_Tracker(parameter)
'''