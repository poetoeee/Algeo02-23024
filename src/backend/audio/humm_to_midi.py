import librosa
import mido
import numpy as np

def freq_to_note(frequency):
    return int(round(69 + 12 * (np.log2(frequency/440))))
