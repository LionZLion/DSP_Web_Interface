import numpy as np

def generate_damaged_signal(signal, damage_type="zeros", damage_fraction=0.2, dev_noise=1):
    """
    Создаёт повреждённый сигнал на основе исходного.

    Args:
        signal: Оригинальный сигнал.
        damage_type: Тип повреждения ("zeros", "noise", "cut").
        damage_fraction (float): Доля повреждений.

    Returns:
        np.ndarray: Повреждённый сигнал.
    """
    damaged_signal = signal.copy()
    N = len(signal)
    L = int(damage_fraction * N)
    damage_indices = np.random.choice(N, L, replace=False)
    
    if damage_type == "zeros":
        damaged_signal[damage_indices] = 0

    elif damage_type == "noise":
        noise = np.random.normal(0, dev_noise, len(damage_indices))
        damaged_signal[damage_indices] += noise

    elif damage_type == "cut":
        damage_indice = np.random.randint(N - L)
        damaged_signal[damage_indice:damage_indice  + L] = 0
    
    elif damage_type == "lost":
        noise = np.random.normal(0, dev_noise, len(damage_indices))
        damaged_signal[damage_indices] = noise
    return damaged_signal


if __name__ == '__main__':
    fs = 1000
    t = np.linspace(0, 1, fs, endpoint=False)
    signal = np.sin(2 * np.pi * 50 * t)
    damaged_signal = generate_damaged_signal(signal, "cut", 0.2)
    damaged_signal = generate_damaged_signal(damaged_signal, "noise", 0.5, 0.5)