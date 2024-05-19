import statsmodels
from arch import arch_model
import matplotlib.pyplot as plt
import torch
import torch.nn as nn


class GARCHModel:
    def __init__(self, p, q, dist='normal', start_vals = None):
        self.p = p
        self.q = q
        self.dist = dist
        self.model = None
        self.result = None
        self.resid = None
        self.conditional_volatility = None
        self.start_vals = start_vals

    def fit_garch_model(self, data, disp='final'):
        self.model = arch_model(data, vol='GARCH', p=self.p, q=self.q, dist=self.dist, mean='Zero')
        self.result = self.model.fit(disp=disp, options={'maxiter': 100000})
        self.resid = self.result.resid
        self.conditional_volatility = self.result.conditional_volatility

    def plot_results(self):
        print(self.result.summary())
        self.result.plot()
        plt.show()

    def EngleArchTest_(self):
        test_result = statsmodels.stats.diagnostic.het_arch(self.resid, nlags=10, store=False, ddof=0)
        print(f"Test results: {test_result}")

    def forecast(self, horizon=1):
        forecast = self.result.forecast(horizon=horizon)
        return forecast


class LSTMModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, layer_dim, output_dim):
        super(LSTMModel, self).__init__()
        # Hidden dimensions
        self.hidden_dim = hidden_dim

        # Number of hidden layers
        self.layer_dim = layer_dim

        # Building your LSTM
        # batch_first=True causes input/output tensors to be of shape
        # (batch_dim, seq_dim, feature_dim)
        self.lstm = nn.LSTM(input_dim, hidden_dim, layer_dim, batch_first=True)

        # Readout layer
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        # Initialize hidden state with zeros
        h0 = torch.zeros(self.layer_dim, x.size(0), self.hidden_dim).requires_grad_()

        # Initialize cell state
        c0 = torch.zeros(self.layer_dim, x.size(0), self.hidden_dim).requires_grad_()

        # We need to detach as we are doing truncated backpropagation through time (BPTT)
        # If we don't, we'll backprop all the way to the start even after going through another batch
        out, (hn, cn) = self.lstm(x, (h0.detach(), c0.detach()))

        # Index hidden state of last time step
        # out.size() --> 100, 28, 100
        # out[:, -1, :] --> 100, 100 --> just want last time step hidden states!
        out = self.fc(out[:, -1, :])
        # out.size() --> 100, 10
        return out
