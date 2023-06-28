import threading
from dataclasses import dataclass
from typing import Callable, List, Tuple
import sounddevice as sd
import numpy as np
from models.constants import BLOCK_SIZE, SAMPLING_RATE, SECONDS_TO_TUNE, BACKLOG_SIZE
from models.pitch import Pitch
from models.sample import Sample
from models.tunings import TUNINGS


@dataclass
class TuningStatus:
    closest_pitch: Pitch
    freq: float
    freq_diff: float
    freq_diff_normalized: float
    strings: List[Tuple[Pitch, float]]


class Stream(sd.InputStream):

    def update_instrument(self, tuning: List[Pitch]):
        print('Updated tuning to ' + str([str(pitch) for pitch in tuning]))
        self.strings = tuning
        self.tunings = [0 for _ in self.strings]

    def read_input(self, indata: np.ndarray, frames, time, status) -> None:
        if len(self.backlog) >= BACKLOG_SIZE * BLOCK_SIZE:
            self.backlog = self.backlog[BLOCK_SIZE:]

        self.backlog = np.append(self.backlog, indata)

        if len(self.backlog) != BACKLOG_SIZE * BLOCK_SIZE:
            return

        sample = Sample(self.backlog)
        freq = sample.harmonic_product_spectrum()

        pitch = Pitch.from_frequency(freq)

        if pitch.is_within_error_margin(freq):
            for i in range(len(self.strings)):
                if self.strings[i] == pitch:
                    self.tunings[i] = min(1, self.tunings[i] + (BLOCK_SIZE / (SAMPLING_RATE * SECONDS_TO_TUNE)))

        self.update_view(TuningStatus(
            closest_pitch=pitch,
            freq=freq,
            freq_diff=freq - pitch.frequency,
            freq_diff_normalized=(freq - pitch.frequency) * 2 / (pitch.frequency - pitch.shift(-1).frequency),
            strings=[(self.strings[i], self.tunings[i]) for i in range(len(self.strings))])
        )

    def __init__(self, update_view: Callable[[TuningStatus], None]):
        super().__init__(
            callback=lambda indata, frames, time, status: self.read_input(indata, frames, time, status),
            channels=1,
            samplerate=SAMPLING_RATE,
            blocksize=BLOCK_SIZE
        )
        self.update_view = update_view
        self.strings = TUNINGS['guitar standard']
        self.tunings = [0 for _ in self.strings]
        self.backlog = np.array([])
