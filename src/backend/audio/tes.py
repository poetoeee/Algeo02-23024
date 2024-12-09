from mido import MidiFile, tempo2bpm, tick2second
import midi_func
import numpy as np
import matplotlib.pyplot as plt
import os
import time

directory_in_str = r"C:\Users\User\Algeo2\Algeo02-23024\src\backend\audio\database_song\midi_dataset"

mid1 = MidiFile(r"src\backend\audio\database_song\midi_dataset\kelas2.mid")#32
mid2 = MidiFile(r"src\backend\audio\database_song\midi_dataset\x (35).mid")

print(midi_func.calculate_time_measure(mid1, mid2, 0))
# print(midi_func.divide_to_beat(mid2))
# event1 = midi_func.divide_to_beat(mid2)
# print(event1)
# window1 =   [(64, 0.25), (64, 0.25), (64, 0.25), (65, 0.5), (65, 0.25), (65, 0.25), (64, 0.25), (64, 0.25)]
# window2 =  [(66, 0.08333333333333333), (66, 0.3333333333333333), (69, 0.16666666666666666), (69, 0.3333333333333333), (66, 2.5), (66, 0.3333333333333333), (69, 0.25), (69, 0.08333333333333333)]


# res = midi_func.calculate_count_measure(mid1, mid2, 1)
# print(sorted(res))

# print("cos count: ", cosc)
# print("cos time", cost)

# startp = time.time()
# for file in os.listdir(directory_in_str):
#     start =time.time()
#     filename = os.path.join(directory_in_str, file)
#     res = []
#     mid2 = MidiFile(filename)
#     for i in range(3):
#         calc = midi_func.calculate_time_measure(mid1, mid2, i)
#         res.append(calc)
#         if i != 0:
#             calc = midi_func.calculate_count_measure(mid1, mid2, i)
#             res.append(calc)
#         # print(f"calc {i}: ", calc)
#     print(f"Hasil dengan {file} = ", res)
#     print("time taken: ", time.time() - start)

# print("total: ", time.time() - startp)

# res = midi_func.calculate(mid1, mid2, 1)

# print(res)
# event2 = midi_func.divide_to_beat(mid2)

# print(midi_func.divide_to_beat(mid1))


# def beat_lenth(event):
#     sum = 0
#     for a, b in event:
#         sum += b
#     print("sum:",sum)

# beat_lenth(event1)

# segments1 = midi_func.divide_to_segment(event1)
# segments2 = midi_func.divide_to_segment(event2)

# res = midi_func.calculate(segments1, segments2)
# print(sorted(res, reverse=True))
# print("max: ", max(res))


# a, c = midi_func.ftb_hist_count_measure(notes)

# print("count:")
# print(a)
# print(c)

# event = midi_func.divide_to_beat(mid)

# print("time:")
# h, b = midi_func.ftb_hist_time_measure(event)

# print(h)
# print(b)



# h1, b1 = midi_func.ftb_hist_time_measure(event1)
# h2, b2 = midi_func.ftb_hist_time_measure(event2)

# res= midi_func.compare(h1, h2)

# print(res)