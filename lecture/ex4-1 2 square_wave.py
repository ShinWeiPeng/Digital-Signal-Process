import numpy as np
import wave
import struct
import scipy.signal as signal

file = "aquare.wav"

amplitude = 30000
frequency = 100
duration = 3
fs = 44100
num_samples = fs * duration

num_channels = 1
sampwidth = 2
num_frames = num_samples
comptype = "NONE"
compname = "not compressed"

t = np.linspace(0 , duration, num_frames, endpoint = False)
x = amplitude * signal.square(2 *np.pi * frequency * t)

wav_file = wave.open(file, 'w')
wav_file.setparams((num_channels, sampwidth, fs, num_frames, comptype, compname))

for s in x:
    wav_file.writeframes(struct.pack('h', int(s)))
    
wav_file.close()
