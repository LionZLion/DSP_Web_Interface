from scipy.fft import fft
from scipy.signal.windows import hamming
import numpy as np


def fft_morse(signal, step=50, size=480, nu=1000, fs=48000):
    """_summary_
    Args:
        path (str): До сигнала в формате .wav или np.array.
        step (int, optional): Шаг окна. Defaults to 50.
        size (int, optional): Размер окна. Должен быть кратным 48 для миниммизации потерь.
        nu (int, optional): Частотата Фурье.
        fs (int, optional): Частота дискретизации. Defaults to 48000.

    Returns:
        morsef (np.array): Возвращает оконный фурье
    """

    morse = signal
    window = hamming(size)
    new_size = (len(morse) - size) // step + 1
    morsef = np.array([])
    new_index = int(nu * size / fs)
    for i in range(new_size):
        transform_s = abs(fft(window * morse[i*step:i*step+size])[new_index])
        morsef = np.hstack([morsef, transform_s])
    
    last_start = i * step
    if len(morse) - last_start > 5:
        last_segment = morse[last_start:]
        len_last = len(last_segment)
        window = hamming(len_last)
        spectrum = abs(fft(window * last_segment))
        last_idx = int(nu * len_last / fs)
        morsef = np.hstack([morsef, spectrum[last_idx]])
        #min-max нормализация
        morsef = (morsef - morsef.min()) / (morsef.max() - morsef.min())
        # morsef = np.log(morsef + 1e-8)
    return morsef

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    plt.plot(fft_morse(r'.\signals\signal_0.wav', step=50, size=960, nu=500, fs=48000))
    plt.show()