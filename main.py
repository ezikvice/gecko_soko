import numpy as np
import pyglet
from pyglet.window import key

import game_objects
import gamefield
from game_metric import *

__author__ = 'Dmitry'

# TODO: сделать нормальный расчет координат. сейчас неправильно считаются

pyglet.resource.path = ["res"]
pyglet.resource.reindex()

batch = pyglet.graphics.Batch()

game_level = gamefield.GameField()
# game_field.music.play()


def show_victory():
    label2.text = 'VICTORY!'


def load_next_level(level_number, game_level, batch):
    try:
        gamefield.load_level(str(level_number), game_level, batch)
        game_level.player = gamefield.find_player(game_level.cells)
    except IOError:
        print("END GAME")
        show_victory()


load_next_level(1, game_level, batch)


window = pyglet.window.Window(width=(CELL_SIZE * 10), height=(CELL_SIZE * 10), caption="Gecko Soko")
window.set_mouse_visible(True)

fps_display = pyglet.window.FPSDisplay(window)
fps_display.label.y = 0

label = pyglet.text.Label('[{0}, {1}]'.format(game_level.player.row, game_level.player.column),
                          font_name='Times New Roman',
                          font_size=36,
                          x=410, y=10,
                          anchor_x='right', anchor_y='baseline')

label2 = pyglet.text.Label('',
                           font_name='Times New Roman',
                           font_size=64,
                           color=(255, 0, 0, 255),
                           x=550, y=310,
                           anchor_x='right', anchor_y='baseline')


def show_coords():
    label.text = '[{0}, {1}]'.format(game_level.player.row, game_level.player.column)
    label2.text = ''
    # print(game_level.cells)


def is_figure_in_cell(figure, cell):
    cell_set = game_level.cells.get((cell[0], cell[1]))
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
            if is_figure_in_cell(game_objects.Box(None, next_cell), next_cell) or is_figure_in_cell(
                    game_objects.Brick(None, next_cell), next_cell):
                return False
            else:
                old_obj_set = game_level.cells.get((old_r, old_c))
                box = get_object_in_set(game_objects.Box, old_obj_set)
                old_obj_set.remove(box)
                if len(old_obj_set) == 0:
                    del game_level.cells[(old_r, old_c)]
                box.move(direction)
                next_cell_objects = game_level.cells.get((next_cell[0], next_cell[1]))
                if next_cell_objects is None:
                    next_obj_set = set()
                else:
                    next_obj_set = set(game_level.cells.get((next_cell[0], next_cell[1])))
                next_obj_set.add(box)
                game_level.cells[(next_cell[0], next_cell[1])] = next_obj_set
    return True


# если во всех мишенях коробки, то возвращаем True и показываем, что уровень пройден
# TODO: переход на следующий уровень и если уровней больше не осталось, то победа!
def check_win():
    for cell in game_level.cells:
        if game_objects.BoxTarget(None, (0, 0)) in game_level.cells[cell] \
                and game_objects.Box(None, (0, 0)) not in game_level.cells[cell]:
            return False
    return True


def get_object_in_set(needed_object, obj_set):
    for obj in obj_set:
        if obj is not None:
            if isinstance(obj, needed_object):
                return obj
    return None


@window.event
def on_text_motion(motion):
    if motion == key.MOTION_UP:  # координаты по y обращены для удобства
        direction = [-1, 0]
        if can_move(game_level.player, direction):
            game_level.player.image = game_level.player.views['up']
            game_level.player.move(direction)
        show_coords()
        if check_win():
            # label2.text = 'VICTORY!'
            load_next_level(game_level.level + 1, game_level, batch)
    if motion == key.MOTION_DOWN:  # координаты по y обращены для удобства
        direction = [1, 0]
        if can_move(game_level.player, direction):
            game_level.player.image = game_level.player.views['down']
            game_level.player.move(direction)
        show_coords()
        if check_win():
            # label2.text = 'VICTORY!'
            load_next_level(game_level.level + 1, game_level, batch)
    if motion == key.MOTION_LEFT:
        direction = [0, -1]
        if can_move(game_level.player, direction):
            game_level.player.image = game_level.player.views['left']
            game_level.player.move(direction)
        show_coords()
        if check_win():
            # label2.text = 'VICTORY!'
            load_next_level(game_level.level + 1, game_level, batch)
    if motion == key.MOTION_RIGHT:
        direction = [0, 1]
        if can_move(game_level.player, direction):
            game_level.player.image = game_level.player.views['right']
            game_level.player.move(direction)
        show_coords()
        if check_win():
            # label2.text = 'VICTORY!'
            load_next_level(game_level.level + 1, game_level, batch)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.M:
        game_level.music.pause()
    if symbol == key.P:
        game_level.music.play()
    if symbol == key.PAGEUP:
        game_level.music.volume += 0.05
    if symbol == key.PAGEDOWN:
        game_level.music.volume -= 0.05


@window.event
def on_draw():
    window.clear()
    batch.draw()
    label.draw()
    label2.draw()
    fps_display.draw()


def update(dt):
    pass


# pyglet.clock.set_fps_limit(60)
pyglet.clock.schedule_interval(update, 1 / 120)

pyglet.app.run()
