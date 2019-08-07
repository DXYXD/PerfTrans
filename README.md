# PerfTrans

summer research

## 7/25/2019
### Reported
1. Compute variance and mean of notes' duration and velocity. This is for detecting the differences of performance among different people.
2. The new csv data file, new transferred midi files
3. Modified match algorithm and matched midi files 

### New Staff
1. Integrate information of notes' duration and velocity(people's performance):
- Meta-data
- Enrich the information conveyed by features of data
2. In sight of new records
- Compare durations of Lab with that of Audi
- Compute decibels' differences
- Compute durations' envelope
- Observe abnormal situations of transferred midi file: problems, reasons and solutions


## 7/12/2019
### Reported
1. Created piece relations
2. Standard midi file

### New staff
1. Find the cause why duration in audi is shorter than that in lab
- compute the envelope of intensity
- notice the 'normal' notes and 'outliers'
2. Beat phenomena: 
- find the beat frequency of keys of the piano with more than one strings
- compare the frequency with data in records
- https://www.youtube.com/watch?v=mF5edFbqWaU
- https://www.youtube.com/watch?v=efwIvzv3MSM
3. Match
- Compare all experiment midi file with the standard midifile
- Match notes, generate relations and figures(like the form in cubase) to examine the match algorithm
- Calcualte variance of notes' velocity and duration
