# python 3.7.1

import numpy as np 
import pandas as pd 
# import pretty_midi
import os
from analysis import CSrelationship


def t_trans(pitch, velocity, dur):
    if dur >= 1:
        dur = 0.99
    d, v = trans2level(dur, velocity) 

    so1.time_inter(pitch, v)
    so2.time_inter(pitch, v)

    x = [.02, .15, .3, .7]
    if dur < min(x):
        dur = min(x)
    elif dur > max(x):
        dur = max(x)

    s0 = so1.ft(dur)
    t1 = np.linspace(0.02,.2,50)
    s1 = so2.ft(t1)
    diff = np.abs(s1-s0)
    tstar = np.where(diff==min(diff))[-1]

    return t1[tstar][-1]

def v_trans(pitch, velocity, dur):
    if dur >= 1:
        dur = 0.99
    d, v = trans2level(dur, velocity) 

    if pitch > 87:
        pitch = 87
    so1.interpolation(pitch, d, 0)
    so2.interpolation(pitch, d, 0)

    x = np.linspace(7, 127, 16)
    if velocity < min(x):
        velocity = min(x)
    elif velocity > max(x):
        velocity = max(x)

    s0 = so1.fl(velocity)
    v1 = np.linspace(8, 127, 120)
    s1 = so2.fl(v1)
    diff = np.abs(s1-s0)
    vstar = np.where(diff==min(diff))[0] + 8
    
    return vstar

def trans2level(d_data, v_data):
    return int(d_data // 0.25), int(v_data // 8)

def vt_trans(track):
    for i in range(len(track)):
        # if track[i].pitch == 67:
        #     print(track[i])
        n = track[i]
        dur = n.end-n.start
        v = n.velocity
        p = n.pitch
        track[i].velocity = np.int(v_trans(p, v, dur)[-1])
    
    # print('\n\n')

    for i in range(len(track)):
        n = track[i]
        dur = n.end-n.start
        v = n.velocity
        p = n.pitch
        track[i].end = track[i].start + t_trans(p, v, dur)
        # if track[i].pitch == 67:
        #     print(track[i])

    return track


def exe(midi_data, csv_file):

    '''
    1. Audi to Lab
    '''

    df = pd.read_csv(csv_file)
    global so1 
    so1 = CSrelationship(y=1, sr=1)
    global so2
    so2 = CSrelationship(y=2, sr=2)
    so2.decibel = df['so1db(lab)']
    so1.decibel = df['so3db(audio)']
    so2.delay = df['so1delay(lab)']
    so1.delay = df['so3delay(audio)']
    s1 = np.array(so1.decibel)
    s1.shape=[88,16,4]
    s2 = np.array(so2.decibel)
    s2.shape=[88,16,4]
    # print(midi_file)
    # midi_data = pretty_midi.PrettyMIDI(midi_file)
    # track = midi_data.instruments[0].notes
    track = midi_data.notes
    midi_data.notes = vt_trans(track)
    # print(type(midi_data))

    #midi_data.write('trans.midi')

    return midi_data


if __name__ == "__main__":
    os.chdir('D:\\Academic_work\\00_music\\experiment') 
    exe('chuange1.midi', 'anal.csv')

