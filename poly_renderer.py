import numpy as np
import wave
import sys
sys.path.insert(0, '.')
from fm_synth_engine_v2 import fm_oscillator, comb_reverb, breath_noise, waveshape, portamento

A3 = 220.0
SR = 44100

def edo19_freq(step):
    return A3 * (2 ** (step / 19.0))

def render_voice(step_sequence, dur_per_step=4.0, mod_index=1.5, fade_in=0.0, fade_out=0.0):
    out = np.zeros(0)
    for s in step_sequence:
        freq = edo19_freq(s)
        sig = fm_oscillator(freq, freq * 1.0, mod_index, dur_per_step, SR)
        out = np.concatenate([out, sig])
    if fade_in > 0:
        n = int(fade_in * SR)
        out[:n] *= np.linspace(0, 1, n)
    if fade_out > 0:
        n = int(fade_out * SR)
        out[-n:] *= np.linspace(1, 0, n)
    return out

def mix_voices(voices):
    maxlen = max(len(v) for v in voices)
    mixed = np.zeros(maxlen)
    for v in voices:
        mixed[:len(v)] += v
    return mixed / len(voices)

def save_wav(filename, sig):
    sig = sig / np.max(np.abs(sig)) * 0.95
    samples = (sig * 32767).astype(np.int16)
    wf = wave.open(filename, 'w')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    wf.writeframes(samples.tobytes())
    wf.close()
    print(f'Wrote {filename} {len(samples)} samples {len(samples)/SR:.1f}s')
