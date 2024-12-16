import librosa
import mido
import numpy as np

# Function to convert frequency (Hz) to the closest MIDI note
def freq_to_midi(frequency):
    return int(round(69 + 12 * np.log2(frequency / 440.0)))

# Function to extract pitch and timing information from the audio
def extract_pitch(audio_file):
    y, sr = librosa.load(audio_file)
    
    # Extract pitch and magnitude using librosa's piptrack
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
    
    # Detect onsets in the audio
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, units='frames')
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    
    pitch_values = []
    times = []
    
    # Extract the most prominent pitch at each onset frame
    for frame in onset_frames:
        index = magnitudes[:, frame].argmax()
        pitch = pitches[index, frame]
        if pitch > 0:
            pitch_values.append(pitch)
            times.append(librosa.frames_to_time(frame, sr=sr))
    
    return pitch_values, times, onset_times

# Function to create a MIDI file from detected pitches and timings
def create_midi(pitches, times, onset_times, midi_file="output.mid"):
    midi = mido.MidiFile()
    track = mido.MidiTrack()
    midi.tracks.append(track)
    
    # Add a tempo event (set to 120 BPM as an example)
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))
    
    prev_time = 0
    
    for i in range(len(pitches)):
        pitch = pitches[i]
        time = times[i]
        
        # Convert pitch to MIDI note
        midi_note = freq_to_midi(pitch)
        
        # Calculate the time delta between the previous onset and the current one
        time_delta = int(librosa.time_to_frames(time - prev_time))  # Convert time difference to frames
        
        # Add 'note_on' event at the current time
        track.append(mido.Message('note_on', note=midi_note, velocity=64, time=time_delta))

        # Calculate the duration of the current note by subtracting the current onset time from the next onset time
        if i + 1 < len(onset_times):
            duration_time = onset_times[i + 1] - time
        else:
            # If it's the last note, use a fixed duration (e.g., 0.5 seconds or a threshold)
            duration_time = 0.5
        
        # Convert the duration from seconds to MIDI ticks
        note_duration = int(librosa.time_to_frames(duration_time))  # Duration in frames
        note_duration = note_duration  # Duration in frames
        
        # Add 'note_off' event with calculated duration
        track.append(mido.Message('note_off', note=midi_note, velocity=64, time=note_duration))
        
        prev_time = time  # Update the previous time for the next note
    
    for i, track in enumerate(midi.tracks):
        
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            print(msg)
    # Save the MIDI file
    midi.save(midi_file)

# # Example usage
# audio_file = "your_humming_audio.wav"  # Path to yo/ur humming audio file
# pitches, times, onset_times = extract_pitch(audio_file)  # Extract pitch, time, and onset info
# create_midi(pitches, times, onset_times, "output.mid")  # Create the MIDI file


# mid2 = mido.MidiFile(r"src\backend\audio\query\x (11).mid")


# for i, track in enumerate(mid2.tracks):
#         # print("tick: ", mid2.ticks_per_beat)
#         # print('Track {}: {}'.format(i, track.name))
#         for msg in track:
#             # print(msg.type)
#             if msg.type == 'note_off':
#                 print(msg)


pitches, times, onset_times = extract_pitch(r"C:\Users\User\Downloads\11_voice.wav")
create_midi(pitches, times, onset_times, midi_file=r"C:\Users\User\Downloads\11_voice.mid")