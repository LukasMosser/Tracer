from itertools import islice
import math
import pygame
import numpy as np


class Trace(object):
    def __init__(self, peaks, screen, noise=False):
        """
        Trace:
        contains representation of trace data
        is used on Screen to represent seismic data
        :return:
        """
        self.peaks = peaks
        self.wavelet = self.ricker_wavelet_analytical()
        if noise:
            added_noise = np.random.uniform(low=-0.03, high=0.03, size=800)
            self.impedance = self.create_impedance_vector(self.peaks, [1]*len(self.peaks), 800, noise=added_noise)
        else:
            self.impedance = self.create_impedance_vector(self.peaks, [1]*len(self.peaks), 800)

        self.data = self.create_trace(self.wavelet, self.impedance)

        self.screen = screen

        self.length = screen.height * 2 # the vertical size in pixels

    def draw_line(self, screen, dim, pos, linecolor=[255, 0, 0], line_resolution=2):
        """
        Draws a horizontal line at position pos
        :param screen: current screen canvas
        :param dim: width of screen
        :param pos: position of line
        :param linecolor: line color as rgb values
        :param lineresolution: width of line segmens
        :return:
        """
        line_range = range(dim-1)
        for pixel_window in self.moving_window(line_range, n=line_resolution):
            pygame.draw.line(screen, linecolor, (pixel_window[0], pos), (pixel_window[1], pos))

    def moving_window(self, seq, n=2):
        "Returns a sliding window (of width n) over data from the iterable"
        "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
        it = iter(seq)
        result = tuple(islice(it, n))
        if len(result) == n:
            yield result
        for elem in it:
            result = result[1:] + (elem,)
            yield result

    def draw(self, pos, x_offset=200, y_offset=200, color=(255, 255, 0)):
		"""
		:param pos: vertical position relative to center
		"""

		window = self.screen.height

		sample_rate = float(len(self.data)) / self.length

		begin_pos = self.length / 2 - window / 2 + pos
		end_pos = self.length / 2 + window / 2 + pos

		begin_index = int(begin_pos * sample_rate)
		end_index = int(end_pos * sample_rate)

		amplitude_factor = 100

		y = end_index - begin_index
		for n in range(begin_index, end_index):
			x0 = self.data[n % len(self.data)] * amplitude_factor + x_offset
			y0 = y / sample_rate

			x1 = self.data[(n+1) % len(self.data)] * amplitude_factor + x_offset
			y1 = (y + 1) / sample_rate

			pygame.draw.aaline(self.screen.screen, color, (x0, y0), (x1, y1), 2)
			y = y - 1


    def ricker_wavelet_analytical(self, frequency=10., position=0.5, resolution=1000):
        time = np.linspace(0, 1.0, resolution)
        time_pow = np.power(time-position, 2)
        ricker = np.multiply(1-2*np.pi**2*frequency**2.*time_pow, np.exp(-np.pi**2*frequency**2.*time_pow))
        return ricker

    def create_impedance_vector(self, positions, values, dim, noise=None):
        impedance_values = np.zeros(dim)
        if noise is not None:
            impedance_values = np.add(impedance_values, noise)

        for position, value in zip(positions, values):
            impedance_values[position] = value
        return impedance_values

    def create_trace(self, wavelet, impedance):
        return np.convolve(wavelet, impedance)
