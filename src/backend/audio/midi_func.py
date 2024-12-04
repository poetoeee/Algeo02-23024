from mido import MidiFile, tempo2bpm
import numpy as np
from math import sqrt


#(note, beat_length)

def get_notes(mid: MidiFile) -> list:
    '''get array of notes from midi object'''    
    
    notes = []
    for i, track in enumerate(mid.tracks):
        if track.name == "Voice":
            for msg in track:
                if msg.type == "note_on" and msg.velocity > 0:
                    notes.append(msg.note)
            return notes

def note_normalization(notes: list):
    '''normalize pitch of notes'''

    avg = np.average(notes)
    std = np.std(notes)

    norm= []

    for note in notes:
        norm.append(((note - avg) / std).item())
    
    return norm

def atb_hist_count_measure(notes: list):
    '''get histogram of frequency of each tone (note: 0 - 127)'''
    
    h, bins = np.histogram(notes, bins=np.arange(128))

    return h, bins

def atb_hist_time_measure(l: list):
    '''get atb histogram using time (beat) measure
    l: list of tuple (note, beat)
    '''
    beats = np.zeros(128)
    for note, beat in l:
        beats[note] += beat
    x = np.arange(0, 128)
    return beats, x

def rtb_hist_count_measure(notes: list):
    '''get histogram of tone difference of each succesive note'''
    
    rtb_notes = []

    for i in range(len(notes) - 1):
        diff = notes[i] - notes[i + 1]
        rtb_notes.append(diff)

    h, bins = np.histogram(a= rtb_notes, bins=np.arange(-127, 127))

    return h, bins

def rtb_hist_time_measure(l: list):
    '''get histogram of tone difference of each succesive note with beat measure
    l: list of tuple (note, beat)
    '''
    
    beats = np.zeros(255)

    for i in range(len(l) - 1):
        a, b = l[i]
        c, d = l[i + 1]
        diff  = a - c + 127
        beats[diff] += b

    x = np.arange(-127, 127)

    return beats, x


def ftb_hist_count_measure(notes: list):
    '''get histogram of tone difference between note and the first note'''

    ftb_notes = []

    for i in range(len(notes)):
        diff = notes[i] - notes[0]
        ftb_notes.append(diff)

    h, bins = np.histogram(a= ftb_notes, bins=np.arange(-127, 127))

    return h, bins

def ftb_hist_time_measure(l: list):
    '''get histogram of tone difference of each succesive note with beat measure
    l: list of tuple (note, beat)
    '''
    
    beats = np.zeros(255)
    a, b = l[0]

    for i in range(len(l)):
        c, d = l[i]
        diff  = c - a + 127
        beats[diff] += d

    x = np.arange(-127, 127)

    return beats, x

def hist_normalize(notes: list):
    sum = 0
    normal = []
    for note in notes:
        sum += note

    for note in notes:
        normal.append((note/sum).item())

    return normal

def cos_vector(l1: list, l2: list):
    '''get cosinne of two vector with same dimension'''
    dot_product = 0
    norm_l1 = 0
    norm_l2 = 0

    for i in range(len(l1)):
        dot_product += l1[i] * l2[i]
        norm_l1 += l1[i] * l1[i]
        norm_l2 += l2[i] * l2[i]

    norm_l1 = sqrt(norm_l1)
    norm_l2 = sqrt(norm_l2)

    print("dot:", dot_product)

    return dot_product/(norm_l1 * norm_l2)

def divide_to_beat(midi: MidiFile) -> list:
    '''Mengembalikan (a, b), dengan a adalah note dan b adalah jumlah beat saat ini dari awal lagu'''
    
    '''Beat digitung dengan time / ticks_per_beat (time dihitung dalam satuan ticks)'''
    res = []
    beat_count = 0

    for track in midi.tracks:
        if track.name == "Voice":
            for msg in track:
                if msg.type == "note_on":
                    beat_count += msg.time / midi.ticks_per_beat #msg.time dihitung dalam tick
                    res.append((msg.note, beat_count))
    return res

def compare(mid1: MidiFile, mid2: MidiFile):
    note1 = get_notes(mid1)
    note2 = get_notes(mid2)

