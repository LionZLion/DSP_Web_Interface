from flask import jsonify, request
from signal_processing.filter import filter_coefficients, filteration, filter_parametr
from signal_processing.TransformSignal import fft_spec, linear_chirp
import numpy as np
from signal_processing.noise import noise_gen
from signal_processing.signal_generator import signal_gen, walsh_function
from signal_processing.impulse import impulse_gen


#Время по T для графика
duration = 1
amplitude = 5

def plot_update():
    #Запрос Стетхема
    data = request.json
    # Извлечение данных
    html_data, signal = signal_update(data)

    if not data.get('num_plot'):
        return jsonify({'error': 'Missing plot number! Check JS file!'})
        
    if data.get('num_plot') in (5, 6):
        type_impulse = data.get('type_impulse', 'fir')
        fs = data.get('fs', 400)
        is_dft = data.get('is_dft', False)
        html_filter, coeff = filter_update(data)
        html_data.update(html_filter)
        
        filtred_signal = filteration(signal, coeff, type_impulse)
        
        html_add = {
            'filtred_signal': filtred_signal.tolist() if not is_dft else fft_spec(fs, filtred_signal)[1].tolist(),
            'signal': signal.tolist() if not is_dft else fft_spec(fs, signal)[1].tolist()
        }
            
        html_data.update(html_add)
    return jsonify(html_data)


def filter_update(data):
    num_plot = data.get('num_plot')
    type_impulse = data.get('type_impulse', 'fir')
    type_iir = data.get('type_iir')
    order = data.get('order', 10)
    cutoff_right = data.get('cut_of_right', 50)
    cutoff_left = data.get('cut_of_left', 10)
    cutoff = [cutoff_left, cutoff_right]
    fs = data.get('fs', 400)
    regime_filter = data.get('regime_filter', 'lowpass')
    type_window = data.get('type_window', 'hamming')

    coeff = filter_coefficients(type_impulse, regime_filter, order, cutoff, fs, type_iir, type_window)
    freq, h_db, phase = filter_parametr(coeff, type_impulse, fs)
    html_data = {
            'num_plot': num_plot,
            'freq': freq.tolist(),
            'h_db': h_db.tolist(),
            'phase': phase.tolist(),
            
        }
    
    return html_data, coeff


def signal_update(data):
    num_plot = data.get('num_plot')
    signal_type = data.get('signal_type', 'sine')
    frequency = data.get('frequency', 20)
    chirp = data.get('is_chirp', False)
    fs = data.get('fs', 400) + 1 # потому что ещё 0
    phase = data.get('phase', 0)
    width = data.get('width')
    period = data.get('period')
    sigma = data.get('sigma', 1)
    sequency = data.get('sequency', 0)
    is_dft = data.get('is_dft', False)
    noise_type = data.get('noise_type', 'white')
    
    t = np.linspace(0, duration, int(duration * fs))
    if chirp:
        k = data.get('chirp_coef')
        frequency = linear_chirp(frequency, k, t)

    if num_plot == 1:
        signal = signal_gen(signal_type, frequency, amplitude, t, phase)
    elif num_plot == 2:
        signal = impulse_gen(signal_type, amplitude, fs, duration, phase, width, period, sigma)
    elif num_plot == 3:
        fs = 128
        signal = walsh_function(fs, sequency)
    elif num_plot == 4:
        signal = noise_gen(duration * fs, sigma, signal_type)
    elif num_plot in (5, 6):
        signal = signal_gen(signal_type, frequency, amplitude, t, phase) + noise_gen(duration * fs, sigma, noise_type)
    
    signal_freq, signal_spectrum = fft_spec(fs, signal)
    
    html_data = {
            'num_plot': num_plot,
            'time': t.tolist() if not is_dft else signal_freq.tolist(),
            'signal': signal.tolist() if not is_dft else signal_spectrum.tolist(),
        }
    
    return html_data, signal