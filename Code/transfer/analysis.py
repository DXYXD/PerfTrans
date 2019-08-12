# python 3.7.1

import numpy as np 
from scipy.interpolate import interp1d

class CSrelationship:
    def __init__(self, y, sr):
        self.y_all, self.sr = y, sr     # audio time series, sampling rate of y; original sr: 48000
        self.becibel = None 
        self.delay = None  
        # pitch(88 keys); velocity(16 levels from ppp to fff: 0-127); 
        # duration(4 levels from  staccato (0.02sec) to legato (1.0sec)); note(C2, C4, C6)


    def transformation(self, dur_range, vel_range):
        self.db = np.array(self.decibel)
        self.db.shape = (88,len(vel_range),len(dur_range))

           
    def interpolation(self, note, duration, dur_range, vel_range):
        x = vel_range
        self.transformation(dur_range, vel_range)
        y = self.db[note, :, duration]
        y = (y-min(y))/(max(y)-min(y))
        self.fl = interp1d(x, y, kind='linear')

    
    def time_inter(self, note, velocity, dur_range, vel_range):
        self.dl = np.array(self.delay)
        self.dl.shape=(88,len(vel_range),len(dur_range))
        x = dur_range
        y = self.dl[note,velocity,:]
        self.ft = interp1d(x, y, kind='linear')

