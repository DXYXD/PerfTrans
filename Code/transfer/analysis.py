# python 3.7.1

import librosa
import librosa.display
import os 
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 
from scipy.interpolate import interp1d

class CSrelationship:
    def __init__(self, y, sr):
        self.filePath = ''           
        self.ref = 0.00002     #  constant reference threshold
        self.y_all, self.sr = y, sr     # audio time series, sampling rate of y; original sr: 48000
        self.popt = np.linspace(1, 3*64*88, 3*64*88)
        self.popt.shape = (88, 16, 4, 3)    
        # pitch(88 keys); velocity(16 levels from ppp to fff: 0-127); 
        # duration(4 levels from  staccato (0.02sec) to legato (1.0sec)); note(C2, C4, C6)

# Making the data into pitch*velocity*time data fram
    def to_df(self, start_time, diff, tof):
        d1 = 15000  # ?
        d2 = 5000   # ?
        self.frame = []
        cut1 = 1371*self.sr + 16*self.sr + 48000
        cut2 = 4646*self.sr + 16*self.sr + 58000
        if tof == 1:
            for i in range(5632): # 88*16*4*3 samples for each note
                if (i < 1372):
                    yi = self.y_all[(i*self.sr+self.sr*16+40000) : ((i+1)*self.sr + self.sr*16+40000 )]
                if (i >= 1372) & (i < 4647):
                    yi = self.y_all[cut1 + (i-1372)*self.sr: cut1 + (i-1372+1)*self.sr]
                if (i >= 4647):
                    yi = self.y_all[cut2 + (i-4647)*self.sr: cut2 + (i-4647+1)*self.sr]
                self.frame.append(yi)
        if tof == 0:
            for i in range(5632): # ?diff
                yi = self.y_all[((i + start_time)*self.sr - diff) : ((i + start_time + 1)*self.sr - diff)]
                self.frame.append(yi)
        noteArray = np.array(self.frame) # dataframe of one note: 5632*sr
        self.df = noteArray.flatten() # pull to one dimension
        self.df.shape = (88, 16, 4, self.sr) # reshape df

    # omit wavplot
    # omit delay_fit

# Computing decibel by time window with length t
# Average intensity of the ﬁrst phase of decay from the peak

    def compute_db(self, t):
        self.decibel = []
        for i in self.frame:
            energy = np.array(i ** 2)
            onset = np.where(energy == max(energy))[0][0] # the index of the maximum energy
            tp = np.sqrt(np.mean(energy[onset:(onset + t)])) # # root mean square amplitude of the ﬁrst 10ms after the peak
            self.decibel.append(librosa.amplitude_to_db([tp], self.ref)[0])

    # omit plot_3d_db
    # omit plot_db_note

    def compute_delay(self, threshold):
        self.delay = []
        length = self.sr//100
        for i in range(5632):
            j = 10
            tp = threshold+1
            while(tp > threshold):
                j+=1
                tp = np.sqrt(np.var((self.frame[i][j*length:j*length+length])))
            self.delay.append(float(j)/100)


    def transformation(self, dur_range, vel_range):
        self.db = np.array(self.decibel)
        self.db.shape = (88,len(vel_range),len(dur_range))

           
    def interpolation(self, note, duration, figure, dur_range, vel_range):
        x = vel_range
        self.transformation(dur_range, vel_range)
        y = self.db[note, :, duration]
        y = (y-min(y))/(max(y)-min(y))
        self.f = interp1d(x, y, kind='cubic')
        self.fl = interp1d(x, y, kind='linear')
 
        xnew = np.linspace(min(vel_range), max(vel_range), num=100, endpoint=True)
        if figure == 1:
            plt.plot(xnew,self.fl(xnew),'--')
            plt.xlabel('velocity')
            plt.ylabel('Loudness(db)')
            plt.show()
        
    
    def time_inter(self, note, velocity, dur_range, vel_range):
        self.dl = np.array(self.delay)
        self.dl.shape=(88,len(vel_range),len(dur_range))
        x = dur_range
        y = self.dl[note,velocity,:]
        self.ft = interp1d(x, y, kind='linear')

    # omit p2p

def main():
    os.chdir('D:\\Academic_work\\02_pianoTransfer\\codes\\Analysis_Audi')    
    st = [16, 26, 5, 17]
    diff1 = [27500, 25000, 28000, 7000]

    y1, sr1 = librosa.load('player_0113.wav', sr = None)

    so1 = CSrelationship(y1, sr1) 
    so1.to_df(st[1], diff1[1], 0)
    so1.compute_db(20)
    so1.compute_delay(0.003)
    # so1.interpolation(40, 2, 2)

    y2, sr2 = librosa.load('player_0116.wav', sr = None)
    so2 = CSrelationship(y2, sr2) 
    so2.to_df(st[0], diff1[3], 1)
    so2.compute_db(20)
    so2.compute_delay(0.003)
    # so2.interpolation(40, 2, None)
    # so2.interpolation(40, 2, 1)

    names = ['so1db(lab)', 'so3db(audio)', 'so1delay(lab)', 'so3delay(audio)']
    data = np.array([so1.decibel, so2.decibel, so1.delay, so2.delay]).T
    df=pd.DataFrame(columns=names,data=data)
    df.to_csv('anal2.csv', encoding='utf-8')


# if __name__ == "__main__":
#     main()

