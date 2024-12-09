import midi_func as mf
import numpy as np
from midi_func import save_numpy_file
from midi_func import divide_to_beat
import os


save_numpy_file()
d = np.load(r"C:\Users\User\Algeo2\Algeo02-23024\src\backend\audio\window_database.npy", allow_pickle=True).item()
keys = list(d.keys())
# print(keys[29])
# print(d["x (35).mid"])
#     print(i)
for i in d[keys[29]]:
    print(i)