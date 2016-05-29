from trace import Trace
from numpy.random import randint, normal, uniform
from collections import deque

class Level(object):
    def __init__(self, peaks, screen):
        self.screen = screen

        self.dim = self.screen.height
        self.peaks = peaks
        self.previous_traces = deque()
        self.current_trace = None
        self.next_trace = None

        self.reference_trace = None

        self.top_pad = 10
        self.bottom_pad = 10

        self.level_params = {"switch_probability": 0.05, "peak_shift_distance_min": 3, "peak_shift_distance_max": 100, "peak_shift_spread": 1.0}

    def initial_trace(self):
        self.reference_trace = Trace([400], self.screen)
        self.current_trace = Trace([400], self.screen, noise=True)
        self.current_trace.peaks = randint(0, high=self.dim, size=self.peaks)

    def get_next_trace(self):
        new_trace = Trace([400], self.screen, noise=True)
        for i, (current_peak, next_peak) in enumerate(zip(self.current_trace.peaks, new_trace.peaks)):
            new_pos = self.get_new_peak_position(current_peak)
            while new_pos <= self.bottom_pad or new_pos >= self.dim-self.top_pad:
                new_pos = self.get_new_peak_position(current_peak)
            new_trace.peaks[i] = new_pos
        return new_trace

    def get_new_peak_position(self, current_pos):
        switch = 1
        if uniform() < self.level_params["switch_probability"]:
            switch = -1
        peak_shift_distance = randint(self.level_params["peak_shift_distance_min"], high=self.level_params["peak_shift_distance_max"])
        shift = int(normal(loc=0.0, scale=self.level_params["peak_shift_spread"])*peak_shift_distance*switch)
        new_pos = current_pos+shift
        return new_pos

    def push_next_trace(self):
        self.previous_traces.append(self.current_trace)
        self.current_trace = self.get_next_trace()