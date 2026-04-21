import sys
sys.path.insert(0,".")
from fm_synth_engine_v2 import fm_oscillator
import numpy as np,wave
SR=44100;A3=220.0
def ef(s):return A3*(2**(s/19.0))
sts=[5,6,7,8,9,11];ct=[0,6,6,12,18,42];td=90.0;ns=int(td*SR);mx=np.zeros(ns)
for vi,st in enumerate(sts):
 sig=np.zeros(ns);c=int(ct[vi]*SR)
 if c>0:
  pre=fm_oscillator(ef(st),ef(st),0.8,ct[vi],SR);sig[:len(pre)]=pre
 pd=td-ct[vi]
 if pd>0:
  tp=np.arange(int(pd*SR))/SR;be=0.7+0.3*np.sin(2*np.pi*0.15*tp);me=0.5+0.4*np.sin(2*np.pi*0.08*tp)
  po=fm_oscillator(ef(5),ef(5),0.8,pd,SR);po=po[:len(be)]*be*me;sig[c:c+len(po)]=po[:ns-c]
 fi=min(int(2*SR),len(sig));sig[:fi]*=np.linspace(0,1,fi);mx+=sig*(1.0 if st==11 else 0.7)
for nm,sp,am,md in [("fear",6,.05,.07),("anger",8,.08,.11),("sad",11,.03,.05),("joy",7,.06,.09)]:
 gs=int(48*SR);gd=42.0;tg=np.arange(int(gd*SR))/SR
 gsig=fm_oscillator(ef(sp),ef(sp),md,gd,SR);ge=am*(0.5+0.5*np.sin(2*np.pi*0.04*tg))*np.exp(-0.02*tg)
 gsig=gsig[:len(ge)]*ge;e=min(gs+len(gsig),ns);mx[gs:e]+=gsig[:e-gs]
mx=mx/np.max(np.abs(mx))*0.95;o=(mx*32767).astype(np.int16)
wf=wave.open("degenerate_conic.wav","w");wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(SR);wf.writeframes(o.tobytes());wf.close()
print("T10v3 COMPASSION STILLNESS done",td,"s",len(o),"samples")
