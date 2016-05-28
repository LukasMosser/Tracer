from itertools import islice
import math
import pygame


class Trace(object):
    def __init__(self, screen):
        """
        Trace:
        contains representation of trace data
        is used on Screen to represent seismic data
        :return:
        """
        self.data = [math.sin(float(n) / 3) for n in range(100)]

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

    def draw(self, pos, offset=200):
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

        for n in range(begin_index, end_index):
            x0 = self.data[n] * amplitude_factor + offset
            y0 = n / sample_rate - window / 2

            x1 = self.data[n + 1] * amplitude_factor + offset
            y1 = (n + 1) / sample_rate - window / 2

            pygame.draw.line(self.screen.screen, (255, 0, 255), (x0, y0), (x1, y1), 2)
    
