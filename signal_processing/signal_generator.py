import numpy as np
from scipy.linalg import hadamard
from operator import xor

def signal_gen(type, frequency, amplitude, t, phase):
    if type == "sine":
        #sinusoid
        signal = amplitude * np.sin(2*np.pi * (frequency * t + phase))
        
    elif type == "meandr":
        #meandr
        signal = amplitude * np.sign(np.sin(2*np.pi * (frequency * t + phase)))
        if phase == 0:
            signal[0] = amplitude
            signal[-1] = -amplitude
    elif type == "sawtooth":
        #sawtooth
        a = t * frequency + phase 
        signal = 2 * amplitude * (a - np.floor(a)) - amplitude
    elif type == "triangle":
        #triangle
        signal = 2 * amplitude / np.pi * np.arcsin(np.sin(2*np.pi * (frequency * t + phase)))
    
    return np.round(signal, 8)


def walsh_function(fs, N):
    hadamardM = hadamard(fs)
    HadIdx = np.arange(fs)  # Индексы Адамара
    M = int(np.log2(fs))
    binHadIdx = np.fliplr(np.array([[int(b) for b in format(i, f'0{M}b')] for i in HadIdx]))
    binSeqIdx = np.zeros((fs, M), dtype=int)
    for k in range(0, M-1):
        binSeqIdx[:,k] = xor(binHadIdx[:, k], binHadIdx[:, k+1])
    
    binSeqIdx[:,M-1] = binHadIdx[:, M-1]
    SeqIdx = np.matmul(binSeqIdx, (2 ** (np.arange(M-1, -1, -1))))
    walshMatrix = hadamardM[SeqIdx]
    return walshMatrix[N-1, :]

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
    type = "sine"  # "sine", "meandr", "sawtooth", "triangle"
    frequency = 1  # Frequency in Hz
    amplitude = 1  # Amplitude of the signal
    phase = 0  # Phase shift in radians
    t = np.linspace(0, 1, 4)  # Time vector from 0 to 1 second with 3 samples
    plt.plot(signal_gen(type, frequency, amplitude, t, phase))
    plt.show()