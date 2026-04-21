import sys
sys.path.insert(0, '.')
from fm_synth_engine_v2 import fm_oscillator, comb_reverb
import numpy as np
import wave

SR = 44100
A3 = 220.0
def edo19_freq(step):
    return A3 * (2 ** (step / 19.0))

starts = [5, 6, 7, 8, 9, 11]
converge_times = [0, 6, 6, 12, 18, 42]
total_dur = 90.0
samples = int(total_dur * SR)
mixed = np.zeros(samples)
for vi, start in enumerate(starts):
    sig = np.zeros(samples)
    ct = int(converge_times[vi] * SR)
    # Pre-convergence: hold starting pitch
    if ct > 0:
        pre = fm_oscillator(edo19_freq(start), edo19_freq(start)*1.0, 0.8, converge_times[vi], SR)
        sig[:len(pre)] = pre
    # Post-convergence: unison step 5 with BREATHING
    post_dur = total_dur - converge_times[vi]
    if post_dur > 0:
        t_post = np.arange(int(post_dur * SR)) / SR
        breath_rate = 0.15 + 0.05 * np.sin(0.02 * t_post)
        breath_env = 0.7 + 0.3 * np.sin(2 * np.pi * breath_rate * t_post)
        mod_breath = 0.5 + 0.4 * np.sin(2 * np.pi * 0.08 * t_post)
        carrier = edo19_freq(5)
        post = fm_oscillator(carrier, carrier*1.0, 0.8, post_dur, SR)
        post = post[:len(breath_env)] * breath_env * mod_breath
        sig[ct:ct+len(post)] = post[:samples-ct]
    fade_in = min(int(2.0 * SR), len(sig))
    sig[:fade_in] *= np.linspace(0, 1, fade_in)
    mixed += sig * (1.0 if start == 11 else 0.7)
mixed = mixed / np.max(np.abs(mixed)) * 0.95
out = (mixed * 32767).astype(np.int16)
wf = wave.open('degenerate_conic.wav', 'w')
wf.setnchannels(1)
wf.setsampwidth(2)
wf.setframerate(SR)
wf.writeframes(out.tobytes())
wf.close()
print(f'T10 Degenerate Conic v2 BREATHING STILLNESS: {total_dur}s, {len(out)} samples')
