import numpy as np
import pyglet
from pyglet.window import key

import gamefield
import game_objects
from game_metric import *

__author__ = 'Dmitry'

# TODO: сделать нормальный расчет координат. сейчас неправильно считаются

pyglet.resource.path = ["res"]
pyglet.resource.reindex()


batch = pyglet.graphics.Batch()
layer2 = pyglet.graphics.Batch()

current_cell = 0, 0
game_field = gamefield.GameField()


class ObjectsRepository:
    trees = []
    bricks = []
    boxes = []
    box_targets = []
    player = (0, 0)
    level = 0


ob = ObjectsRepository()
gamefield.load_level("1", ob, batch)
player = game_objects.Player(None, ob.player)
# TODO: избавиться от лишних объектов
trees = ob.trees
bricks = ob.bricks
boxes = ob.boxes
box_targets = ob.box_targets

window = pyglet.window.Window(width=(CELL_SIZE * 10), height=(CELL_SIZE * 10), caption="Gecko Soko")
window.set_mouse_visible(True)

fps_display = pyglet.window.FPSDisplay(window)
fps_display.label.y = 0

label = pyglet.text.Label('[{0}, {1}]'.format(player.row, player.column),
                          font_name='Times New Roman',
                          font_size=36,
                          x=410, y=10,
                          anchor_x='right', anchor_y='baseline')

label2 = pyglet.text.Label('',
                           font_name='Times New Roman',
                           font_size=24,
                           color=(255, 0, 0, 255),
                           x=250, y=10,
                           anchor_x='right', anchor_y='baseline')


def show_coords():
    label.text = '[{0}, {1}]'.format(player.row, player.column)
    label2.text = ''


def can_move(obj, direction):
    # проверяем не кирпич ли это
    next_cell = np.add([obj.row, obj.column], direction)
    next_cell.tolist()
    r, c = next_cell
    if get_obj_by_coords(bricks, r, c):
        return False
    else:
        # проверяем, если это ящик, то что за ним
        old_r = r
        old_c = c
        if get_obj_by_coords(boxes, r, c):
            next_cell = np.add(next_cell, direction)
            next_cell.tolist()
            r, c = next_cell
            if get_obj_by_coords(boxes, r, c) or get_obj_by_coords(bricks, r, c):
                return False
            else:
                box = get_obj_by_coords(boxes, old_r, old_c)
                box.move(direction)
    return True


# если во всех мишенях коробки, то возвращаем True и показываем, что уровень пройден
# TODO: переход на следующий уровень и если уровней больше не осталось, то победа!
def check_win():
    count = 0
    for target in box_targets:
        for box in boxes:
            if box.get_position() == target.get_position():
                count += 1
    if count == len(box_targets):
        return True
    return False


def get_obj_by_coords(objects, r, c):
    for obj in objects:
        if obj.row == r and obj.column == c:
            return obj


@window.event
def on_text_motion(motion):
    if motion == key.MOTION_UP:  # координаты по y обращены для удобства
        direction = [-1, 0]
        if can_move(player, direction):
            player.image = player.views['up']
            player.move(direction)
        show_coords()
        if check_win():
            label2.text = 'VICTORY!'
    if motion == key.MOTION_DOWN:  # координаты по y обращены для удобства
        direction = [1, 0]
        if can_move(player, direction):
            player.image = player.views['down']
            player.move(direction)
        show_coords()
        if check_win():
            label2.text = 'VICTORY!'
    if motion == key.MOTION_LEFT:
        direction = [0, -1]
        if can_move(player, direction):
            player.image = player.views['left']
            player.move(direction)
        show_coords()
        if check_win():
            label2.text = 'VICTORY!'
    if motion == key.MOTION_RIGHT:
        direction = [0, 1]
        if can_move(player, direction):
            player.image = player.views['right']
            player.move(direction)
        show_coords()
        if check_win():
            label2.text = 'VICTORY!'


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.M:
        game_field.music.pause()
    if symbol == key.P:
        game_field.music.play()
    if symbol == key.PAGEUP:
        game_field.music.volume += 0.05
    if symbol == key.PAGEDOWN:
        game_field.music.volume -= 0.05


@window.event
def on_draw():
    window.clear()
    batch.draw()
    player.draw()
    label.draw()
    label2.draw()
    fps_display.draw()


def update(dt):
    pass


# pyglet.clock.set_fps_limit(60)
pyglet.clock.schedule_interval(update, 1 / 120)

pyglet.app.run()
