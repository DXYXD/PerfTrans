# python 3.7.1

import numpy as np 
import pandas as pd 
from analysis import CSrelationship


def t_trans(pitch, velocity, dur, dur_range, vel_range):
    dd = dur
    if dur >= max(dur_range):
        dur = max(dur_range) - 0.01
    d, v = trans2level(dur, velocity, dur_range, vel_range) 

    so1.time_inter(pitch, v, dur_range, vel_range)
    so2.time_inter(pitch, v, dur_range, vel_range)

    if dd < min(dur_range) or dd > max(dur_range):
        return dd
    else:
        s0 = so1.ft(dd) 
        t1 = np.linspace(min(dur_range), max(dur_range), 50)
        s1 = so2.ft(t1)
        diff = np.abs(s1-s0)
        tstar = np.where(diff==min(diff))[-1]

        return t1[tstar][-1]


def v_trans(pitch, velocity, dur, dur_range, vel_range):
    if dur >= max(dur_range):
        dur = max(dur_range) - 0.01
    d, v = trans2level(dur, velocity, dur_range, vel_range) 

    so1.interpolation(pitch, d, dur_range, vel_range)
    so2.interpolation(pitch, d, dur_range, vel_range)

    if velocity < min(vel_range) or velocity >= max(vel_range):
        return velocity
    else:
        s0 = so1.fl(velocity)
        v1 = np.linspace(min(vel_range), max(vel_range), 120)
        s1 = so2.fl(v1)
        diff = np.abs(s1-s0)
        vstar = np.where(diff==min(diff))[0] + 8
        return vstar


def trans2level(d_data, v_data, dur_range, vel_range):
    diff = vel_range[1]-vel_range[0]
    return int(round(d_data // (max(dur_range)/len(dur_range)))), int(round(v_data // diff))


def vt_trans(track, dur_range, vel_range):
    notes = [{'pitch': track[i].pitch, 'start': track[i].start, 'end': track[i].end, 'velocity': track[i].velocity} for i in range(len(track))]

    for i in range(len(track)):
        n = notes[i]
        dur = n['end']-n['start']
        v = n['velocity']
        p = n['pitch'] - 21
        notes[i]['velocity'] = np.int(v_trans(p, v, dur, dur_range, vel_range)[-1])
        notes[i]['end'] = track[i].start + t_trans(p, notes[i]['velocity'], dur, dur_range, vel_range)

    for i in range(len(track)):
        track[i].pitch = notes[i]['pitch']
        track[i].start = notes[i]['start']
        track[i].velocity = notes[i]['velocity']
        track[i].end = notes[i]['end']

    return track


def exe(midi_data, csv_file, dur_range, vel_range, transdir):

    global so1
    global so2 

    if transdir == 0:
        df = pd.read_csv(csv_file)
        df = df.sort_values(by=['pitch','vel','dur'])
        so1 = CSrelationship(y=1, sr=1)
        so2 = CSrelationship(y=2, sr=2)
        so2.decibel = df['db(lab)']
        so1.decibel = df['db(audi)']
        so2.delay = df['duration(lab)']
        so1.delay = df['duration(audi)']
        s1 = np.array(so1.decibel)
        s1.shape=[88,len(vel_range),len(dur_range)]
        s2 = np.array(so2.decibel)
        s2.shape=[88,len(vel_range),len(dur_range)]
        track = midi_data.notes
        midi_data.notes = vt_trans(track, dur_range, vel_range)
    elif transdir == 1:
        df = pd.read_csv(csv_file)
        df = df.sort_values(by=['pitch','vel','dur'])
        so1 = CSrelationship(y=1, sr=1)
        so2 = CSrelationship(y=2, sr=2)
        so1.decibel = df['db(lab)']
        so2.decibel = df['db(audi)']
        so1.delay = df['duration(lab)']
        so2.delay = df['duration(audi)']
        s1 = np.array(so1.decibel)
        s1.shape=[88,len(vel_range),len(dur_range)]
        s2 = np.array(so2.decibel)
        s2.shape=[88,len(vel_range),len(dur_range)]
        track = midi_data.notes
        midi_data.notes = vt_trans(track, dur_range, vel_range)

    return midi_data



