import pyglet
import pyglet.sprite as sprite
from pyglet import clock
from pyglet.window import mouse

import gamefield
import resources as res

__author__ = 'Dmitry'

pyglet.resource.path = ["res"]
pyglet.resource.reindex()

batch = pyglet.graphics.Batch()
editor_batch = pyglet.graphics.Batch()


class ObjectsRepository:
    trees = []
    bricks = []
    boxes = []
    box_targets = []
    player = (0, 0)
    level = 0


ob = ObjectsRepository()
gamefield.load_level("test", ob, batch)

tree = sprite.Sprite(res.pinetree, 630, 500, batch=editor_batch)

window = pyglet.window.Window(width=800, height=640, caption="Gecko Soko")
image = res.target
cursor = pyglet.window.ImageMouseCursor(image, 16, 8)
window.set_mouse_cursor(cursor)

label = pyglet.text.Label('',
                          font_name='Times New Roman',
                          font_size=36,
                          x=410, y=10,
                          anchor_x='right', anchor_y='baseline')


def update(dt):
    # tree.rotation += 100*dt
    pass


clock.schedule(update)


@window.event
def on_draw():
    window.clear()
    batch.draw()
    editor_batch.draw()
    label.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        label.text = 'left: {0}:{1}'.format(x, y)


gamefield.save_level("levels/test.ini", ob, "test")

# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)

pyglet.app.run()

