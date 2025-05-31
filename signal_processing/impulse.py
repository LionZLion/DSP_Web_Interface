import numpy as np

np.random.seed(42)


def impulse_gen(signal_type, amplitude, fs, duration, phase, width=0.1, period=0.2, sigma=0.1):
    N = int(duration * fs)
    signal = np.zeros(N)
    if signal_type == "delta":
        signal[int(phase * (fs-1))] = amplitude
    
    elif signal_type == 'square':
        signal = [
            amplitude if phase * fs <= i <= (width + phase) * fs
            else 0 for i in range(N)
            ]
        return np.array(signal)
    
    elif signal_type == 'gauss':
        signal = [
            amplitude * np.exp(-((i - phase*fs) / (sigma*fs)) ** 2 / 2)
            for i in range(N)
            ]
    
    elif signal_type == 'exponent':
        #tau - коэффициент затухания
        signal = [
            amplitude * np.exp(-(int(i - phase*fs)) / (sigma* fs)) 
            if i >= phase*fs else 0 for i in range(N)
            ]
    
    elif signal_type == 'pulse_train':
        a = int(duration*100)
        b = int(period*100)
        for n in range(a // b):
            start_idx = int((n * period + phase) * fs)
            end_idx = int(start_idx + (width) * fs)
            if end_idx > N:
                end_idx = N
            signal[start_idx:end_idx] = amplitude
    
    elif signal_type == 'rand_pulse_train':
        a = int(duration*100)
        b = int(period*100)
        for n in range(a // b):
            start_idx = int((n * period + phase) * fs)
            end_idx = int(start_idx + (width) * fs)
            if end_idx > N:
                end_idx = N
            new_amplitude = np.random.uniform(amplitude)
            signal[start_idx:end_idx] = new_amplitude
    
    return np.array(signal)