from mido import MidiFile, tempo2bpm
import numpy as np
from math import sqrt
import os


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
        
        elif track.name == "Lead":
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
        normal.append((note/sum))

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
    if (norm_l1 * norm_l2 == 0):
        return 0

    return dot_product/(norm_l1 * norm_l2)

def divide_to_beat(midi: MidiFile) -> list:
    '''Mengembalikan list of (a, b), dengan a adalah note dan b adalah jumlah beat saat ini dari awal lagu'''
    
    '''Beat digitung dengan time / ticks_per_beat (time dihitung dalam satuan ticks)'''
    res = []
    beat_count = 0
    tpb = midi.ticks_per_beat
    for track in midi.tracks:
        if track.name == "Voice":
            for msg in track:
                if msg.type == "note_on" or msg.type == "note_off":
                    if msg.time > 0:
                        beat_count = msg.time / tpb #msg.time dihitung dalam tick
                        res.append((msg.note, beat_count))
            return res
        
        elif track.name == "Lead":
            for msg in track:
                if msg.type == "note_on" or msg.type == "note_off":
                    if msg.time > 0:
                        beat_count = msg.time / tpb #msg.time dihitung dalam tick
                        res.append((msg.note, beat_count))
            return res
        
    return res

def divide_to_segment(events: list):
    '''Membagi list menjadi beberapa list yang masing masing segmen terdiri dari 20 - 40 beat
    events: list of tuple (note, beat)

    Menghasilkan list of list of tuple (note, beat)
    '''

    res = []
    temp = []
    beat_count = 0

    for note, beat in events:
        if beat_count < 20:
            temp.append((note, beat))
            beat_count += beat
        else:
            res.append(temp)
            temp = []
            beat_count = 0
    if beat_count != 0:
        res.append(temp)
    return res

def compare(h1, h2):
    '''
    compare two histogram using cosine
    h1: list of int (histogram 1)
    bins1: list of int (bins 1)
    h2: list of int (histogram 2)
    bins2: list of int (bins 2)
    '''

    cos_res = cos_vector(h1, h2)
    return cos_res


def create_windows(events):    
    is_window = False
    window_size = 20
    sliding_window = 4    
    windows = []
    window = []
    idx = 0
    beat_count = 0

    deque_count = 0
    window = []

    while idx < len(events):

        n, b = events[idx]
        if not is_window:
            window.append(events[idx])
            beat_count += b
            
            if beat_count > window_size:
                is_window = True
            idx += 1

        else:
            if window == []:
                is_window = False
            else:

                windows.append(window[:])
                
                while deque_count < sliding_window:
                    n, first_beat = window[0]
                    deque_count += first_beat
                    beat_count -= first_beat
                    window.pop(0)
                    if window == []:
                        break

                is_window = False
                deque_count = 0
    if window != []:
        windows.append(window[:])

    return windows

def save_numpy_file():
    '''
    Membuat file numpy berisikan dict (key= nama lagu, value = array of array of window)
    '''
    current_directory = os.path.dirname(os.path.realpath(__file__))
    directory_in_str = os.path.join(current_directory, "database_song", "midi_dataset")
    database = {}

    window_size = 20
    sliding_window = 4
    for file in os.listdir(directory_in_str):
        print(file)
        filename = os.path.join(directory_in_str, file)
        mid = MidiFile(filename)
        
        events = divide_to_beat(mid)

        windows = create_windows(events)
        
        database[file] = windows[:]

    f = os.path.join(current_directory, "window_database")
    np.save(f, database)
    print("database saved")





def calculate_time_measure(mid1: MidiFile, mid2: MidiFile, feature: int):
    '''
    Membandingkan 2 list of tuple (note, beat).
    feature = 1: atb
    feature = 2: rtb
    feature = 3: ftb

    '''
    event1 = divide_to_beat(mid1)
    event2 = divide_to_beat(mid2)
    if event1 == [] or event2 == []:
        return -1
    segments1 = divide_to_segment(event1)
    segments2 = divide_to_segment(event2)


    res = -1
    window1 = []
    window2 = []
    window_size = 8
    for segment1 in segments1:
        for segment2 in segments2:
            for i in range(len(segment1) - window_size):
                if window1 == []:
                    window1 = segment1[:window_size]
                else:
                    window1.pop(0)
                    window1.append(segment1[i + window_size - 1])

                if feature == 0:
                    h1, b1 = atb_hist_time_measure(window1)
                elif feature == 1:
                    h1, b1 = rtb_hist_time_measure(window1)
                else:
                    h1, b1 = ftb_hist_time_measure(window1)

                h1 = hist_normalize(h1)
                window2 = []

                for j in range(len(segment2) - window_size):                    
                    if window2 == []:
                        window2 = segment2[:window_size]
                    else:
                        window2.pop(0)
                        window2.append(segment2[j + window_size - 1])

                    if feature == 0:
                        h2, b2 = atb_hist_time_measure(window2)
                        
                    elif feature == 1:
                        h2, b2 = rtb_hist_time_measure(window2)

                    else:
                        h2, b2 = ftb_hist_time_measure(window2)

                    h2 = hist_normalize(h2)
                    

                    kemipiran = compare(h1, h2)
                    # print("kemiripan: ", kemipiran)

                    if res < kemipiran.item():
                        res = kemipiran.item()

                    if kemipiran > 0.9:
                        return res
    return res


    
def calculate_count_measure(mid1: MidiFile, mid2: MidiFile, feature: int):
    '''
    Membandingkan 2 list of tuple (note, beat).
    feature = 1: atb
    feature = 2: rtb
    feature = 3: ftb

    '''
    event1 = divide_to_beat(mid1)
    event2 = divide_to_beat(mid2)
    if event1 == [] or event2 == []:
        return -1

    segments1 = divide_to_segment(event1)
    segments2 = divide_to_segment(event2)


    res = -1
    window1 = []
    window2 = []
    window_size = 8
    for segment1 in segments1:
        for segment2 in segments2:
            for i in range(len(segment1) - window_size):
                if window1 == []:
                    window1 = segment1[:window_size]
                    window1 = [a for a, b in window1]
                else:
                    window1.pop(0)
                    a, b = segment1[i + window_size - 1]
                    window1.append(a)

                if feature == 0:
                    h1, b1 = atb_hist_count_measure(window1)
                elif feature == 1:
                    h1, b1 = rtb_hist_count_measure(window1)
                else:
                    h1, b1 = ftb_hist_count_measure(window1)

                h1 = hist_normalize(h1)
                window2 = []

                for j in range(len(segment2) - window_size):                    
                    if window2 == []:
                        window2 = segment2[:window_size]
                        window2 = [a for a, b in window2]
                    else:
                        window2.pop(0)
                        a, b = segment2[j + window_size - 1]
                        window2.append(a)

                    if feature == 0:
                        h2, b2 = atb_hist_count_measure(window2)

                    elif feature == 1:
                        h2, b2 = rtb_hist_count_measure(window2)

                    else:
                        h2, b2 = ftb_hist_count_measure(window2)

                    h2 = hist_normalize(h2)
                    

                    kemipiran = compare(h1, h2)
                    # print("kemiripan: ", kemipiran)

                    if kemipiran.item() > res:
                        res = kemipiran.item()

                    if kemipiran > 0.9:
                        return res
    return res
