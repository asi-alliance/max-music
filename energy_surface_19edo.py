import numpy as np
import json

# 19EDO pitch classes: step -> cents
steps = np.arange(19)
cents = steps * (1200.0 / 19)

# JI targets with prime limits and cents values
# Format: (name, cents, prime_limit, tenney_weight)
ji_targets = [
    ('unison', 0.0, 1, 0.0),
    ('minor3rd_6:5', 315.64, 5, np.log2(30)),
    ('major3rd_5:4', 386.31, 5, np.log2(20)),
    ('fourth_4:3', 498.04, 3, np.log2(12)),
    ('fifth_3:2', 701.96, 3, np.log2(6)),
    ('major6th_5:3', 884.36, 5, np.log2(15)),
    ('minor7th_9:5', 1017.60, 5, np.log2(45)),
    ('septimal_maj3rd_9:7', 435.08, 7, np.log2(63)),
    ('septimal_min3rd_7:6', 266.87, 7, np.log2(42)),
    ('harmonic7th_7:4', 968.83, 7, np.log2(28)),
    ('tritone_7:5', 582.51, 7, np.log2(35)),
    ('octave', 1200.0, 1, 0.0),
]

# Energy: minimum weighted deviation to nearest JI target
def energy(c):
    min_e = float('inf')
    for name, jc, plim, tenney in ji_targets:
        dev = min(abs(c - jc), 1200 - abs(c - jc))  # circular
        w = 1.0 / (1.0 + tenney)  # lower Tenney = stronger attractor
        e = w * dev**2
        if e < min_e:
            min_e = e
    return min_e

# Compute energy for continuous cents and 19EDO discrete points
cont_cents = np.linspace(0, 1200, 1200)
cont_energy = np.array([energy(c) for c in cont_cents])
edo_energy = np.array([energy(c) for c in cents])

# Find Voronoi assignments (nearest JI attractor per 19EDO step)
voronoi = []
for c in cents:
    best = min(ji_targets, key=lambda t: min(abs(c-t[1]), 1200-abs(c-t[1])))
    voronoi.append({'step': int(c/63.16+0.01), 'cents': round(float(c),1), 'attractor': best[0], 'dev': round(min(abs(c-best[1]),1200-abs(c-best[1])),2), 'energy': round(energy(c),1)})

for v in voronoi:
    print(f"step {v['step']:2d} ({v['cents']:6.1f}c) -> {v['attractor']:20s} dev={v['dev']:5.1f}c  E={v['energy']:8.1f}")

print(f"\nEnergy range: {min(edo_energy):.1f} - {max(edo_energy):.1f}")
print(f"Sweet spots (E<50): {[v['step'] for v in voronoi if v['energy']<50]}")
print(f"Tension peaks (E>5000): {[v['step'] for v in voronoi if v['energy']>5000]}")

json.dump(voronoi, open('voronoi_19edo.json','w'), indent=2)
print('Saved voronoi_19edo.json')
