import json, numpy as np
from scipy.optimize import linear_sum_assignment

data = json.load(open('transport_costs.json'))
sweet = data['sweet']
C = np.array(data['costs'])
n = len(sweet)
Csub = np.zeros((n,n))
for i in range(n):
    for j in range(n):
        Csub[i][j] = C[sweet[i]][sweet[j]]

# Sinkhorn-Knopp: find optimal coupling between two mass distributions
# Source: uniform mass at all sweet spots
# Target: concentrated at steps 5,6,7 (minor3rd, maj3rd, sept_maj3rd)
src = np.ones(n) / n
tgt = np.zeros(n)
for idx in [1,2,3]:  # indices into sweet array for steps 5,6,7
    tgt[idx] = 1.0/3

epsilon = 50.0  # regularization
K = np.exp(-Csub / epsilon)
u = np.ones(n)
for it in range(200):
    v = tgt / (K.T @ u + 1e-10)
    u = src / (K @ v + 1e-10)
T = np.diag(u) @ K @ np.diag(v)

print('Source: uniform over sweet spots', sweet)
print('Target: concentrated at steps 5,6,7 (home cluster)')
print('Epsilon:', epsilon)
print('\nOptimal transport coupling T[i,j]:')
header = ''.join(f'{sweet[j]:>8d}' for j in range(n))
print(f'{"":>12s}{header}')
for i in range(n):
    row = ''.join(f'{T[i][j]:>8.4f}' for j in range(n))
    print(f'step {sweet[i]:>2d}     {row}')
print(f'\nTotal transport cost: {np.sum(T * Csub):.1f}')
print('\nFlow interpretation: each row shows how mass at that sweet spot distributes to targets.')
print('High T[i,j] = strong flow from step i toward step j.')
json.dump({'coupling': T.tolist(), 'sweet': sweet, 'cost': float(np.sum(T*Csub))}, open('sb_coupling.json','w'))
print('Saved sb_coupling.json')
