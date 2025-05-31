import torch.nn as nn


class Morse_Decoder(nn.Module):
    def __init__(self, num_char):
        super(Morse_Decoder, self).__init__()
        self.hidden_layer = nn.Sequential(
            nn.Conv1d(1, 64, kernel_size=401, stride=4, padding=201),
            nn.BatchNorm1d(64),
            nn.Softplus(),
            nn.Dropout(0.3),

            nn.Conv1d(64, 64, kernel_size=41, stride=1, padding=20),
            nn.BatchNorm1d(64),
            nn.Softplus(),
            nn.Dropout(0.5),

            nn.Conv1d(64, 64, kernel_size=21, stride=1, padding=10),
            nn.BatchNorm1d(64),
            nn.Softplus(),
            nn.Dropout(0.3),
        )

        self.lstm = nn.LSTM(
            input_size=64,
            hidden_size=64,
            num_layers=2,
            batch_first=True,
            bidirectional=True,
            dropout=0.2
        )

        self.output_layer = nn.Sequential(
            nn.Linear(128, num_char),
        )

    def forward(self, inp):
        # batch, channel, time
        x = self.hidden_layer(inp)
        # batch, time, channel
        x = x.permute(0, 2, 1)

        x, _ = self.lstm(x)
        x = self.output_layer(x)

        # time, batch, channel
        x = x.permute(1, 0, 2)
        return x