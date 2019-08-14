import pretty_midi as pm
import numpy as np
from functools import reduce


def fix_instrument(ins):
    # This function eliminates the cases where two notes overlap with
    # each other,
    # i.e., for two notes n1, n2, n1_start < n2_start, but n1_end > n2_end

    # Use this function just before writing the midi file.
    # Eg, if you have an pretty_midi.Instrument instance: `ins` ready to write,
    # run `ins = fix_instrument(ins)`, and do the rest.

    def notes2nmat(notes):
        nmat = np.zeros((len(notes), 4))
        for i, n in enumerate(notes):
            nmat[i, 0] = n.start
            nmat[i:, 1] = n.end
            nmat[i:, 2] = n.pitch
            nmat[i:, 3] = n.velocity
        return nmat

    def nmat2notes(nmat):
        notes = []
        for n in nmat:
            start, end, pitch, vel = tuple(n)
            notes.append(pm.Note(int(vel), int(pitch), start, end))
        return notes

    notes_dic = {}
    for n in ins.notes:
        if n.pitch in notes_dic.keys():
            notes_dic[n.pitch].append(n)
        else:
            notes_dic[n.pitch] = [n]

    for key in notes_dic.keys():
        nmat = notes2nmat(notes_dic[key])
        nmat = nmat[nmat[:, 0].argsort()]
        for i in range(nmat.shape[0] - 1):
            nmat[i, 1] = min(nmat[i + 1, 0], nmat[i, 1])
        notes_dic[key] = nmat2notes(nmat)

    notes_fixd = reduce(lambda a, b: a + b, notes_dic.values())
    ins.notes = notes_fixd
    return ins








