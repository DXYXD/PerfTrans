#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pretty_midi as pm
import peta_testing
import algorithm
from midi_fix import fix_instrument


def note_extension(data, s1m):
    data = data.instruments[0]
    new_data = peta_testing.trans1(data, s1m)
    return new_data


def note_trans(data, csv_file, dur_range, vel_range, transdir):
    new_data = algorithm.exe(data, csv_file, dur_range, vel_range, transdir)
    return new_data


def pedal_trans(data, E, s1m, s1M, s2m, s2M, label, pedal_file):
    if label == 1:
        after_PETA = peta_testing.PETA1(data, s1m)
    elif label == 2:
        after_PETA = peta_testing.PETA2(data, s1m, s2M, s2m, s2M)
    elif label == 3:
        after_PETA = peta_testing.PETA3(data, E, s1m, s1M, s2m, s2M, pedal_file)
    elif label == 4:
        after_PETA = peta_testing.PETA4(data)
    
    return after_PETA

def Perf_Trans(filename, csv_file, E, s1m, s1M, s2m, s2M, fn_out, label, dur_range, vel_range, transdir, pedal_file):
    original_data = pm.PrettyMIDI(filename)
    after_extend = note_extension(original_data, s1m)
    after_trans = note_trans(after_extend, csv_file, dur_range, vel_range, transdir)
    if label == 1:
        for pedal in after_trans.control_changes:
            pedal.value = 0
        original_data.instruments[0] = fix_instrument(after_trans)
        original_data.write(fn_out)
    else:
        after_PETA = pedal_trans(after_trans, E, s1m, s1M, s2m, s2M, label, pedal_file)
        original_data.instruments[0] = fix_instrument(after_PETA) 
        original_data.write(fn_out)

    return original_data


def test(original_mid_path, mid_file, csv_file, save_mid_path, transdir, pedal_file):

    # 0 audi to lab, 1 lab to audi
    if transdir == 0:
        prefix = 'A2L_' 
    if transdir == 1:
        prefix = 'L2A_'
    name = mid_file.split('.')[0] + '_'
    # dur_range = [.02, .15, .3, .7] # old
    # vel_range = list(range(7, 128, 8)) # old
    dur_range = [0.1,0.3,0.7,1] # new
    vel_range = list(range(1, 127, 8)) + [127] # new

    for label in range(1,2):
        Perf_Trans(original_mid_path + mid_file, csv_file, 0, 60, 70, 53, 62, 
                    save_mid_path + prefix + name +str(label) + '.mid', label, dur_range, vel_range, 
                    transdir, pedal_file)

    return 0



def main():

# 如果test1 请将test2 注释掉
# 如果进行test2 请将test1 注释掉

    # test1
    original_mid_path = 'D:\\Academic_work\\00PerfTransfer\\Song\\midi_2\\'
    csv_file = 'D:\\Academic_work\\00PerfTransfer\\File\\csv\\anal_new.csv'
    save_mid_path = 'D:\\Academic_work\\00PerfTransfer\\Song\\midi_2\\'
    pedal_file = 'D:\\Academic_work\\00PerfTransfer\\File\\csv\\pedal_testing_data.xlsx'
    transdir = 0
    mid_file = ['chuange1.mid']
    test(original_mid_path, mid_file[0], csv_file, save_mid_path, transdir, pedal_file)

    # test2




if __name__ == "__main__":
    main()

