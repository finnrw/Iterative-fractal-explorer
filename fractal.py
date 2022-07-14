"""
Finn Williams
2021/04/16

This file contains the base class, Fractal.
"""
from math_functions import *

from numpy import mean, exp  # These are much faster than what I can write
from PIL import Image, ImageDraw
import math
import pyglet
from graph import *

# noinspection PyBroadException
try:  # This try-except is to account for differences in operating systems
    import ctypes
    user32 = ctypes.windll.user32  # NOTE: This maybe only works on windows
    S_WIDTH = user32.GetSystemMetrics(0)
    S_HEIGHT = user32.GetSystemMetrics(1)
except:
    S_WIDTH = 1280
    S_HEIGHT = 720

XY_MAX = 10
MAX_IT = 32
MAX_PATTERN = 32


class Fractal:
    """
    The base (or parent) function used to represent and model a iterative fractal and its orbitals.

    The fractal image is defined in terms of width, as the height is of the image is just the screen
    height.

    Instance Attributes:
      - im_buffer: the extra distance that should be added (or subtracted) from the ranges to clean
      up the fractal image
      - _width: width of image
      - _height: height of image
      - shapes: related to the batch functionality of pyglet library
      - batch: a collection of graphical components that are all drawn to the screen at once
    """

    def __init__(self, width: int):
        self.im_buffer = 0.0
        self._height = S_HEIGHT
        self._width = width

        self.shapes = []
        self.batch = pyglet.graphics.Batch()

        self.im = None
        self.x_range = None
        self.y_range = None

    def base(self, c: complex, n: int = MAX_IT) -> int:
        """
        A base function made to be overloaded with the base function of the fractal
        """
        pass

    def point(self, c: complex, n: int = MAX_IT) -> list[complex]:
        """
        A base function made to be overloaded with the base function of the fractal
        """
        pass

    def _init_image(self) -> None:
        """
        Generates the initial fractal image used for the background and
        calculates the ranges to accelerate updating the background
        """

        # Determine the x and y range of the fractal
        x_range = DRange(0, 0)
        y_range = DRange(0, 0)
        x = -XY_MAX
        y = -XY_MAX
        while x < XY_MAX:
            while y < XY_MAX:
                if self.base(complex(x, y)) >= MAX_IT:
                    if x_range.max <= x:
                        x_range.max = x
                    elif x_range.min > x:
                        x_range.min = x
                    if y_range.max <= y:
                        y_range.max = y
                    elif y_range.min > y:
                        y_range.min = y
                y += 0.05
            y = -XY_MAX
            x += 0.05

        x_range.max += self.im_buffer
        x_range.min -= self.im_buffer

        y_range.max += self.im_buffer
        y_range.min -= self.im_buffer

        x_range.update_span()
        y_range.update_span()

        xi_scale = x_range.span / y_range.span
        xy_scale = self._width / self._height

        # determine which dimension the diagram needs to be scaled to match the scale of the screen
        if xi_scale >= xy_scale:
            scale_buffer = (y_range.span * self._width - x_range.span * self._height) / \
                           (2 * self._height)
            x_range.max += scale_buffer
            x_range.min -= scale_buffer
        else:
            scale_buffer = (x_range.span * self._height - y_range.span * self._width) / \
                           (2 * self._width)
            y_range.max += scale_buffer
            y_range.min -= scale_buffer

        x_range.update_span()
        y_range.update_span()

        self.x_range = x_range
        self.y_range = y_range
        self.update_image()  # generate the image using the generated parameters

    def update_image(self) -> None:
        """
        Updates fractal image
        """
        im = Image.new('RGB', (self._width, self._height), (0, 0, 0))
        draw = ImageDraw.Draw(im)

        for x in range(0, self._width):
            for y in range(0, self._height):
                c = complex(self.x_range.min + (x / self._width) * self.x_range.span,
                            self.y_range.min + (y / self._height) * self.y_range.span)

                final_n = self.base(c)

                rgb_scale = int(final_n * 255 / MAX_IT)
                rgb = 255 - int(-255 * math.log(rgb_scale, 1 / 255))
                draw.point([x, y], (rgb, 0, rgb))

        self.im = im

    def save_image(self, local_address: str) -> None:
        """
        Saves image at the given local address
        """
        self.im.save(local_address + '.png')

    def update_point(self, x: int, y: int, n: int = MAX_IT):
        """
        Classifies whether a point (given by clicking on the screen) is
        divergent (not in Mandelbrot set), convergent, cyclic, or chaotic or divergent
        and then draws the points that have been iterated through on the graph
        """
        self.clear_batch()
        c = complex(self.x_range.min + (x / self._width) * self.x_range.span,
                    self.y_range.min + (y / self._height) * self.y_range.span)

        sequence = self.point(c, n)  # Iteration sequence

        # Use a graph mapping
        graph = Graph()
        for cn in sequence:
            graph.add_vertex(cn, 'graph')

            screen_x = self._width * (cn.real - self.x_range.min) / self.x_range.span
            screen_y = self._height * (cn.imag - self.y_range.min) / self.y_range.span
            graph.add_vertex((screen_x, screen_y), 'screen')

            graph.add_edge(cn, (screen_x, screen_y))

        # First determine what kind of sequence was generated
        center = c
        if len(sequence) < n:
            orbit = 'TYPE: divergent'
        else:
            center = sum(sequence) / len(sequence)
            d_seq = [complex_distance(sequence[i], sequence[i + 1])
                     for i in range(int(n * (1 - 1 / exp(abs(center)))))]

            if all([d_seq[i] >= mean(d_seq[i + 1:n]) for i in range(len(d_seq) - 1)]):
                orbit = 'TYPE: convergent\n\nCENTER: ' + \
                        str(complex(round(center.real, 2), round(center.imag, 2)))
            else:
                pattern = get_pattern([complex(el.real, el.imag) for el in sequence[-MAX_PATTERN:]])
                if pattern == [] or len(pattern) == MAX_PATTERN // 4 + 1:
                    orbit = 'TYPE: chaotic or undetermined' + \
                            '\n\nTEST DEPTH: ' + str(n) + \
                            '\n\nCENTER: ' + str(complex(round(c.real, 2), round(c.imag, 2)))

                else:
                    orbit = 'TYPE: cyclic' + \
                            '\n\nPERIOD: ' + str(len(pattern)) + \
                            '\n\nCENTER: ' + str(complex(round(c.real, 2), round(c.imag, 2)))

        # Then draw the sequence to the screen
        x1, y1 = graph.get_neighbour(sequence[0]).item

        self.shapes.append(
            pyglet.shapes.Circle(x1, y1, radius=2, color=(255, 255, 255), batch=self.batch))

        for i in range(len(sequence) - 1):  # This draws the lines and white circles
            x2, y2 = graph.get_neighbour(sequence[i + 1]).item
            self.shapes.append(pyglet.shapes.Line(x1, y1, x2, y2, width=1, batch=self.batch,
                                                  color=(255, 0, 255)))
            self.shapes.append(
                pyglet.shapes.Circle(x2, y2, radius=2, color=(255, 255, 255), batch=self.batch))
            x1 = x2
            y1 = y2

        x = self._width * (c.real - self.x_range.min) / self.x_range.span  # Red circle
        y = self._height * (c.imag - self.y_range.min) / self.y_range.span
        self.shapes.append(
            pyglet.shapes.Circle(x, y, radius=5, color=(0, 255, 255), batch=self.batch))

        return orbit, sequence

    def update(self, x: int, y: int, n: int = MAX_IT) -> None:
        """
        The quicker version of update_point that allows the image to update live as a user
        drags around the mouse
        """
        self.clear_batch()
        c = complex(self.x_range.min + (x / self._width) * self.x_range.span,
                    self.y_range.min + (y / self._height) * self.y_range.span)

        sequence = self.point(c, n)  # Iteration sequence

        # Scale the given point to its equivalent on the fractal graph
        x1 = self._width * (c.real - self.x_range.min) / self.x_range.span
        y1 = self._height * (c.imag - self.y_range.min) / self.y_range.span
        self.shapes.append(
            pyglet.shapes.Circle(x1, y1, radius=2, color=(0, 255, 255), batch=self.batch))

        # Draw the sequence to the screen
        x1 = self._width * (sequence[0].real - self.x_range.min) / self.x_range.span
        y1 = self._height * (sequence[0].imag - self.y_range.min) / self.y_range.span
        self.shapes.append(
            pyglet.shapes.Circle(x1, y1, radius=2, color=(255, 255, 255), batch=self.batch))
        for i in range(len(sequence) - 1):  # This draws the lines and white circles
            x2 = self._width * (sequence[i + 1].real - self.x_range.min) / self.x_range.span
            y2 = self._height * (sequence[i + 1].imag - self.y_range.min) / self.y_range.span
            self.shapes.append(pyglet.shapes.Line(x1, y1, x2, y2, width=1, batch=self.batch,
                                                  color=(255, 0, 255)))
            self.shapes.append(
                pyglet.shapes.Circle(x2, y2, radius=2, color=(255, 255, 255), batch=self.batch))
            x1 = x2
            y1 = y2
        x = self._width * (c.real - self.x_range.min) / self.x_range.span  # Cyan circle
        y = self._height * (c.imag - self.y_range.min) / self.y_range.span
        self.shapes.append(
            pyglet.shapes.Circle(x, y, radius=5, color=(0, 255, 255), batch=self.batch))

    def clear_batch(self) -> None:
        """
        Clears the last epoch of drawn lines to allow a new, clean drawing
        """
        self.shapes = []

    def get_height(self) -> int:
        """
        returns value of private attribute self._height
        """
        return self._height

    def get_width(self) -> int:
        """
        returns value of private attribute self._width
        """
        return self._width
