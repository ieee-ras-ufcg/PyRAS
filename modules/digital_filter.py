import numpy as np


class FirstOrderLowPass:
    def __init__(
        self,
        fc,  # Cutoff frequency, in Hz
        fs,  # Sampling frequency, in Hz
    ):
        self.Ts = 1.0 / fs  # Sampling time
        self.tau = 1.0 / (2 * np.pi * fc)  # Filter time constant
        self.alpha = self.Ts / (self.tau + self.Ts)
        self.y_prev = 0.0

    def filter(self, x):
        y = self.alpha * x + (1 - self.alpha) * self.y_prev
        self.y_prev = y

        return y


class LowPassFilter:
    def __init__(
        self,
        order,  # Order of the filter
        fc,  # Cutoff frequency, in Hz
        fs,  # Sampling frequency, in Hz
    ):
        self.stages = [FirstOrderLowPass(fc, fs) for _ in range(order)]

    def filter(self, x):
        for stage in self.stages:
            x = stage.filter(x)

        return x


class FirstOrderHighPass:
    def __init__(
        self,
        fc,  # Cutoff frequency, in Hz
        fs,  # Sampling frequency, in Hz
    ):
        self.Ts = 1.0 / fs  # Sampling time
        self.tau = 1.0 / (2 * np.pi * fc)  # Filter time constant
        self.alpha = self.tau / (self.tau + self.Ts)
        self.x_prev = 0.0
        self.y_prev = 0.0

    def filter(self, x):
        y = self.alpha * (self.y_prev + x - self.x_prev)
        self.x_prev = x
        self.y_prev = y
        return y


class HighPassFilter:
    def __init__(
        self,
        order,  # Order of the filter
        fc,  # Cutoff frequency, in Hz
        fs,  # Sampling frequency, in Hz
    ):
        self.stages = [FirstOrderHighPass(fc, fs) for _ in range(order)]

    def filter(self, x):
        for stage in self.stages:
            x = stage.filter(x)

        return x
