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
# game_field.music.play()

gamefield.load_level2("2", game_field.cells, batch)
# player = game_objects.Player(None, ob.player)
player = gamefield.find_player(game_field.cells)

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


def is_figure_in_cell(figure, cell):
    cell_set = game_field.cells.get((cell[0], cell[1]))
    if cell_set is not None and figure in cell_set:
        return True
    return False


def can_move(obj, direction):
    # проверяем не кирпич ли в нашем направлении
    next_cell = np.add([obj.row, obj.column], direction)
    next_cell.tolist()
    r, c = next_cell
    if is_figure_in_cell(game_objects.Brick(None, next_cell), next_cell):
        return False
    else:
        # проверяем, если это ящик, то что за ним
        old_r = r
        old_c = c
        if is_figure_in_cell(game_objects.Box(None, next_cell), next_cell):
            next_cell = np.add(next_cell, direction)
            next_cell.tolist()
            if is_figure_in_cell(game_objects.Box(None, next_cell), next_cell) or is_figure_in_cell(game_objects.Brick(None, next_cell), next_cell):
                return False
            else:
                box = get_object_by_coords(game_objects.Box, game_field.cells.get((old_r, old_c)))
                box.move(direction)
                obj_set = set(game_field.cells.get((old_r, old_c)))
                obj_set.remove(box)
                next_cell = np.add(next_cell, direction)
                next_cell.tolist()
                next_cell_objects = game_field.cells.get((next_cell[0], next_cell[1]))
                if next_cell_objects is None:
                    obj_set = set()
                else:
                    obj_set = set(game_field.cells.get((next_cell[0], next_cell[1])))
                obj_set.add(box)
                game_field.cells.setdefault((next_cell[0], next_cell[1]), obj_set)
    return True


# если во всех мишенях коробки, то возвращаем True и показываем, что уровень пройден
# TODO: переход на следующий уровень и если уровней больше не осталось, то победа!
# def check_win():
#     count = 0
#     for target in box_targets:
#         for box in boxes:
#             if box.get_position() == target.get_position():
#                 count += 1
#     if count == len(box_targets):
#         return True
#     return False


def get_object_by_coords(needed_object, cells):
    for obj in cells:
        if obj is not None:
            if isinstance(obj, needed_object):
                return obj
    return None


@window.event
def on_text_motion(motion):
    if motion == key.MOTION_UP:  # координаты по y обращены для удобства
        direction = [-1, 0]
        if can_move(player, direction):
            player.image = player.views['up']
            player.move(direction)
        show_coords()
        # if check_win():
        #     label2.text = 'VICTORY!'
    if motion == key.MOTION_DOWN:  # координаты по y обращены для удобства
        direction = [1, 0]
        if can_move(player, direction):
            player.image = player.views['down']
            player.move(direction)
        show_coords()
        # if check_win():
        #     label2.text = 'VICTORY!'
    if motion == key.MOTION_LEFT:
        direction = [0, -1]
        if can_move(player, direction):
            player.image = player.views['left']
            player.move(direction)
        show_coords()
        # if check_win():
        #     label2.text = 'VICTORY!'
    if motion == key.MOTION_RIGHT:
        direction = [0, 1]
        if can_move(player, direction):
            player.image = player.views['right']
            player.move(direction)
        show_coords()
        # if check_win():
        #     label2.text = 'VICTORY!'


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
