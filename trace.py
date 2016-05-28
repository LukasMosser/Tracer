from itertools import islice
import pygame


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

    def moving_window(seq, n=2):
        "Returns a sliding window (of width n) over data from the iterable"
        "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
        it = iter(seq)
        result = tuple(islice(it, n))
        if len(result) == n:
            yield result
        for elem in it:
            result = result[1:] + (elem,)
            yield result
