import sys
sys.path.insert(0,".")
from fm_synth_engine_v2 import fm_oscillator
import numpy as np,wave,random
SR=44100;A3=220.0
def ef(s):return A3*(2**(s/19.0))
pools={"flowing":[5,6,7,8],"staccato":[4,5,6,7,8],"chaos":[4,5,6,7,8,9,10,11,12,13,14,15,16,17],"lyrical":[4,5,6,7,8,9,10,11],"stillness":[5,6,7,8]}
order=["flowing","staccato","chaos","lyrical","stillness"]
sec_dur=24.0;total=int(5*sec_dur*SR);mx=np.zeros(total)
for si,name in enumerate(order):
 off=int(si*sec_dur*SR);pool=pools[name];nd=int(sec_dur*SR)
 if name=="flowing":
  t=np.arange(nd)/SR;sig=np.zeros(nd)
  for j in range(4):
   s=pool[j%len(pool)];f=ef(s);sig+=0.3*np.sin(2*np.pi*f*t+j)*np.sin(2*np.pi*0.1*t)
  mx[off:off+nd]+=sig
 elif name=="staccato":
  for k in range(48):
   s=pool[k%len(pool)];dur=0.15;st=int(k*sec_dur/48*SR);n=int(dur*SR)
   note=fm_oscillator(ef(s),ef(s)*2,3.0,dur,SR);env=np.exp(-8*np.arange(n)/SR)
   note=note[:n]*env;e=min(st+n,nd);mx[off+st:off+e]+=note[:e-st]*0.5
 elif name=="chaos":
  for k in range(96):
   s=random.choice(pool);dur=0.08+random.random()*0.2;st=int(random.random()*sec_dur*SR);n=int(dur*SR)
   note=fm_oscillator(ef(s),ef(s)*random.uniform(1,4),random.uniform(2,8),dur,SR)
   e=min(st+n,nd);mx[off+st:off+e]+=note[:e-st]*0.3
 elif name=="lyrical":
  t=np.arange(nd)/SR;sig=np.zeros(nd)
  mel=[4,5,6,7,8,9,10,11,10,9,8,7];seg=nd//len(mel)
  for i,s in enumerate(mel):
   env=np.zeros(nd);env[i*seg:min((i+1)*seg,nd)]=0.4
   sig+=env*np.sin(2*np.pi*ef(s)*t)
  mx[off:off+nd]+=sig
 else:
  t=np.arange(nd)/SR;be=0.7+0.3*np.sin(2*np.pi*0.15*t)
  mx[off:off+nd]+=0.6*be*np.sin(2*np.pi*ef(5)*t)
mx=mx/np.max(np.abs(mx))*0.95;o=(mx*32767).astype(np.int16)
wf=wave.open("wave_arc.wav","w");wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(SR);wf.writeframes(o.tobytes());wf.close()
print("T8 Wave Arc:",5*sec_dur,"s",len(o),"samples, 5 sections rendered")
