import sys
sys.path.insert(0, '.')
from poly_renderer import render_voice, mix_voices, save_wav, edo19_freq
import numpy as np

SR = 44100
# T10 Degenerate Conic - STILLNESS
# 6 voices start at [5,6,7,8,9,11], converge cheapest-first to unison 5
# Convergence order: 5(already),6(cost10.2),7(10.2),8(11.4),9(32.4),11(392.8)
# Each voice holds its starting pitch then glides to 5 at its convergence time
# Total duration ~48s, 8 steps of 6s each

starts = [5, 6, 7, 8, 9, 11]
converge_step = [0, 1, 1, 2, 3, 7]  # step index when each voice joins unison
total_steps = 8
dur = 6.0

voices = []
for vi, start in enumerate(starts):
    steps = []
    for t in range(total_steps):
        if t >= converge_step[vi]:
            steps.append(5)
        else:
            steps.append(start)
    sig = render_voice(steps, dur_per_step=dur, mod_index=0.8, fade_in=2.0, fade_out=4.0)
    voices.append(sig * (0.7 if start != 11 else 1.0))

mixed = mix_voices(voices)
save_wav('degenerate_conic.wav', mixed)
print('T10 Degenerate Conic rendered - Stillness')
