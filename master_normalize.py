import numpy as np, wave, os, glob

TARGET_RMS = 10000
SRC = '/tmp/max-music-clean'

for f in sorted(glob.glob(os.path.join(SRC, '*.wav'))):
    w = wave.open(f, 'r')
    params = w.getparams()
    d = np.frombuffer(w.readframes(-1), np.int16).astype(np.float64)
    w.close()
    rms = np.sqrt(np.mean(d**2))
    if rms < 1:
        print(f'{os.path.basename(f)} SILENT skip')
        continue
    gain = TARGET_RMS / rms
    d2 = np.clip(d * gain, -32767, 32767).astype(np.int16)
    new_rms = int(np.sqrt(np.mean(d2.astype(float)**2)))
    w2 = wave.open(f, 'w')
    w2.setparams(params)
    w2.writeframes(d2.tobytes())
    w2.close()
    print(f'{os.path.basename(f)} RMS {int(rms)} -> {new_rms} gain {gain:.2f}')
