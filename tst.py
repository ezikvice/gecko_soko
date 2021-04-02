import ast
import configparser

import pyglet
import pyglet.sprite as sprite
from pyglet import clock
from pyglet.window import mouse

import game_objects
import resources as res

__author__ = 'Dmitry'

pyglet.resource.path = ["res"]
pyglet.resource.reindex()

batch = pyglet.graphics.Batch()
editor_batch = pyglet.graphics.Batch()


def save_level(filename, game_object):
    # lets create that config file for next time...
    cfgfile = open(filename, 'w')

    cfg = configparser.ConfigParser()
    # add the settings to the structure of the file, and lets write it out...
    cfg.add_section('GameObjects')
    cfg.set('GameObjects', 'trees', ', '.join(str(x.get_position()) for x in game_object.trees))
    cfg.set('GameObjects', 'bricks', ', '.join(str(x.get_position()) for x in game_object.bricks))
    cfg.set('GameObjects', 'boxes', ', '.join(str(x.get_position()) for x in game_object.boxes))
    cfg.set('GameObjects', 'box_targets', ', '.join(str(x.get_position()) for x in game_object.box_targets))
    cfg.set('GameObjects', 'player', str(game_object.player))
    cfg.write(cfgfile)
    cfgfile.close()


def load_level(levelnumber, g_o):
    opencfg = configparser.ConfigParser()
    opencfg.read("levels/" + levelnumber + ".ini")

    # ast.literal_eval приводит строку к простым типам питона
    # (в данном случае в список позиций - туплу, в которой тупла)
    trees_list = ast.literal_eval(opencfg.get("GameObjects", 'trees'))
    # заполняем массив деревьев с помощью генераторного выражения
    g_o.trees = [game_objects.Tree(batch, current_cell) for current_cell in trees_list]

    g_o.bricks = [game_objects.Brick(batch, current_cell) for current_cell in
                           ast.literal_eval(opencfg.get("GameObjects", 'bricks'))]
    g_o.boxes = [game_objects.Box(batch, current_cell) for current_cell in
                          ast.literal_eval(opencfg.get("GameObjects", 'boxes'))]
    g_o.box_targets = [game_objects.BoxTarget(batch, current_cell) for current_cell in
                                ast.literal_eval(opencfg.get("GameObjects", 'box_targets'))]

    player_coords = ast.literal_eval(opencfg.get("GameObjects", 'player'))
    g_o.player = player_coords

    return game_objects


class ObjectsRepository:
    trees = []
    bricks = []
    boxes = []
    box_targets = []
    player = (0, 0)


ob = ObjectsRepository()

load_level("1", ob)
save_level("levels/test.ini", ob)


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


# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)

pyglet.app.run()
