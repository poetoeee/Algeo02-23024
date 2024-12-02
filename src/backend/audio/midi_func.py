from mido import MidiFile, tempo2bpm
import numpy as np
import matplotlib.pyplot as plt


mid = MidiFile(r"src\backend\audio\database_song\midi_dataset\x (28).mid")

def get_notes(mid: MidiFile) -> list:
    '''get array of notes from midi object'''    
    
    notes = []
    for i, track in enumerate(mid.tracks):
        if track.name == "Voice":
            print(f"Track: {track.name}")
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

def atb_hist(notes: list):
    '''get histogram of frequency of each tone (note: 0 - 127)'''
    
    h, bins = np.histogram(notes, bins=np.arange(127))

    return h, bins

def rtb_hist(notes: list):
    '''get histogram of tone difference of each succesive note'''
    
    rtb_notes = []

    for i in range(len(notes) - 1):
        diff = notes[i] - notes[i + 1]
        rtb_notes.append(diff)

    h, bins = np.histogram(a= rtb_notes, bins=np.arange(-127, 127))

    return h, bins

def ftb_hist(notes: list):
    '''get histogram of tone difference between note and the first note'''

    ftb_notes = []

    for i in range(len(notes)):
        diff = notes[i] - notes[0]
        ftb_notes.append(diff)

    h, bins = np.histogram(a= ftb_notes, bins=np.arange(-127, 127))

    return h, bins
