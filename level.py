from trace import Trace
from numpy.random import randint, normal, uniform, seed
from collections import deque
import json
from survey import Survey

class Level(object):
    def __init__(self, peaks, screen):
        seed(666)
        self.screen = screen

        self.survey = Survey()
        self.artificial = True

        self.dim = self.screen.height
        self.peaks = peaks
        self.previous_traces = deque()
        self.current_trace = None
        self.next_trace = None

        self.reference_trace = None

        self.top_pad = 10
        self.bottom_pad = 10

        self.level_params = {"switch_probability": 0.05, "peak_shift_distance_min": 100, "peak_shift_distance_max": 400, "peak_shift_spread": 1.0}

        self.interpreted_traces = []
        self.current_real_trace = 0

    def initial_trace(self):
        self.reference_trace = Trace([400], self.screen)
        if not self.artificial:
            self.reference_trace.data = self.survey.data[self.current_real_trace, :]#/(max(self.survey.data[:, 0])-min(self.survey.data[:, 0]))
        self.current_real_trace += 1
        self.current_trace = Trace([400], self.screen, noise=True)

        if not self.artificial:
            self.current_trace.data = self.survey.data[self.current_real_trace, :]
        self.current_real_trace += 1
        self.current_trace.peaks = randint(0, high=self.dim, size=self.peaks)

    def get_next_trace(self):
        new_trace = Trace([400], self.screen, noise=True)
        for i, (current_peak, next_peak) in enumerate(zip(self.current_trace.peaks, new_trace.peaks)):
            new_pos = self.get_new_peak_position(current_peak)
            while new_pos <= self.bottom_pad or new_pos >= self.dim-self.top_pad:
                new_pos = self.get_new_peak_position(current_peak)
            new_trace.peaks[i] = new_pos
            print new_trace.peaks

        if not self.artificial:
            new_trace.data = self.survey.data[self.current_real_trace, :]
            self.current_real_trace += 1

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

    def save_json(self):

        traces_out = [[list(trace_dat[0]), trace_dat[1]] for trace_dat in self.interpreted_traces]
        data_out = {"data": traces_out}
        #print data_out
        with open("interpretation.json", "w") as f:
            json.dump(data_out, f)