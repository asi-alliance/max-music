import numpy as np
from fm_synth_engine_v2 import portamento, waveshape, comb_reverb
import wave

sr = 44100
dur = 90
N = sr * dur
pent = [0, 2, 4, 7, 9]
bpm = 80
nsamp = int(sr * 120 / bpm)
segs = N // nsamp + 1
freq_arr = np.zeros(N)
for i in range(segs):
    s = slice(i * nsamp, min((i + 1) * nsamp, N))
    freq_arr[s] = 220 * 2 ** (pent[i % 5] / 12)
freq_arr = portamento(freq_arr, 300)
phase = np.cumsum(freq_arr) / sr
sig = np.sin(2 * np.pi * phase + 1.5 * np.sin(2 * np.pi * phase * 2))
sig = waveshape(sig * 0.7, 1.5)
sig = comb_reverb(sig, 100, 0.25, sr)
sig = sig / (np.max(np.abs(sig)) + 1e-9) * 0.8
w = wave.open('conic_focus.wav', 'w')
w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((sig * 32767).astype(np.int16).tobytes())
w.close()
print('conic_focus OK', int(np.sqrt(np.mean(sig**2)) * 32767))
