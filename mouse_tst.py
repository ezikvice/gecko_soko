import copy

import pyglet
import pyglet.sprite as sprite
from pyglet import clock
from pyglet.window import mouse

import game_objects
import resources as res

__author__ = 'Dmitry'

pyglet.resource.path = ["res"]
pyglet.resource.reindex()

editor_batch = pyglet.graphics.Batch()

figures = []

tree = game_objects.Tree(editor_batch, [1, 10])
figures.append(tree)
brick = game_objects.Brick(editor_batch, [1, 11])
figures.append(brick)
box = game_objects.Box(editor_batch, [2, 10])
figures.append(box)
box_target = game_objects.BoxTarget(editor_batch, [2, 11])
figures.append(box_target)

window = pyglet.window.Window(width=800, height=640, caption="Mouse test")

image = res.target
cursor = pyglet.window.ImageMouseCursor(image, 16, 8)
# window.set_mouse_cursor(cursor)
window.set_mouse_visible()

label = pyglet.text.Label('', font_name='Times New Roman',
                          font_size=36, x=410, y=10,
                          anchor_x='right', anchor_y='baseline')


def change_cursor(sprt):
    # TODO: делать (или передавать копию картинки, а не менять исходный объект)
    img = sprt
    img.opacity = 128
    current_cursor = pyglet.window.ImageMouseCursor(img.image, 0, 0)
    window.set_mouse_cursor(current_cursor)


def check_figure_under_mouse(x, y, figures_array):
    for figure in figures_array:
        if figure.x <= x <= figure.x + figure.width and figure.y <= y <= figure.y + figure.height:
            label.text = "figure #" + str(figure.obj_id)
            change_cursor(figure)


def update(dt):
    pass


clock.schedule(update)


@window.event
def on_draw():
    window.clear()
    editor_batch.draw()
    label.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        label.text = 'left: {0}:{1}'.format(x, y)
        check_figure_under_mouse(x, y, figures)
    elif button == mouse.RIGHT:
        label.text = 'right: {0}:{1}'.format(x, y)


pyglet.app.run()
