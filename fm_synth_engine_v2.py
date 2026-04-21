import numpy as np

def fm_oscillator(freq, mod_freq, mod_depth, duration, sr=44100):
    t = np.linspace(0, duration, int(duration * sr), endpoint=False)
    modulator = mod_depth * np.sin(2 * np.pi * mod_freq * t)
    return np.sin(2 * np.pi * freq * t + modulator)

def comb_reverb(sig, delay_ms=80, decay=0.3, sr=44100):
    delay_samp = int(delay_ms * sr / 1000)
    out = np.copy(sig).astype(np.float64)
    for i in range(delay_samp, len(out)):
        out[i] += decay * out[i - delay_samp]
    return out

def portamento(freq_array, smooth_samples=200):
    k = max(int(smooth_samples), 1)
    kernel = np.exp(-np.arange(k) / k)
    kernel = kernel / kernel.sum()
    return np.convolve(freq_array, kernel, mode='same')

def waveshape(sig, drive=2.0):
    return np.tanh(drive * sig)

def breath_noise(N, density=0.3, gain=0.02):
    noise = np.random.randn(N) * gain
    gate = (np.random.rand(N) < density).astype(np.float64)
    try:
        from scipy.signal import butter, lfilter
        b, a = butter(2, 3000 / 22050, btype='low')
        noise = lfilter(b, a, noise)
    except Exception:
        pass
    return noise * gate
