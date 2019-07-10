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
    # data = data.instruments[0]
    # print(data.instruments[0])
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
                #for k in all_move:
                    #print(2, i)
                #print()
                break
        elif data.control_changes[i].value < s1m and start_time != False and end_time == False:
            # the last control (pedal up movement)
            end_time = data.control_changes[i].time
            end_i = i
            all_move.append(data.control_changes[start_i:end_i+1])
            #for k in all_move:
                #print(1, k)
            #print()
            start_time = False
            end_time = False
            i+=1
        else:
            i+=1
            
    return all_move

def PETA1(data, s1m, fn_out):
    # create a pm object
    piano = pm.PrettyMIDI()
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
            
    for c in data.control_changes:
        c.value = 0
    #piano.instruments.append(data)
    #piano.write(fn_out)
    return data
                
def trans1(data, s1m):
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

def PETA2(data, s1m, s1M, s2m, s2M, fn_out):
    # create a pm object
    piano = pm.PrettyMIDI()

    for pedal in data.control_changes:
        # in case value1 is negative
        value1 = max(0, int((pedal.value-s1m) / (s1M-s1m) * (s2M-s2m) + s2m))
        if value1 <= 127:
            pedal.value = value1
        else:
            # in case value1 is greater than 127
            pedal.value = 127
        
    piano.instruments.append(data)
    piano.write(fn_out)
    return data
    
        
def PETA3(data, E, s1m, s1M, s2m, s2M, fn_out): #data is a MIDI instrument
    # E is E2, the objective environment
    # create a pm object
    #piano = pm.PrettyMIDI()
    
    # read the existing data dictionary
    sample_data = create_data_frame('pedal_testing_data.xlsx')
    # an array collects all controls in one pedal-down movement
    all_pedal_movement = get_all_pedal_movement(data, s2m)
    p_to_be_modi = []

    for pdm in all_pedal_movement:
        start_time = pdm[0].time
        if pdm[-1].value < s1m:
            end_time = pdm[-1].time
        else:
            end_time = data.notes[-1].end
        for note in data.notes:
            if note.end >= start_time and note.start <= end_time:
                disting = find_nearest(0, note, sample_data)
                # if distinguishable, PETA 2
                if disting == True:     
                    # two indices indicating the start and the end of the pedal
                    # sequence that have effects on this note
                    start_i, end_i = 0, 0
                    # two flags indicating whether the starting and ending indices
                    # have been found yet
                    f1,f2=1,1
                    for j in range(len(pdm)-1):
                        # if the start has not been found
                        if pdm[j+1].time>note.start and f1==1:
                            # j is the starting pedal
                            start_i=j
                            # the starting pedal is now found
                            f1=0
                        # if the ending pedal has not been found
                        if pdm[j+1].time>note.end and f2==1:
                            # j is the ending pedal
                            end_i=j
                            # the ending is not found
                            f2=0
                        # corner case: if the length of this note is longer than 
                        # this pedal-down movement, then all controls from the starting
                        # pedal to the end of this movement should be included
                        if j+1 == len(pdm)-1 and f2==1:
                            end_i = j+1
                            f2 = 0
                
                    for p in pdm[start_i:end_i+1]:
                        if p not in p_to_be_modi:
                            p_to_be_modi.append(p)
                        
                # if not distinguishable, PETA1
                else:
                    if note.end < end_time:
                        note.end = end_time
                        
            elif note.start >= end_time: 
                break
        

    for pedal in data.control_changes:
        if pedal not in p_to_be_modi:
            pedal.value = 0
        else:
            value1 = max(0, int((pedal.value-s1m) / (s1M-s1m) * (s2M-s2m) + s2m))
            if value1 <= 127:
                pedal.value = value1
            else:
                # in case value1 is greater than 127
                pedal.value = 127

        
    #piano.instruments.append(data)
    #piano.write(fn_out)
    return data

def PETA4(data, fn_out):
    piano = pm.PrettyMIDI()
    piano.instruments.append(data)
    piano.write(fn_out)
    return data
    

def main():
    # data only contains 1 instrument
    data = pm.PrettyMIDI("E_competition_1.midi").instruments[0]
    #for i in data.control_changes[len(data.control_changes)//2:]:
        #print(i)
    data_frame = create_data_frame('/Users/verasun/Desktop/research/pedal_testing_data.xlsx')
    for i in data.notes[100:150]:
        print(i)
    print()
    #for i in data.control_changes[len(data.control_changes)//2:]:
        #print(i)
    new_data = PETA4(data,'fn_out')
    #for i in new_data.control_changes[0:20]:
        #print(i)
    for i in new_data.notes[100:150]:
        print(i)
    #print(data.control_changes)
    #print('\n\n\n')
    #new_data = PETA3(data, 0, 60, 70, 53, 62, 'after_trans_Nocturnes_3.midi')
    #new_data = PETA4(data,  'new_Nocturne4.midi')
    #for j in new_data.control_changes:
        #print(j)    
    
    #print()
    #print(new_data.control_changes)
    #for note in new_data.notes:
        #print(note)
    #print(new_data)


# if __name__ == "__main__":
#     main()


    
    
        
