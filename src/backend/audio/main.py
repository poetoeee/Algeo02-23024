import midi_func as mf
import numpy as np
import os
import mido

def main():
    # mf.save_numpy_file()
    res_dict = {}
    res = []
    humm = mido.MidiFile(r"C:\Users\User\Algeo2\Algeo02-23024\src\backend\audio\humming\x (2).mid")

    humm_windows = mf.create_windows(mf.divide_to_beat(humm))

    # save_numpy_file()#create np file of window
    d = np.load(r"C:\Users\User\Algeo2\Algeo02-23024\src\backend\audio\window_database.npy", allow_pickle=True).item()
    keys = list(d.keys())

    for key in keys:
        res_song = 0
        for humm_window in humm_windows:
            for window in d[key]:
                res_window = []
                ###TIME MEASURE
                h1, b1 = mf.atb_hist_time_measure(humm_window)
                h2, b2 = mf.atb_hist_time_measure(window)
                res_window.append(mf.compare(h1, h2))

                

                h1, b1 = mf.rtb_hist_time_measure(humm_window)
                h2, b2 = mf.rtb_hist_time_measure(window)
                res_window.append(mf.compare(h1, h2))

                
                h1, b1 = mf.ftb_hist_time_measure(humm_window)
                h2, b2 = mf.ftb_hist_time_measure(window)
                res_window.append(mf.compare(h1, h2))

                ###COUNT MEASURE
                h1, b1 = mf.rtb_hist_count_measure([note for note, b in humm_window])
                h2, b2 = mf.rtb_hist_count_measure([note for note, b in window])
                res_window.append(mf.compare(h1, h2))

                
                h1, b1 = mf.ftb_hist_count_measure([note for note, b in humm_window])
                h2, b2 = mf.ftb_hist_count_measure([note for note, b in window])
                res_window.append(mf.compare(h1, h2))
                
                avg_window = sum(res_window)/len(res_window)

                if avg_window > res_song:
                    res_song = avg_window
                        

        print(f"hasil dengan {key}:",  avg_window)
        res_dict[key] = avg_window

    d2  = {k: v for k, v in sorted(res_dict.items(), key=lambda item: item[1], reverse=True)}
    for k in d2.keys():
        print(f"{k}, {res_dict[k].item()}")
    return res_dict
            


main()

