import numpy as np
from scipy.fft import rfft, irfft

np.random.seed(42)

def noise_wr(noise_f):
    def wrapper(N, noise_deviation):
        white_noise = rfft(np.random.normal(0, noise_deviation, N))
        S = noise_f(np.fft.rfftfreq(N), noise_deviation)               # Применение декорируемой функции
        #Здесь работаем с амплитудами, а они корень из мощности, поэтому и из частот тоже корень(для нормировки)
        S = S / np.sqrt(np.mean(S**2))
        X_shaped = white_noise * S
        return irfft(X_shaped, n=N)     
    return wrapper        

@noise_wr
def white_noise(f, noise_deviation):
    return 1

@noise_wr
def blue_noise(f, noise_deviation):
    return np.sqrt(f)

@noise_wr
def violet_noise(f, noise_deviation):
    return f

@noise_wr
def red_noise(f, noise_deviation):
    return 1/np.where(f == 0, float('inf'), f)

@noise_wr
def pink_noise(f, noise_deviation):
    return 1/np.where(f == 0, float('inf'), np.sqrt(f))

def noise_gen(t, noise_deviation, noise_type):
    if noise_type == 'white':
        return white_noise(t, noise_deviation)
    elif noise_type == 'blue':
        return blue_noise(t, noise_deviation)
    elif noise_type == 'violet':
        return violet_noise(t, noise_deviation)
    elif noise_type == 'red':
        return red_noise(t, noise_deviation)
    elif noise_type == 'pink':
        return pink_noise(t, noise_deviation)
    else:
        raise ValueError("Unknown noise type")

if __name__ == '__main__':
    print(len(noise_gen(77297, 1, 'white')))