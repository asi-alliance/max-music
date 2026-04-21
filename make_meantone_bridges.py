import numpy as np
import json, wave, struct, sys
sys.path.insert(0, '/tmp/max-music-clean')
from fm_synth_engine_v2 import fm_oscillator, comb_reverb, waveshape, breath_noise

sr = 44100
data = json.load(open('track7_arc_v2.json'))
arc = data['arc']
C = np.array(json.load(open('transport_costs.json'))['costs'])

def edo19_freq(step, base=220):
    return base * 2 ** (step / 19)

def render_section(steps, sec_dur=12.0):
    note_dur = sec_dur / len(steps)
    out = np.zeros(0)
    for i in range(len(steps)):
        s = steps[i]
        freq = edo19_freq(s)
        cost = C[steps[max(0,i-1)]][s] if i > 0 else 0
        mod_depth = 0.5 + min(cost / 300, 8.0)
        mod_freq = freq * (1.0 + cost / 500)
        sig = fm_oscillator(freq, mod_freq, mod_depth, note_dur, sr)
        env = np.ones(len(sig))
        atk = int(0.05 * sr)
        rel = int(0.15 * sr)
        env[:atk] = np.linspace(0, 1, atk)
        env[-rel:] = np.linspace(1, 0, rel)
        sig = sig * env
        if cost > 100:
            sig = waveshape(sig, drive=1.0 + cost / 200)
        out = np.concatenate([out, sig])
    return out

full = np.zeros(0)
for name, steps in arc:
    print(f'Rendering {name}: {steps}')
    full = np.concatenate([full, render_section(steps)])

full = comb_reverb(full, delay_ms=60, decay=0.25)
bn = breath_noise(len(full), density=0.2, gain=0.01)
full = full + bn
full = full / np.max(np.abs(full)) * 0.95
samples = (full * 32767).astype(np.int16)

wf = wave.open('meantone_bridges.wav', 'w')
wf.setnchannels(1)
wf.setsampwidth(2)
wf.setframerate(sr)
wf.writeframes(samples.tobytes())
wf.close()
print(f'Wrote meantone_bridges.wav {len(samples)} samples {len(samples)/sr:.1f}s')