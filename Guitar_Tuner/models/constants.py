A4_FREQ = 440
"""Frequency associated with A4 tone, 440 Hz by standard."""

_12TH_ROOT_OF_2 = 1.05946309436
"""12th root of 2, approx. 1.06, frequently used in calculating pitches."""

SAMPLING_RATE = 44100
"""Indicates how many samples are taken from input stream in a second."""

BLOCK_SIZE = 22050
"""Indicates how often a callback function is called by the stream (as a number of samples passed with each call)."""

HIGH_FREQUENCY = 700
"""Highest frequency considered when estimating sound frequency."""

LOW_FREQUENCY = 60
"""Lowest frequency considered when estimating sound frequency."""

SECONDS_TO_TUNE = 2
"""Indicates how long input sound's frequency have to fit within error margin of a string's pitch in order to 
consider that string to in tune. """

ERROR_MARGIN = 0.1
"""Indicates how wide is the interval of accepted frequencies around perfect frequency of a tone."""

BACKLOG_SIZE = 2
"""Indicates how many blocks of input are kept in memory and considered in process of estimating frequency."""

MAX_DOWNSAMPLING = 4
"""Indicates number of epochs for HPS algorithm."""
