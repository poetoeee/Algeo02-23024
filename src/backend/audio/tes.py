from mido import MidiFile
import midi_func
import matplotlib.pyplot as plt


mid = MidiFile(r"src\backend\audio\database_song\midi_dataset\x (2).mid")

# plt.title("Hist normal")
notes = midi_func.get_notes(mid)
a, b = midi_func.ftb_hist(notes)
print(a)
print(midi_func.hist_normalize(a))


# plt.bar(x=b[:-1], height=a)
# plt.show()
