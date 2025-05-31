from flask import jsonify, request
import numpy as np
from signal_processing.neural import morse_processing, morse_numpy

def plt_fft():
    #Запрос Стетхема
    data = request.json
    # Извлечение данных
    html_data = signal_update(data)
    return jsonify(html_data)


def signal_update(data):
    sigma = data.get('sigma', 2)
    phrase = data.get('phrase', '').strip()
    
    prp = {
        'dt': 2000,
        'nu': 1000,
        'fs': 48000,
        'step': 50,
        'size': 480,
    }
    
    phrase_stft = morse_numpy(phrase, prp, sigma)
    duration = len(phrase_stft) / prp['fs'] * prp['step']
    t = np.linspace(0, duration, int(len(phrase_stft)))
    
    if phrase == '':
        encrypt = ''
        if sigma == 0:
            phrase_stft = np.zeros(len(t))
    else:
        encrypt = morse_processing(phrase_stft)
    
    html_data = {
            'time': t.tolist(),
            'signal': phrase_stft.tolist(),
            'encrypt': encrypt
        }
    return html_data

if __name__ == '__main__':
    test_data = {
        'phrase': 'Привет',
        'sigma': 0.5
    }
    print(signal_update(test_data))
    # Вывод: {'time': [...], 'signal': [...], 'encrypt': [...]}