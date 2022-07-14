"""
Finn Williams
2021/04/16

This file contains the derivative class, MandelbrotSet.
"""
from fractal import Fractal
from fractal import MAX_IT


class MandelbrotSet(Fractal):
    """
    A visual representation of the Mandelbrot set and its derivatives

    Instance Attributes:
      - z0: initial iteration value
      - power: the power to raise each iteration to
      - valid_radius: the radius outside of which an iteration is considered divergent
    """

    def __init__(self, width: int, z0: complex = complex(0, 0), power: float = 2.0):
        self.z0 = z0
        self.power = power
        self.valid_radius = 2
        Fractal.__init__(self, width)
        self.im_buffer = 0.2
        self._init_image()

    def base(self, c, max_it=MAX_IT) -> int:
        """
        The base function for generating the set

        Returns the number of iterations before becoming divergent
        If the number of iterations is equal to max_it, it (the point, c) is
        considered non-divergent
        """
        n = 0
        z = self.z0
        while abs(z) <= self.valid_radius and n < max_it:
            z = pow(z, self.power) + c
            n += 1
        return n

    def point(self, c, max_it=MAX_IT) -> list[complex]:
        """
        Similar to the base function but returns the entire sequence of iterations for further
        calculations
        """
        z = self.z0
        sequence = []
        while abs(z) <= self.valid_radius and len(sequence) < max_it:
            z = pow(z, self.power) + c
            sequence.append(z)
        return sequence
