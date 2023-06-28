import copy
import math

import numpy as np
import scipy.fftpack
from models.constants import HIGH_FREQUENCY, SAMPLING_RATE, LOW_FREQUENCY, MAX_DOWNSAMPLING


class Sample:
    def __init__(self, data: np.ndarray):
        self.data = data

    @property
    def duration(self) -> float:
        return len(self.data) / SAMPLING_RATE

    @property
    def power(self) -> float:
        """
        :return: Signal power of the sample.
        """
        return np.sum([x ** 2 for x in self.data]) / len(self.data)

    def discrete_fourier_transform(self) -> np.ndarray:
        """
        Transforms sample data from displacement domain to frequency domain.
        """
        window = np.hanning(len(self.data))
        flat_data = self.data.flatten()
        dft = abs(scipy.fftpack.fft(flat_data * window))

        for i in range(LOW_FREQUENCY):
            dft[i] = 0

        return dft[:min(len(dft) // 2, HIGH_FREQUENCY)]

    def harmonic_product_spectrum(self) -> float:
        """
        Estimates frequency of the sample using Harmonic Product Spectrum.

        :return: Estimated frequency.
        """
        window = np.hanning(len(self.data)) * self.data.flatten()
        rate = 1 / self.duration

        dft = abs(scipy.fftpack.fft(window)[:len(window) // 2])
        dft = self.reduce_white_noise(dft, rate)
        dft = self.interpolate_spectrum(dft)

        product_spectrum = copy.deepcopy(dft)

        for start in range(MAX_DOWNSAMPLING):
            product_spectrum = np.multiply(product_spectrum[:int(np.ceil(len(dft) / (start + 1)))], dft[::(start + 1)])

        return np.argmax(product_spectrum) * rate / MAX_DOWNSAMPLING

    @classmethod
    def interpolate_spectrum(cls, dft):
        """
        Interpolates spectrum.
        """
        dft = np.interp(np.arange(0, len(dft), 1 / MAX_DOWNSAMPLING), np.arange(0, len(dft)), dft)
        return dft / np.linalg.norm(dft, ord=2)

    @classmethod
    def reduce_white_noise(cls, dft, rate):
        """
        Reduces white noise from the sample.

        :param dft: Vector of samples after applying DFT
        :param rate: reverse of duration of the sample
        :return: noise-reducted vector
        """
        for i in range(int(LOW_FREQUENCY / rate)):
            dft[i] = 0

        octaves = [50 * i for i in range(1, 11)]

        for j in range(len(octaves) - 1):
            start = int(octaves[j] / rate)
            end = min(int(octaves[j + 1] / rate), len(dft))
            power_freq = math.sqrt((np.linalg.norm(dft[start:end], ord=2) ** 2) / (end - start))

            for start in range(start, end):
                dft[start] = dft[start] if dft[start] > power_freq else 0

        return dft
