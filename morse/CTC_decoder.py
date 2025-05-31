import json
import numpy as np

with open('morse_dict.json', 'r') as file:
    morse_code = json.load(file)


coding_dict = {char: idx + 1 for idx, char in enumerate(morse_code.keys())}
decoding_dict = {v: k for k, v in coding_dict.items()}

def coding_char(message):
    coding = []
    for ch in message:
        coding.append(coding_dict[ch])

    return np.array(coding)


def decoding_char(message):
    decoding = []
    for ch in message:
        decoding.append(decoding_dict[ch])

    return ''.join(str(x) for x in decoding)


def CTC_decoder(predict):
    blanc = 0
    decoded = []
    prev = blanc
    word = []
    for chr in predict:
        if chr != prev and chr != blanc:
            word.append(int(chr))
        prev = chr
    decoded.append(decoding_char(word))

    return decoded

if __name__ == '__main__':
    
    message = 'АБВГ'
    encoded_message = coding_char(message)
    print(f"Encoded: {encoded_message}")
    decoded_message = decoding_char(encoded_message)
    print(f"Decoded: {decoded_message}")
    decoded_message = CTC_decoder([1, 1, 1, 0, 1, 2, 2, 0, 3, 3, 0])
    print(f"Decoded: {decoded_message}")