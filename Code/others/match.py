import pretty_midi
import pandas as pd
from pypianoroll import Multitrack
from matplotlib import pyplot as plt


def GVmidi(df, submidi, stdmidi, sub_name, std_name):
    new_out = df.iloc[:,4:8]

    new_notes1 = []
    for row in new_out.iterrows():
        new_notes1.append(pretty_midi.Note(
            velocity=int(row[1][3]), pitch=int(row[1][0]), start=row[1][1], end=row[1][2]))
    submidi.instruments[0].notes = new_notes1

    new_notes2 = []
    std_df = new_out = df.iloc[:,:4]
    for row in std_df.iterrows():
        new_notes2.append(pretty_midi.Note(
            velocity=int(row[1][3]), pitch=int(row[1][0]), start=row[1][1], end=row[1][2]))
    stdmidi.instruments[0].notes = new_notes2

    submidi.write(sub_name + '-m.midi')
    stdmidi.write(std_name + '-m.midi')

    loaded1 = Multitrack(sub_name + '-m.midi')
    loaded2 = Multitrack(std_name + '-m.midi')
    fig1, axs1 = loaded1.plot()
    fig2, axs2 = loaded2.plot()
    axs1[0].set_title('sub_mini')
    axs2[0].set_title('std_midi')
    # plt.show()
    fig1.savefig(sub_name + '.jpg')
    fig2.savefig(std_name + '.jpg')

    return new_notes1


def load(std_path, sub_path):
    stdmidi = pretty_midi.PrettyMIDI(std_path)
    submidi = pretty_midi.PrettyMIDI(sub_path)

    stdnotes = [{'std.start': n.start, 'std.end': n.end, 'std.pitch': n.pitch, 'std.velocity': n.velocity} for n in stdmidi.instruments[0].notes]
    subnotes = [{'sub.start': n.start, 'sub.end': n.end, 'sub.pitch': n.pitch, 'sub.velocity': n.velocity} for n in submidi.instruments[0].notes]
    stdnotes = sorted(stdnotes,key = lambda s: s['std.start']) 
    subnotes = sorted(subnotes,key = lambda s: s['sub.start']) 

    std_start = stdnotes[0]['std.start']
    sub_start = subnotes[0]['sub.start']
    stdnotes = [{'std.start': n['std.start']-std_start, 'std.end': n['std.end']-std_start, 'std.pitch': n['std.pitch'], 'std.velocity': n['std.velocity']} for n in stdnotes]
    subnotes = [{'sub.start': n['sub.start']-sub_start, 'sub.end': n['sub.end']-sub_start, 'sub.pitch': n['sub.pitch'], 'sub.velocity': n['sub.velocity']} for n in subnotes]

    return stdmidi, submidi, stdnotes, subnotes


def match(std_n, dyn_n, match_list, names, indexF, error, maxi):

    for err in error:
        for idx in indexF:
            match = dyn_n[idx]['match']
            lowerb = std_n[idx][names['stdSname']] - err
            upperb = std_n[idx][names['stdSname']] + err
            
            dyn_p = dyn_n[idx][names['dynPname']]
            
            t = idx + 1
            s = std_n[idx][names['stdSname']]
            while s <= upperb and match is False:
                if t >= maxi:
                    break
                    
                s = std_n[t][names['stdSname']] 
                if std_n[t][names['stdPname']] == dyn_p and std_n[t]['match'] is False:
                    dyn_n[idx]['match'] = True
                    std_n[t]['match'] = True
                    match = True
                    match_list.append((t, idx))
                t += 1
            
            t = idx - 1
            s = std_n[t][names['stdSname']]
            while s >= lowerb and match is False:
                if t < 0:
                    break
                    
                s = std_n[t][names['stdSname']]    
                if std_n[t][names['stdPname']] == dyn_p and std_n[t]['match'] is False:
                    dyn_n[idx]['match'] = True
                    std_n[t]['match'] = True
                    match = True
                    match_list.append((t, idx))
                t -= 1
    
    match_list = sorted(match_list,key = lambda s: s[0])
    ll = [t[0] for t in match_list]
    for i in range(maxi):
        if i not in ll:
            match_list.insert(i, (i, 'None'))
    
    new_notes = []
    for item in match_list:
        dit = std_n[item[0]]
        if item[1] == 'None':
            dit[names['dynEname']] = 0
            dit[names['dynPname']] = 0
            dit[names['dynSname']] = 0
            dit[names['dynVname']] = 0
        else:
            dit[names['dynEname']] = dyn_n[item[1]][names['dynEname']]
            dit[names['dynPname']] = dyn_n[item[1]][names['dynPname']]
            dit[names['dynSname']] = dyn_n[item[1]][names['dynSname']]
            dit[names['dynVname']] = dyn_n[item[1]][names['dynVname']]
        new_notes.append(dit)
    new_notes = sorted(new_notes,key = lambda s: s[names['stdSname']])

    df = pd.DataFrame(new_notes)
    df = df[['std.pitch', 'std.start', 'std.end', 'std.velocity', 
            'sub.pitch', 'sub.start', 'sub.end', 'sub.velocity', 'match']]

    return df

def exe(std_path, sub_path, std_name = 'newstdmidi', sub_name = 'newsubmidi', midiout = True):

    stdmidi, submidi, stdnotes, subnotes = load(std_path, sub_path)

    maxi = max(len(stdnotes),len(subnotes))
    mini = min(len(stdnotes),len(subnotes))
    names = {'dynPname': 'sub.pitch', 'stdPname': 'std.pitch', 'dynSname': 'sub.start',
                'stdSname': 'std.start', 'dynEname': 'sub.end', 'stdEname': 'std.end',
                'dynVname': 'sub.velocity', 'stdVname': 'std.velocity'}

    if len(stdnotes) >= len(subnotes):
        for i in range(mini,maxi):
            subnotes.append({'sub.start': 0, 'sub.end': 0, 'sub.pitch': 0, 'sub.velocity': 0})
    elif len(stdnotes) < len(subnotes):
        for i in range(mini,maxi):
            stdnotes.append({'std.start': 0, 'std.end': 0, 'std.pitch': 0, 'std.velocity': 0})
        
    indexF = []
    match_list = []
    for i in range(maxi):
        if subnotes[i][names['dynPname']] != stdnotes[i][names['stdPname']]:
            indexF.append(i)
            subnotes[i]['match'] = False
            stdnotes[i]['match'] = False
        else:
            match_list.append((i, i))
            stdnotes[i]['match'] = True
            subnotes[i]['match'] = True
    
    error = [0.02, 0.05, 0.1, 0.3, 0.5, 0.8]
    
    df = match(stdnotes, subnotes, match_list, names, indexF, error, maxi)

    if midiout is True:
        GVmidi(df, submidi, stdmidi, sub_name, std_name)

    return df

def main():
    path_1 = 'D:\\Academic_work\\00PerfTransfer\\Song\\midi_1\\standard\\'
    path_2 = 'D:\\Academic_work\\00PerfTransfer\\Song\\midi_1\\trans\\'
    n = 6
    for i in range(1,9):
        name1 = str(i) + '-s'
        path1 = path_1 + name1 + '.midi'
        if i == 8:
            n = 4
        for j in range(1,n):
            for k in ['audi', 'lab']:
                name2 = str(i) + '-' + str(j) + '-' + k
                path2 = path_2 + name2 + '.midi'
                df = exe(path1, path2, name1, name2)
                df.to_json(name2 + ".json")


if __name__ == "__main__":
    main()

