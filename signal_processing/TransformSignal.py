import numpy as np

def fft_spec(fs, signal):
    N = len(signal)
    freq = np.fft.rfftfreq(N, 1 / fs)  # Частоты
    spectrum_freq = (2 / N) * np.abs(np.fft.rfft(signal))
    return freq, np.round(spectrum_freq, 8)


def linear_chirp(freq0, k, t):
    # k is a chirp rate k = (f1-f0)/T
    return freq0 + k * t / 2


def exponential_chirp(freq0, k, t):
    # делим на t, чтобы можно было подставить в любую формулу
    # k = ln(f1/f0) / T, T - длительность сигнала
    return freq0 * (np.exp(k * t) - 1) / (k  * t)