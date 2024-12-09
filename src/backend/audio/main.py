import midi_func as mf
import numpy as np
from midi_func import save_numpy_file
from midi_func import divide_to_beat
import os
import mido
mid1 = mido.MidiFile(r"C:\Users\User\Algeo2\Algeo02-23024\src\backend\audio\database_song\midi_dataset\x (1).mid")


segments = mf.divide_to_segment(divide_to_beat(mid1))

save_numpy_file()#create np file of window
d = np.load(r"C:\Users\User\Algeo2\Algeo02-23024\src\backend\audio\window_database.npy", allow_pickle=True).item()
keys = list(d.keys())

for key in keys:
    res = 0
    res_all = []
    for window in d[key]:
        if window != []:

            for segment in segments:
                h1, b1 = mf.atb_hist_time_measure(segment)
                h2, b2 = mf.atb_hist_time_measure(window)

                res+= mf.compare(h1, h2)

                h1, b1 = mf.rtb_hist_time_measure(segment)
                h2, b2 = mf.rtb_hist_time_measure(window)

                res+= mf.compare(h1, h2)

                h1, b1 = mf.ftb_hist_time_measure(segment)
                h2, b2 = mf.ftb_hist_time_measure(window)

                res+= mf.compare(h1, h2)
                
                res /= 3
                # print("res",)


                res_all.append(res)

    print(f"hasil dengan {key}:",  np.average(res_all))

        



