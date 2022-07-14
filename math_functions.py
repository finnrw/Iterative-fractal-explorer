"""
Finn Williams
2021/04/16

This file contains mathematical helper functions and classes.
"""
import math


def complex_distance(c1, c2) -> float:
    """
    Returns the absolute distance between two complex numbers on the complex plane
    """
    real_comp = abs(c1.real - c2.real)
    imag_comp = abs(c1.imag - c2.imag)
    return math.sqrt(real_comp ** 2 + imag_comp ** 2)


def is_sublist(sub: list, lst: list, acc: float) -> bool:
    """"
    Returns whether or not sub is a sublist of lst

    >>> sub = [1, 2, 3]
    >>> lst = [-3, 5, 0, 1, 2, 3, 4, 9]
    >>> is_sublist(sub, lst)
    True

    >>> sub = [1, 2]
    >>> lst = [3, 4, 5, 6]
    >>> is_sublist(sub, lst)
    False
    """
    if sub == lst:
        return True

    for i in range(0, len(lst) - len(sub), 1):
        # if lst[i:i + len(sub)] == sub:
        #     return True
        if all([acc > abs(lst[i:i + len(sub)][n] - sub[n]) for n in range(len(sub))]):
            return True

    return False


def get_pattern(seq: list, acc: float = 0.00025) -> list:
    """
    Returns the shortest pattern found in seq
    or if there are no patterns returns []

    >>> seq = [1, 2, 3, 1, 2, 3, 1, 2, 3]
    >>> get_pattern(seq)
    [1, 2, 3]

    >>> seq = [1, 2, 3, 4]
    >>> get_pattern(seq)
    []
    """
    s_range = int(round(len(seq) / 2))
    for a in range(1, s_range):
        for b in range(len(seq) - a):
            if is_sublist(seq[b:a + b] * int(s_range / a - 1), seq[:b] + seq[a + b:len(seq)], acc):
                return seq[b:a + b]
    return []


class DRange:
    """
    Represents a range on a number line

    Instance Attributes:
      - max: the maximum value contained in the range
      - min: the minimum value contained in the range
      - span: the distance on a number line between max and min

    Representation Invariants:
      - max >= min
      - span >= 0
    """

    def __init__(self, max: float, min: float):
        self.max = max
        self.min = min
        self.span = max - min

    def update_span(self) -> None:
        """
        Updates self.span to match possible new values of self.max and self.min
        """
        self.span = self.max - self.min
