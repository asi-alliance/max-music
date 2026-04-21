import json
v = json.load(open('voronoi_19edo.json'))
print('19EDO HARMONIC ENERGY LANDSCAPE')
print('=' * 60)
for x in v:
    n = min(int(x['energy'] / 50), 50)
    b = '#' * n + ' ' * (50 - n)
    m = ' *' if x['energy'] < 50 else ''
    print('step %2d |%s| E=%6.0f  %s%s' % (x['step'], b, x['energy'], x['attractor'], m))
