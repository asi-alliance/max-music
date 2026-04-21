import wave,numpy as np
target=9500
files=[("conic_focus.wav",1.00),("ellipse_orbit_fm.wav",0.95),("fibonacci_spiral.wav",0.99),("golden_canon.wav",0.96),("hyperbolic_escape.wav",0.95),("lorenz_drift_fm.wav",0.96),("meantone_bridges.wav",0.56),("parabola_trajectory.wav",0.95),("shepard_lindenmayer.wav",1.06),("degenerate_conic.wav",1.74),("wave_arc.wav",2.00)]
for f,g in files:
 w=wave.open(f,"rb")
 n=w.getnframes();d=w.readframes(n);w.close()
 s=np.frombuffer(d,np.int16).astype(float)
 o=np.clip(s*g,-32767,32767).astype(np.int16)
 wf=wave.open(f,"wb");wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(44100);wf.writeframes(o.tobytes());wf.close()
 print(f,"done gain=",g)
print(len(files),"files normalized")
