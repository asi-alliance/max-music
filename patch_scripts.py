import os
os.chdir('/tmp/max-music-clean')
scripts=['make_golden_canon.py','make_degenerate_conic.py','make_hyperbolic_escape.py','make_parabola_trajectory.py','make_meantone_bridges.py']
header='import os\nos.chdir(os.path.dirname(os.path.abspath(__file__)))\n'
for s in scripts:
    if os.path.exists(s):
        c=open(s).read()
        if 'os.chdir' not in c:
            open(s,'w').write(header+c)
            print('PATCHED',s)
        else:
            print('ALREADY',s)
    else:
        print('MISSING',s)
