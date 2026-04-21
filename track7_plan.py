import json, numpy as np
data = json.load(open('transport_costs.json'))
sweet = data['sweet']
C = np.array(data['costs'])

# Track 7 MEANTONE BRIDGES modulation arc
# ABA form using tritone-as-pivot insight from SB flow v2
# A section: home cluster steps 5,6 (minor3rd, maj3rd) — warm consonance
# Bridge: step 5->8->9 (fourth->tritone) — energy-minimal modulation outward
# Climax: step 9->11 (tritone->fifth) — crossing medium-tier barrier (eps>=10)
# B section: step 11 territory (fifth) — tension plateau
# Return: step 11->9->8->6->5 — reverse the SB flow path back home
# Coda: step 5->0 (minor3rd->unison) — maximum diffusion resolution

arc = [
    ('A1', [5,6,5,6,5], 'warm thirds oscillation'),
    ('A2', [5,6,7,6,5], 'extend to septimal, pull back'),
    ('bridge_out', [5,8,9,8,9], 'fourth->tritone gateway'),
    ('climax', [9,11,9,11], 'tritone-fifth tension'),
    ('B', [11,14,11,16,11], 'fifth explores 6th and 7th'),
    ('bridge_back', [11,9,8,7,6], 'reverse flow home'),
    ('A_return', [6,5,6,5], 'home cluster resolution'),
    ('coda', [5,4,0], 'dissolve through neutral3rd to unison'),
]

print('TRACK 7 MEANTONE BRIDGES — MODULATION ARC')
print('='*55)
total_cost = 0
for name, steps, desc in arc:
    seg_cost = sum(C[steps[i]][steps[i+1]] for i in range(len(steps)-1))
    total_cost += seg_cost
    print(f'{name:>14s}: {str(steps):>20s}  cost={seg_cost:>7.0f}  {desc}')
print(f'\nTotal modulation cost: {total_cost:.0f}')
print('\nSB-optimal: lowest cost path follows energy valleys')
print('Dramatic cost: bridge_out+climax should be ~40pct of total')

json.dump({'arc': arc, 'total_cost': total_cost}, open('track7_arc.json','w'), default=str)
print('Saved track7_arc.json')
