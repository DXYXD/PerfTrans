import pretty_midi 
import json
import os

def attr(midifile, jsonfile, piecename, pedal_lowerb, pedal_upperb):
    midi_data = pretty_midi.PrettyMIDI(midifile)
    ListofCC = [{'number': cc.number, 'value': cc.value, 'time': cc.time} for cc in midi_data.instruments[0].control_changes]
    ListofNotes = [{'pitch':n.pitch, 'start': n.start, 'end': n.end, 'velocity':n.velocity} for n in midi_data.instruments[0].notes]
    
    def f1(dic):
        return dic['start']
    ListofNotes_sort = sorted(ListofNotes, key = f1)
    
    def f2(dic):
        return dic['time']
    ListofCC_sort = sorted(ListofCC, key = f2)
    
    ListofNotes = [] 
    for n in ListofNotes_sort:
        pedal_depth = []
        pedal_time = []
        
        for cc in ListofCC_sort:
            if cc['time'] >= n['start']:
                pedal_depth.append(cc['value'])
                pedal_time.append(cc['time'])
                if cc['value'] <= pedal_lowerb:
                    break
                    
        if pedal_depth:
            pd = max(pedal_depth)
        else:
            pd= pedal_lowerb
        if pd >= pedal_upperb:
            pd = pedal_upperb
        if  pedal_time:
            pt = max(pedal_time) - min(pedal_time)
            if pt < (n['end'] - n['start']):
                pt = n['end'] - n['start']
        else:
            pt = n['end'] - n['start']

        ListofNotes.append({'pitch': n['pitch'], 'duration': n['end'] - n['start'], 'velocity': n['velocity'], 'pedal depth': pd, 'pedal time': pt})
    
    # ! cannot read empty json file
    with open(jsonfile,'r') as load_f:
        load_dict = json.loads(json.load(load_f))
    load_dict[piecename] = ListofNotes        
    with open (jsonfile,'w',encoding='utf-8') as File:
        json.dump(json.dumps(load_dict),File)
        
    return ListofNotes

def main():
    midiFilePath = 'D:\\Academic_work\\00PerfTransfer\\Song\\midi_1\\experiments'
    jsonfile = 'D:\\Academic_work\\00PerfTransfer\\File\\json\\PieceAttr.json'
    files= os.listdir(midiFilePath)
    for File in files:
        piecename = File.split('.')[0]
        if piecename.split('-')[-1] == 'lab':
            pedal_lowerb = 53
            pedal_upperb = 62
        else:
            pedal_lowerb = 60
            pedal_upperb = 70
        midifile = os.path.join(midiFilePath,File)
        ListofNotes = attr(midifile, jsonfile, piecename, pedal_lowerb, pedal_upperb)


if __name__ == "__main__":
    main()
    