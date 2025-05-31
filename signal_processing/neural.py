import torch
import torch.nn as nn
import numpy as np
from morse.CTC_decoder import CTC_decoder
from morse.model_class import Morse_Decoder
from morse.word_to_morse import morse_generator
from morse.stft import fft_morse


def morse_numpy(msg, prp, dev=0.5):

    signal = morse_generator(msg, prp['dt'], prp['nu'], prp['fs'], noise=True, dev=dev)
    signal = np.float32(signal / np.max(np.abs(signal)))
    fft_transform = fft_morse(
        signal, 
        step=prp['step'], 
        size=prp['size'], 
        nu=prp['nu'], 
        fs=prp['fs']
        )
    
    return fft_transform
    

def morse_processing(input_signal):
    
    signal_stft = torch.tensor(input_signal, dtype=torch.float)
    model = Morse_Decoder(57)
    weights = torch.load('best_model.tar', weights_only=True, map_location=torch.device('cpu'))
    model.load_state_dict(weights)
    model.eval()

    with torch.no_grad():
        predict = model(signal_stft.unsqueeze(0).unsqueeze(0))
        predict = nn.functional.log_softmax(predict, dim=-1)
        pred_indices = torch.argmax(predict, dim=-1)
        pred_indices = pred_indices.permute(1, 0).squeeze(0)
        main_answer = CTC_decoder(pred_indices)
    
    return main_answer

if __name__ == '__main__':
    msg = 'Привет'
    print(*morse_processing(msg, dev=0.5))