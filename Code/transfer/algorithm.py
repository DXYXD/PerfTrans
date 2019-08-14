import numpy as np 
import pandas as pd 
from scipy.interpolate import griddata

def cal_ID(modep, v, d, vel_range, dur_range):
    x0 = np.array([[d, v] for v in vel_range for d in dur_range])
    value_v = modep.flatten()
 
    result = griddata(x0, value_v, (d, v), method='linear')

    return result


def ser_vd(modev, moded, I0, D0, vel_range, dur_range):
    x0 = np.array([[d, v] for v in vel_range for d in dur_range])
    value_v = modev.flatten()
    value_d = moded.flatten() 

    xt = np.linspace(0.1, 1, 100)
    yt = np.linspace(1,127,127)
    x, y = np.meshgrid(xt, yt)
    result_v = griddata(x0, value_v, (x, y), method='linear') - I0
    result_d = griddata(x0, value_d, (x, y), method='linear') - D0

    diff = abs(result_v) + abs(result_d)
    coordinate = np.where(diff==np.min(diff))
    v_h = coordinate[0][0]
    d_h = xt[coordinate[1][0]]

    return (v_h, d_h)


def vt_trans(track, mode1db, mode2db, mode1dur, mode2dur, dur_range, vel_range):
    notes = [{'pitch': track[i].pitch, 'start': track[i].start, 'end': track[i].end, 'velocity': track[i].velocity} for i in range(len(track))]

    for i in range(len(track)):
        n = notes[i]
        d = n['end']-n['start']
        v = n['velocity']
        p = n['pitch'] - 21
        
        if d <= max(dur_range) and d >= min(dur_range):
            I0 = cal_ID(mode1db[p,:,:], v, d, vel_range, dur_range)
            D0 = cal_ID(mode1dur[p,:,:], v, d, vel_range, dur_range)

            result = ser_vd(mode2db[p,:,:], mode2dur[p,:,:], I0, D0, vel_range, dur_range)

            v_h = result[0]
            d_h = result[1]
            # print('diff-v:', v_h-v, 'rate:', round(abs(v_h-v)/127, 4))
            # print('diff-d:', round(abs(d_h-d),4), 'rate:', round(abs(d_h-d)/1, 4))
        else:
            v_h = v
            d_h = d

        notes[i]['velocity'] = v_h
        notes[i]['end'] = track[i].start + d_h

    for i in range(len(track)):
        track[i].pitch = notes[i]['pitch']
        track[i].start = notes[i]['start']
        track[i].velocity = notes[i]['velocity']
        track[i].end = notes[i]['end']

    return track


def exe(midi_data, csv_file, dur_range, vel_range, transdir):

    df = pd.read_csv(csv_file)
    df = df.sort_values(by=['pitch','vel','dur'])
    track = midi_data.notes
    
    # 0 audi to lab, 1 lab to audi
    if transdir == 0:
        mode1db = np.array(df['db(audi)']).reshape(88, len(vel_range), len(dur_range))                  
        mode1dur = np.array(df['duration(audi)']).reshape(88, len(vel_range), len(dur_range))
        mode2db = np.array(df['db(lab)']).reshape(88, len(vel_range), len(dur_range))
        mode2dur = np.array(df['duration(lab)']).reshape(88, len(vel_range), len(dur_range))
    if transdir == 1:
        mode1db = np.array(df['db(lab)']).reshape(88, len(vel_range), len(dur_range))
        mode1dur = np.array(df['duration(lab)']).reshape(88, len(vel_range), len(dur_range))
        mode2db = np.array(df['db(audi)']).reshape(88, len(vel_range), len(dur_range))
        mode2dur = np.array(df['duration(lab)']).reshape(88, len(vel_range), len(dur_range))
    
    midi_data.notes = vt_trans(track, mode1db, mode2db, mode1dur, mode2dur, dur_range, vel_range)

    return midi_data