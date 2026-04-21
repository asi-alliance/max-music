import numpy as np
from fm_synth_engine_v2 import fm_oscillator, comb_reverb
import wave

sr = 44100
dur = 90
N = sr * dur
e = 0.7
theta = np.linspace(0, 2 * np.pi * 2, N)
r = 1.0 * (1 - e**2) / (1 + e * np.cos(theta))
freq = 220 + 180 * r / r.max()
phase = np.cumsum(freq) / sr
sig = np.sin(2 * np.pi * phase + 1.5 * np.sin(2 * np.pi * phase * 2))
sig = comb_reverb(sig, 90, 0.25, sr)
sig = sig / (np.max(np.abs(sig)) + 1e-9) * 0.8
w = wave.open('ellipse_orbit_fm.wav', 'w')
w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((sig * 32767).astype(np.int16).tobytes())
w.close()
print('ellipse_orbit_fm OK', int(np.sqrt(np.mean(sig**2)) * 32767))
