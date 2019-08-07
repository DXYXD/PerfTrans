#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pretty_midi as pm
import numpy as np
import peta_testing
import algorithm


def note_extension(data, s1m):
    data = data.instruments[0]
    new_data = peta_testing.trans1(data, s1m)
    return new_data


def note_trans(data, csv_file, dur_range, vel_range, transdir):
    new_data = algorithm.exe(data, csv_file, dur_range, vel_range, transdir)
    return new_data


def pedal_trans(data, E, s1m, s1M, s2m, s2M, fn_out, label):
    if label == 1:
        after_PETA = peta_testing.PETA1(data, s1m, fn_out)
    elif label == 2:
        after_PETA = peta_testing.PETA2(data, s1m, s2M, s2m, s2M, fn_out)
    elif label == 3:
        after_PETA = peta_testing.PETA3(data, E, s1m, s1M, s2m, s2M, fn_out)
    elif label == 4:
        after_PETA = peta_testing.PETA4(data, fn_out)
    
    return after_PETA

def Perf_Trans(filename, csv_file, E, s1m, s1M, s2m, s2M, fn_out, label, dur_range, vel_range, transdir):
    original_data = pm.PrettyMIDI(filename)
    after_extend = note_extension(original_data, s1m)
    after_trans = note_trans(after_extend, csv_file, dur_range, vel_range, transdir)
    after_PETA = pedal_trans(after_trans, E, s1m, s1M, s2m, s2M, fn_out, label)

    original_data.instruments[0] = after_PETA
    original_data.write(fn_out)
    return after_PETA




def main():
    # path_1 = 'D:\\Academic_work\\00PerfTransfer\\Song\\midi_1\\standard\\'
    # path_2 = 'D:\\Academic_work\\00PerfTransfer\\Song\\midi_1\\experiments\\'
    # path_3 = 'D:\\Academic_work\\00PerfTransfer\\File\\csv\\'
    # path_4 = 'D:\\Academic_work\\00PerfTransfer\\Song\\midi_1\\transfer\\'
    # n = 6

    # for i in range(1,9):
    #     name1 = str(i) + '-s'
    #     path1 = path_1 + name1 + '.midi'
    #     for label in range(1,5):
    #         Perf_Trans(path1, path_3 + 'anal_new.csv', 0, 60, 70, 53, 62, 
    #             path_4 + 'A2L-' + name1 + '-'+ str(label) + '.midi', label)
    #     if i == 8:
    #         n = 4
    #     for j in range(1,n):
    #         for k in ['audi', 'lab']:
    #             name2 = str(i) + '-' + str(j) + '-' + k
    #             path2 = path_2 + name2 + '.midi'
    #             for label in range(1,5):
    #                 Perf_Trans(path2, path_3 + 'anal_new.csv', 0, 60, 70, 53, 62,
    #                             path_4 + 'L2A-' + name2 + '-' + str(label) + '.midi', label)

    path0 = 'D:\\Academic_work\\00PerfTransfer\\Song\\trial\\'
    path1 = 'D:\\Academic_work\\00PerfTransfer\\Song\\midi_2\\'
    path2 = 'D:\\Academic_work\\00PerfTransfer\\File\\csv\\'

    dur_range = [0.1,0.3,0.7,1] # new
    vel_range = list(range(1, 127, 8)) + [127] # new
    transdir = 0  # 0 audi to lab, 1 lab to audi
    # dur_range = [.02, .15, .3, .7] # old
    # vel_range = list(np.linspace(7, 127, 16)) # old

    for label in range(1,5):
        Perf_Trans(path1 +'chuange1.mid', path2 + 'anal_new.csv', 0, 60, 70, 53, 62, 
                    path0 + 'transP_chuange1_' + str(label) + '.mid', label, dur_range, vel_range, transdir)
        # Perf_Trans(path1 + 'chuange2.midi', path2 + 'anal_new.csv', 0, 60, 70, 53, 62, 
        #             'trans_chuange2_' + str(label) + '.midi', label, dur_range, vel_range, transdir)
        # Perf_Trans(path1 + 'EtudeN01inC_M_op10.midi', path2 + 'anal_new.csv', 0, 60, 70, 53, 62, 
        #             'trans_EtudeN01inC_M_op10_' + str(label) + '.midi', label, dur_range, vel_range, transdir)
        # Perf_Trans(path1 + 'PerludesAndFuguesIX_E_M.midi', path2 + 'anal_new.csv', 0, 60, 70, 53, 62, 
        #             'trans_PerludesAndFuguesIX_E_M_' + str(label) + '.midi', label, dur_range, vel_range, transdir)


if __name__ == "__main__":
    main()

