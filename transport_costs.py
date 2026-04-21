import json, numpy as np
v = json.load(open('voronoi_19edo.json'))
E = [x['energy'] for x in v]
n = len(E)
C = np.zeros((n,n))
for i in range(n):
    for j in range(n):
        if i==j: continue
        fwd = list(range(i,j+1)) if j>i else list(range(i,n))+list(range(0,j+1))
        bwd = list(range(j,i+1)) if i>j else list(range(j,n))+list(range(0,i+1))
        C[i][j] = min(max(E[k] for k in fwd), max(E[k] for k in bwd))
sweet = [x['step'] for x in v if x['energy']<50]
print('Sweet spots:', sweet)
print('Transport cost matrix (sweet spots only):')
for si in sweet:
    row = ' '.join(f'{C[si][sj]:6.0f}' for sj in sweet)
    print(f'  step {si:2d} ({v[si]["attractor"]:>20s}): {row}')
pairs = sorted([(C[si][sj],v[si]['attractor'],v[sj]['attractor'],si,sj) for i,si in enumerate(sweet) for sj in sweet[i+1:]])
print('\nCheapest modulations:')
for c,a,b,si,sj in pairs[:8]: print(f'  {a:>20s} <-> {b:<20s} saddle={c:.0f}')
print('\nCostliest modulations:')
for c,a,b,si,sj in pairs[-5:]: print(f'  {a:>20s} <-> {b:<20s} saddle={c:.0f}')
json.dump({'sweet':sweet,'costs':C.tolist()},open('transport_costs.json','w'))
print('Saved transport_costs.json')
