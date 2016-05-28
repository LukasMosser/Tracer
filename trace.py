from itertools import islice
import pygame
import numpy as np


class Trace(object):
    def __init__(self):
        """
        Trace:
        contains representation of trace data
        is used on Screen to represent seismic data
        :return:
        """
        self.data = []

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