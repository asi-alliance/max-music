import json, numpy as np
data = json.load(open('transport_costs.json'))
sweet = data['sweet']
C = np.array(data['costs'])
n = len(sweet)
Csub = np.zeros((n,n))
for i in range(n):
    for j in range(n):
        Csub[i][j] = C[sweet[i]][sweet[j]]

# v2: source = home cluster (steps 5,6,7,8), target = distant keys (0,11,14,16)
home = [1,2,3,4]  # indices into sweet for steps 5,6,7,8
dist = [0,5,6,7]  # indices into sweet for steps 0,11,14,16
src = np.zeros(n)
for i in home: src[i] = 0.25
tgt = np.zeros(n)
for i in dist: tgt[i] = 0.25

for eps in [5, 10, 20, 50]:
    K = np.exp(-Csub / eps)
    u = np.ones(n)
    for it in range(500):
        v = tgt / (K.T @ u + 1e-12)
        u = src / (K @ v + 1e-12)
    T = np.diag(u) @ K @ np.diag(v)
    cost = np.sum(T * Csub)
    print(f'\nEpsilon={eps}  Total cost={cost:.1f}')
    for i in range(n):
        if src[i] > 0:
            flows = [(sweet[j], T[i][j]) for j in range(n) if T[i][j] > 0.001]
            flows.sort(key=lambda x: -x[1])
            fstr = ', '.join(f'step{s}:{w:.3f}' for s,w in flows)
            print(f'  step{sweet[i]:2d} -> {fstr}')

json.dump({'coupling': T.tolist(), 'sweet': sweet, 'epsilon': 5}, open('sb_coupling_v2.json','w'))
print('\nSaved sb_coupling_v2.json (eps=5)')
