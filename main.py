import numpy as np
import pyglet
from pyglet.window import key

import gamefield
import undo_redo as history
from game_objects import Box, Brick, BoxTarget
from ui_manager import UiManager


def main():
    global undo_redo, lvl
    pyglet.resource.path = ["res"]
    pyglet.resource.reindex()

    undo_redo = history.UndoRedo()

    lvl = gamefield.GameField()
    load_next_level(1, lvl)

    # game_field.music.play()

    UiManager.window.set_mouse_visible(True)
    UiManager.fps_display.label.y = 0


def load_next_level(level_number, game_level):
    try:
        game_level.load_level(str(level_number))
        game_level.player = gamefield.find_player(game_level.cells)
        undo_redo.clear_history()
        UiManager.show_level(level_number)
    except IOError:
        print("END GAME")
        UiManager.show_victory()


def is_figure_in_cell(figure, cell):
    cell_set = lvl.cells.get((cell[0], cell[1]))
    if cell_set is not None and figure in cell_set:
        return True
    return False


def is_brick_in_cell(cell):
    return is_figure_in_cell(Brick(None, cell), cell)


def is_box_in_cell(cell):
    return is_figure_in_cell(Box(None, cell), cell)


def can_move(obj, direction):
    # проверяем не кирпич ли в нашем направлении
    next_cell = np.add([obj.row, obj.column], direction)
    r, c = next_cell.tolist()
    if is_brick_in_cell(next_cell):
        return False
    else:
        # проверяем, если это ящик, то что за ним
        old_r = r
        old_c = c
        if is_box_in_cell(next_cell):
            next_cell = np.add(next_cell, direction)
            next_cell.tolist()
            if is_box_in_cell(next_cell) or \
                    is_brick_in_cell(next_cell):
                return False
            else:
                old_obj_set = lvl.cells.get((old_r, old_c))
                box = get_object_in_set(Box, old_obj_set)
                undo_redo.add_to_history(lvl.cells)
                old_obj_set.remove(box)
                if len(old_obj_set) == 0:
                    del lvl.cells[(old_r, old_c)]
                box.move(direction)
                next_cell_objects = lvl.cells.get((next_cell[0], next_cell[1]))
                if next_cell_objects is None:
                    next_obj_set = set()
                else:
                    next_obj_set = set(
                        lvl.cells.get((next_cell[0], next_cell[1])))
                next_obj_set.add(box)
                lvl.cells[(next_cell[0], next_cell[1])] = next_obj_set
    return True


# если во всех мишенях коробки, то возвращаем True и показываем, что уровень пройден
def check_win():
    for cell in lvl.cells:
        if BoxTarget(None, (0, 0)) in lvl.cells[cell] \
                and Box(None, (0, 0)) not in lvl.cells[cell]:
            return False
    return True


def get_object_in_set(needed_object, obj_set):
    for obj in obj_set:
        if obj is not None:
            if isinstance(obj, needed_object):
                return obj
    return None


def move_player(motion):
    motions = {key.MOTION_UP: [-1, 0], key.MOTION_DOWN: [1, 0],
               key.MOTION_LEFT: [0, -1], key.MOTION_RIGHT: [0, 1]}

    player_views = {key.MOTION_UP: 'up', key.MOTION_DOWN: 'down',
                    key.MOTION_LEFT: 'left', key.MOTION_RIGHT: 'right'}

    if motion in motions.keys():
        direction = motions.get(motion)
        if can_move(lvl.player, direction):
            lvl.player.image = lvl.player.views[player_views.get(motion)]
            lvl.player.move(direction)
        if check_win():
            load_next_level(lvl.level + 1, lvl)


@UiManager.window.event
def on_draw():
    UiManager.draw_all()


@UiManager.window.event
def on_text_motion(motion):
    move_player(motion)


@UiManager.window.event
def on_key_press(symbol, modifiers):
    if symbol == key.M:
        lvl.music.pause()
    if symbol == key.P:
        lvl.music.play()
    if symbol == key.PAGEUP:
        lvl.music.volume += 0.05
    if symbol == key.PAGEDOWN:
        lvl.music.volume -= 0.05
    if symbol == key.Z:
        if modifiers & key.MOD_CTRL:
            print("undo()")
            undo_redo.show_history()


def update(dt):
    pass


# наверное, надо удалить закомментированное
# pyglet.clock.set_fps_limit(60)
# pyglet.clock.schedule_interval(update, 1 / 120)
main()
pyglet.app.run()
