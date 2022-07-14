"""
Finn Williams
2021/04/16

This file contains graphical objects used in displaying information with pyglet.
"""

import pyglet


class Button:
    """
    Graphical object representing a clickable button with text and a given action to call upon
    press.

    Instance Attributes:
      - action: function to be called upon press
    """

    def __init__(self, action, start: tuple, end: tuple, text: str = ''):
        self.batch = pyglet.graphics.Batch()
        self.shapes = []

        self.action = action

        self.start = start
        self.end = end
        self.width = abs(start[1] - start[0])
        self.height = abs(start[1] - start[0])

        self.text = text

        self.update()

    def get(self, x, y) -> bool:
        """
        Return whether or not a click at (x, y) was on the button
        """
        return self.start[0] < x < self.end[0] and self.start[1] < y < self.end[1]

    def get_press(self, x, y) -> None:
        """
        Check if a click was on the button and if so, call the button's action function
        """
        if self.start[0] < x < self.end[0] and self.start[1] < y < self.end[1]:
            self.action()

    def clear_batch(self) -> None:
        """Clear the graphical batch, removes button from screen"""
        self.shapes = []

    def update(self) -> None:
        """
        Update button graphically
        """
        self.clear_batch()
        x = (self.start[0] + self.end[0]) // 2
        y = (self.start[1] + self.end[1]) // 2
        self.shapes.append(pyglet.text.Label(self.text,
                                             x=x, y=y,
                                             anchor_x='center', anchor_y='center',
                                             font_size=28,
                                             batch=self.batch))


class PropertiesBox:
    """
    Graphical object that displays information on the given orbital.

    Instance Attributes:
      - label: a sub-object used to contain text information
      - desc: a sub-object used to contain a sentence
    """

    def __init__(self, p1: tuple, p2: tuple):
        self.buffer = 20

        self.height = abs(p1[1] - p2[1])
        self.width = abs(p1[0] - p2[0])
        self.p1 = p1
        self.p2 = p2

        self.batch = pyglet.graphics.Batch()
        self.shapes = []

        self.label = None
        self.desc = None
        self.update('')

    def update(self, text: str) -> None:
        """
        Updates the information in the info box given new text
        """
        self.label = pyglet.text.Label(text,
                                       bold=True,
                                       x=self.p1[0] + self.buffer, y=self.p2[1] - self.buffer,
                                       anchor_x='left', anchor_y='top',
                                       multiline=True,
                                       width=(self.width - 2 * self.buffer) // 2,
                                       batch=self.batch)
        description = ''
        if 'divergent' in text:
            description = 'This sequence approaches infinity.'
        elif 'convergent' in text:
            description = 'This sequence approaches a single point within the Mandelbrot set.'
        elif 'cyclic' in text:
            description = 'This sequence forms a stable orbital or pattern. \nNote: the ' + \
                          'pattern often emerges later in the sequence as it stabilizes. '
        elif 'chaotic' in text:
            description = 'This sequence forms a chaotic orbit with no repeating points or ' + \
                          'the test depth was not great enough to determine its true type.'

        self.desc = pyglet.text.Label(description,
                                      bold=False,
                                      x=(self.p1[0] + self.p2[0]) / 2 + self.buffer,
                                      y=self.p2[1] - self.buffer,
                                      anchor_x='left', anchor_y='top',
                                      multiline=True,
                                      width=(self.width - 2 * self.buffer) // 2,
                                      batch=self.batch)

    def clear_batch(self) -> None:
        """Clears the graphical batch, removing the properties box from the screen"""
        self.label.delete()
        self.desc.delete()


class CyclicGraph:
    """
    Graphical object that displays the cycle-graph of the given sequence.

    Instance Attributes:
      - n_points: number of iterations to be displayed
    """

    def __init__(self, p1: tuple, p2: tuple):
        self.batch = pyglet.graphics.Batch()
        self.shapes = []

        self.n_points = 50
        self.buffer = 20

        self.height = abs(p1[1] - p2[1])
        self.width = abs(p1[0] - p2[0])
        self.p1 = p1
        self.p2 = p2

    def update(self, sequence: list) -> None:
        """
        Update the cycle-graph given a new sequence
        """
        self.clear_batch()
        sequence = [abs(c) for c in sequence]
        c_max = max(sequence)
        c_min = min(sequence)

        available_width = self.width

        # In case the sequence is divergent and has less than n_points elements
        if len(sequence) < self.n_points:
            n_points = len(sequence)
        else:
            n_points = self.n_points

        screen_sequence = []
        for i in range(n_points):
            if c_max - c_min > 0:
                # Linear two point form used to scale a fractal coordinate to a screen coordinate
                y = round((self.height - self.buffer) / (c_max - c_min) *
                          (sequence[i] - c_min)) + self.p1[1]
                x = round(self.buffer + i * available_width / n_points + self.p1[0])
                screen_sequence.append((x, y))

        for i in range(len(screen_sequence) - 1):
            self.shapes.append(pyglet.shapes.Line(screen_sequence[i][0],
                                                  screen_sequence[i][1],
                                                  screen_sequence[i + 1][0],
                                                  screen_sequence[i + 1][1],
                                                  color=[255, 0, 255],
                                                  width=1, batch=self.batch))
            self.shapes.append(pyglet.shapes.Circle(screen_sequence[i][0],
                                                    screen_sequence[i][1],
                                                    radius=3,
                                                    batch=self.batch))

        if isinstance(sequence, list):
            pass
        else:  # Graph -- cyclic
            pass

    def clear_batch(self) -> None:
        """Clears the batch, removing the cycle-graph from the screen"""
        self.shapes = []

    def increase_disp_cycles(self, n: int = 10) -> None:
        """
        Used to increase the number of displayed cycles
        """
        if 0 < self.n_points + n < 512:
            self.n_points += n

    def decrease_disp_cycles(self, n: int = 10) -> None:
        """
        Used to decrease the number of displayed cycles
        """
        if 0 < self.n_points - n < 512:
            self.n_points -= n
