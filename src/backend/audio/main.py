import audio.midi_func as mf
import numpy as np
import os
import mido

def handle_query_audio(query: str):
    res_dict = {}
    res = []
    humm = mido.MidiFile(query)

    humm_windows = mf.create_windows(mf.divide_to_beat(humm))

    dir = os.path.join(r"src/backend/audio/window_database.npy")
    d = np.load(dir, allow_pickle=True).item()
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
                        

        res_dict[key] = avg_window
    

    d2  = {k: v for k, v in sorted(res_dict.items(), key=lambda item: item[1], reverse=True)}
    limited_res = {}
    for k in d2.keys():
        if d2[k] > 0.7:
            limited_res[k] = d2[k]

    return limited_res

def procces_audio_db(path):

    mf.save_numpy_file(path)