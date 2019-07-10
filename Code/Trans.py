#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 17:21:32 2019

@author: verasun
"""

import pretty_midi as pm
import os
import peta_testing2
import algorithm2


def note_extension(data, s1m):
    data = data.instruments[0]
    new_data = peta_testing2.trans1(data, s1m)
    return new_data


def note_trans(data, csv_file):
    new_data = algorithm2.exe(data, csv_file)
    return new_data


def pedal_trans(data, E, s1m, s1M, s2m, s2M, fn_out, label):
    if label == 1:
        after_PETA = peta_testing2.PETA1(data, s1m, fn_out)
    elif label == 2:
        after_PETA = peta_testing2.PETA2(data, s1m , s2M, s2m, s2M, fn_out)
    elif label == 3:
        after_PETA = peta_testing2.PETA3(data, E, s1m, s1M, s2m, s2M, fn_out)
    elif label == 4:
        after_PETA = peta_testing2.PETA4(data, fn_out)
    # new_data = peta_testing2.PETA3(data, E, s1m, s1M, s2m, s2M, fn_out)
    
    return after_PETA

def Perf_Trans(filename, csv_file, E, s1m, s1M, s2m, s2M, fn_out, label):
    original_data = pm.PrettyMIDI(filename)
    after_extend = note_extension(original_data, s1m)
    after_trans = note_trans(after_extend, csv_file)
    after_PETA = pedal_trans(after_trans, E, s1m, s1M, s2m, s2M, fn_out, label)
    
    original_data.instruments[0] = after_PETA
    original_data.write(fn_out)
    return after_PETA


# Perf_Trans('try.midi', 'anal.csv', 0, 60, 70, 53, 62, 'after_trans_try.midi')

if __name__ == "__main__":
    os.chdir('D:\\Academic_work\\00_music\\experiment\\20190627')
    for label in range(1,5):
        Perf_Trans('chuange1.midi', 'anal2.csv', 0, 60, 70, 53, 62, 'trans_chuange1_' + str(label) + '.midi', label)
        Perf_Trans('chuange2.midi', 'anal2.csv', 0, 60, 70, 53, 62, 'trans_chuange2_' + str(label) + '.midi', label)
        Perf_Trans('EtudeN01inC_M_op10.midi', 'anal2.csv', 0, 60, 70, 53, 62, 'trans_EtudeN01inC_M_op10_' + str(label) + '.midi', label)
        Perf_Trans('PerludesAndFuguesIX_E_M.midi', 'anal2.csv', 0, 60, 70, 53, 62, 'trans_PerludesAndFuguesIX_E_M_' + str(label) + '.midi', label)