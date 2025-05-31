'''
Коэффициенты для циврового фильтра - отдельная задача, которая
призвана прежде всего удовлетворить любителей ТФКП
Самые базовые можно найти в пакете scipy.signal
'''
from scipy.signal import firwin, freqz, iirfilter, freqz_sos, sosfilt, sosfiltfilt
import numpy as np


def filteration(signal, coefficients, impulse_type, phase=0):
    if impulse_type == 'fir':
        """
        Реализовано через свёртку
        """
        filtred_signal = np.convolve(signal, coefficients, mode='same') 
    elif impulse_type == 'iir':
        """
        Нельзя реализовать при помощи свёртки в полном объёме, лучше использовать
        готовые приближения, такие уже реализованы в пакете scipy.signal
        Здесь фильтр представлен в виде фильтров второго порядка, сделано это,
        потому что для порядках фильтра более 10, наблюдаются проблемы вычисления.
        Поэтому коэффициенты в формате 'sos'
        """ 
        if phase:
            filtred_signal = sosfiltfilt(coefficients, signal)
        else:
            filtred_signal = sosfilt(coefficients, signal)
    else:
        raise ValueError("3rd argument must be 'iir' or 'fir'!")
    
    return np.round(filtred_signal, 8)


def filter_coefficients(type_f, filter_regime, order, cutoff, fs, type_iir, type_window):
    """
    length = длина фильтра
    cutoff - частота среза
    fs - частота дискретизации
    filter_regime - 
    """
    if type_f == 'fir':
        order += 1
        
    if filter_regime == 'lowpass':
        cutoff = cutoff[1]
    elif filter_regime == 'highpass':
        order |= 1
        cutoff = cutoff[0]
    elif filter_regime == 'bandpass' or filter_regime == 'bandstop':
        if cutoff[0] == cutoff[1]:
            cutoff[0] = cutoff[0] - 0.00001
        cutoff = [min(cutoff), max(cutoff)]
    
    if filter_regime == 'bandstop':
        order |= 1

    
    if type_f == "fir":
        coeff = firwin(order, cutoff, window=type_window, pass_zero=filter_regime, scale=True, fs=fs)
    elif type_f == "iir":
        coeff = iirfilter(order, cutoff, btype=filter_regime, ftype=type_iir, rp=5, rs=60, fs=fs, output='sos')
    else:
        raise ValueError("3rd argument must be 'iir' or 'fir'!")

    return coeff


def filter_parametr(coeff, type_f, fs):
    if type_f == 'fir':
        w, h = freqz(coeff)
    elif type_f == 'iir':
        w, h = freqz_sos(coeff)
    else:
        raise ValueError("3rd argument must be 'iir' or 'fir'!")
    h_db = 20 * np.log10(np.maximum(abs(h), 1e-10))
    freq = w * fs /(2 * np.pi)
    phase = np.unwrap(np.angle(h))
    return freq, np.round(h_db, 8) , np.round(phase, 8)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from scipy.signal import get_window

    fs = 48000
    order = 1
    cutoff = [10000, 15000]
    type_f = 'fir'
    type_iir = 'butter'
    type_window = 'boxcar'
    filter_regime = 'lowpass'

    coeff = filter_coefficients(type_f, filter_regime, order, cutoff, fs, type_iir, type_window)
    freq, h_db, phase = filter_parametr(coeff, type_f, fs)
    plt.plot(freq, h_db)
    plt.show()