"""
Finn Williams
2021/04/16

Exploring Orbitals in Iterative Fractals

This is the main file of the project. Running this file will setup and start the entire application.
"""
from mandelbrot import MandelbrotSet
from fractal import S_WIDTH, S_HEIGHT
from graphics import *

#############################################################################
# SETUP
#############################################################################

frac_w = round(S_WIDTH * 6 / 10)
frac = MandelbrotSet(frac_w)
frac.im_buffer = 0.2
frac.save_image('fractal_image')

info = PropertiesBox((frac_w, round(S_HEIGHT * 8 / 10)), (S_WIDTH, S_HEIGHT))

c_graph = CyclicGraph((frac_w, round(S_HEIGHT * 2 / 10)), (S_WIDTH, round(S_HEIGHT * 8 / 10)))

buttons = []
buttons.append(Button(c_graph.decrease_disp_cycles,
                      (S_WIDTH - 45, round(S_HEIGHT * 2 / 10) - 25),
                      (S_WIDTH - 20, round(S_HEIGHT * 2 / 10)),
                      '+'))
buttons.append(Button(c_graph.increase_disp_cycles,
                      (S_WIDTH - 70 - 5, round(S_HEIGHT * 2 / 10) - 20),
                      (S_WIDTH - 45 - 5, round(S_HEIGHT * 2 / 10)),
                      '-'))

pic = pyglet.image.load('fractal_image.png')
pic.anchor_y = frac.get_height()

window = pyglet.window.Window(fullscreen=True)

current_seq = [1]

name = pyglet.text.Label('Exploring Orbitals in Iterative Fractals' +
                         '\nFinn Williams' +
                         '\n2021/04/16',
                         bold=False,
                         x=S_WIDTH,
                         y=round(S_HEIGHT * 2 / 10 - 30) // 2,
                         align='center',
                         anchor_x='right', anchor_y='center',
                         multiline=True,
                         width=S_WIDTH - frac_w)


#############################################################################
# RUNTIME LOOP
#############################################################################

@window.event
def on_draw() -> None:
    """
    What to do everytime .draw() is called...
    > Clear the window
    > Draw background image
    > Draw new graphic batch
    > Clear the batch
    """
    window.clear()
    pic.blit(0, S_HEIGHT)
    name.draw()

    info.batch.draw()
    c_graph.batch.draw()
    frac.batch.draw()

    for b in buttons:
        b.batch.draw()


@window.event
def on_key_press(symbol, modifiers) -> None:
    """
    If the escape key is pressed, close the window
    """
    if symbol == pyglet.window.key.ESCAPE:
        window.close()


@window.event
def on_mouse_release(x, y, button, modifiers) -> None:
    """
    When the mouse is released, call the update point function at the location of release
    """
    global current_seq, current_xy
    if button == pyglet.window.mouse.LEFT:
        if x < frac.get_width():
            current_xy = (x, y)

            text, seq = frac.update_point(x, y, 512)
            current_seq = seq

            info.clear_batch()
            info.update(text)
            c_graph.update(seq)
        else:
            for b in buttons:
                b.get_press(x, y)
            c_graph.update(current_seq)
            c_graph.batch.draw()
    frac.batch.draw()


@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers) -> None:
    """
    Continuously update the iteration drawing the the mouse is dragged around the fractal graph
    """
    global current_xy
    if button == pyglet.window.mouse.LEFT:
        if x < frac.get_width():
            current_xy = (x + dx, y + dy)

            frac.update(x + dx, y + dy)
            frac.batch.draw()


# Begin the runtime loop
event_loop = pyglet.app.EventLoop()
pyglet.app.run()
