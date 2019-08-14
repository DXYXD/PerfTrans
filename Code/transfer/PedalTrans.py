#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 19:52:31 2019

@author: verasun
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 17:57:49 2019

@author: verasun
"""
import sys, getopt
import pretty_midi as pm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cm
import pandas as pd
import seaborn as sns


def create_data_frame(path):
    data = pd.read_excel(path)
    lst=[]
    total_lst = []
    for i in range(1, 73):
        lst = []
        for j in data[i][1:25]:
            lst.append(j)
        total_lst.append(lst)

    l = []
    for i in total_lst:
        sub = []
        if '-' in i:
            i.remove('-')
        sub.append(i[0])
        sub.append(sum(i[1:])>=16)
        l.append(sub)

    data_frame = {}
    for sub in l:
        name = str(sub[0][1:2])+str(sub[0][4:5])+str(sub[0][7:8])+str(sub[0][10:11])
        data_frame[name] = sub[-1];

    return data_frame

def find_nearest(E, note, data_frame):
    p = note.pitch
    d = note.end-note.start
    v = note.velocity

    d_lst = [0.25, 1, 4]
    v_lst = [30, 70, 110]

    # pitch
    if p in range(9, 21):
        p = 1
    elif p in range(21, 41):
        p = 2
    elif p in range(41, 78):
        p = 3
    else:
        p = 4

    # duration
    min_dist = d-0.25
    d0 = 0
    for i in range(len(d_lst)):
        if abs(d-d_lst[i]) < min_dist:
            d0 = i
    # velocity
    min_dist = v-30
    v0 = 0
    for i in range(len(v_lst)):
        if abs(v-v_lst[i]) < min_dist:
            v0 = i

    return data_frame[str(E)+str(p)+str(d0)+str(v0)]


def get_all_pedal_movement(data, s1m):
    all_move = []
    start_time = False
    end_time = False
    i = 0
    # an index token loop through control array
    while i <= len(data.control_changes)-1:

        if data.control_changes[i].value >= s1m and start_time == False:
            # the first control (pedal down movement)
            # +0.004 arbitrary number in case the first pedal starts precisely at t = 0
            start_time = data.control_changes[i].time + 0.004
            start_i = i
            i += 1
        elif data.control_changes[i].value >= s1m and start_time != False:
            # during the pedal, only the depth of pedal is changing
            if data.control_changes[i] != data.control_changes[-1]:
                i += 1
                continue
            else:
                end_i = i
                all_move.append(data.control_changes[start_i:end_i+1])
                break
        elif data.control_changes[i].value < s1m and start_time != False and end_time == False:
            # the last control (pedal up movement)
            end_time = data.control_changes[i].time
            end_i = i
            all_move.append(data.control_changes[start_i:end_i+1])
            start_time = False
            end_time = False
            i+=1
        else:
            i+=1

    return all_move


def on_which_pedal(note, pedal_lst):
    index = -1
    for i in range(len(pedal_lst)):
        if note.end > pedal_lst[i][0].time and note.end <= pedal_lst[i][-1].time:
            index = i
    if index < 0:
        return False
    else:
        return pedal_lst[index][-1].time


def PETA1_1(data, s1m): # peta1 step1: 手代脚extend all notes
    all_pedal_movement = get_all_pedal_movement(data, s1m)
    for pdm in all_pedal_movement:
        start_time = pdm[0].time
        if pdm[-1].value < s1m:
            end_time = pdm[-1].time
        else:
            end_time = data.notes[-1].end
        for note in data.notes:
            if note.end >= start_time and note.start <= end_time:
                if note.end < end_time:
                    note.end = end_time
            elif note.start >= end_time:
                break
    return data

def PETA1_3(data): # peta1 step3: remove all the pedals
    for pedal in data.control_changes:
        pedal.value = 0
    return data


def PETA2_1(data, s1m):
    pedal_lst = get_all_pedal_movement(data, s1m)
    pedal_dict = {}
    for note in data.notes:
        time = on_which_pedal(note, pedal_lst)
        pedal_dict[note] = time
    return pedal_dict

def PETA2_3(data, pedal_dict):
    for note in data.notes:
        if pedal_dict[note] != False:
            note.end = pedal_dict[note]
    return data

def PETA2_4(data, s1m, s1M, s2m, s2M):
    for pedal in data.control_changes:
        value1 = max(0, int((pedal.value-s1m) / (s1M-s1m) * (s2M-s2m) + s2m)) # in case value1 is negative
        if value1 <= 127:
            pedal.value = value1
        else: # in case value1 is greater than 127
            pedal.value = 127
    return data



def main():
    # read the instrument
    #data = pm.PrettyMIDI("chuange1(1).mid").instruments[0]
    data = pm.PrettyMIDI("/Users/verasun/Desktop/0704Transfer_Match/2-s-m.midi").instruments[0]
    all_pedals = get_all_pedal_movement(data, 60)
    pedal_dict = PETA2_1(data, 60)
    #for k, v in pedal_dict.items():
        #print(k, v)
        #print()

if __name__ == "__main__":
     main()




'----------------------------------------------------------------------------------------------------'


