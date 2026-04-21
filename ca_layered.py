import numpy as np
import wave, math
W=64; steps=128; sr=44100; bpm=120
beat_dur=60.0/bpm; spb=int(sr*beat_dur); base=55.0
def ca_grid(rule):
    row=np.zeros(W,int); row[W//2]=1; grid=[row.copy()]
    for i in range(steps-1):
        n=np.roll(row,1)*4+row*2+np.roll(row,-1)
        row=np.array([(rule>>int(v))&1 for v in n]); grid.append(row.copy())
    return np.array(grid)
g30=ca_grid(30); g90=ca_grid(90)
audio=np.zeros(spb*steps)
for si,r30 in enumerate(g30):
    r90=g90[si]
    for cj in range(W):
        if r30[cj] or r90[cj]:
            edo=cj%19; freq=base*(2**(edo/19.0))
            t=np.linspace(0,0.08,int(sr*0.08),False)
            amp=0.25 if r30[cj] else 0.15
            decay=30 if r30[cj] else 15
            grain=amp*np.sin(2*math.pi*freq*t)*np.exp(-t*decay)
            if r90[cj] and r30[cj]: grain*=1.4
            s=si*spb; e=s+len(grain)
            if e<=len(audio): audio[s:e]+=grain
audio=audio/max(abs(audio).max(),1e-6)*0.9
out=np.clip(audio*32767,-32767,32767).astype(np.int16)
wf=wave.open('ca_layered_30_90.wav','wb')
wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
wf.writeframes(out.tobytes()); wf.close()
print(f'Layered 30+90: {len(audio)/sr:.1f}s')
