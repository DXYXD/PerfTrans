#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pretty_midi as pm
import PedalTrans
import algorithm
from midi_fix import fix_instrument



def note_trans(data, csv_file, dur_range, vel_range, transdir):
    new_data = algorithm.exe(data, csv_file, dur_range, vel_range, transdir)
    return new_data


def Perf_Trans(filename, csv_file, E, s1m, s1M, s2m, s2M, fn_out, label, dur_range, vel_range, transdir, pedal_file):
    if label == 1:
        original_data = pm.PrettyMIDI(filename)
        new1 = PedalTrans.PETA1_1(original_data.instruments[0], s1m)
        new2 = note_trans(new1, csv_file, dur_range, vel_range, transdir)
        new3 = PedalTrans.PETA1_3(new2)
        original_data.instruments[0] = fix_instrument(new3)
        original_data.write(fn_out)
    elif label == 2:
        original_data = pm.PrettyMIDI(filename)
        pedal_dict = PedalTrans.PETA2_1(original_data.instruments[0], s1m)
        new2 = note_trans(original_data.instruments[0], csv_file, dur_range, vel_range, transdir)
        new3 = PedalTrans.PETA2_3(new2, pedal_dict)
        new4 = PedalTrans.PETA2_4(new3, s1m, s1M, s2m, s2M)
        original_data.instruments[0] = fix_instrument(new4)
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
    # original_mid_path = 'D:\\Academic_work\\00PerfTransfer\\Song\\midi_2\\'
    # csv_file = 'D:\\Academic_work\\00PerfTransfer\\File\\csv\\anal_new.csv'
    # save_mid_path = 'D:\\Academic_work\\00PerfTransfer\\Song\\midi_2\\'
    # pedal_file = 'D:\\Academic_work\\00PerfTransfer\\File\\csv\\pedal_testing_data.xlsx'
    # transdir = 0
    # mid_file = ['chuange1.mid']
    # test(original_mid_path, mid_file[0], csv_file, save_mid_path, transdir, pedal_file)


    # test2
    original_mid_path =  'D:\\Academic_work\\00PerfTransfer\\Song\\midi_1\\experiments\\' 
    csv_file = 'D:\\Academic_work\\00PerfTransfer\\File\\csv\\anal_new.csv'
    save_mid_path = 'D:\\Academic_work\\00PerfTransfer\\Song\\midi_1\\transfer\\A2L\\' 
    pedal_file = 'D:\\Academic_work\\00PerfTransfer\\File\\csv\\pedal_testing_data.xlsx'
    transdir = 0

    #seven music piecies
    n = 6
    for i in range(2, 9):
        if i == 8:
            n = 4
        for j in range(1, n):
            for k in ['audi']:
                mid_name = str(i) + '-' + str(j) + '-' + k + '.midi'
                test(original_mid_path, mid_name, csv_file, save_mid_path, transdir, pedal_file)



if __name__ == "__main__":
    main()

