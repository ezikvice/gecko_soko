__author__ = 'Dmitry'

import ast
import configparser
import json

import numpy as np
import pyglet.media as media
import pyglet.shapes as shapes

import game_objects
import resources as res


# TODO: все-таки, где располагаются объекты, должно храниться не в объектах а в игровом поле

# TODO: игровое поле представляет собой двумерный массив ячеек, а ячейка содержит в себе список игровых объектов
# {{row, column}:[game_objects]}


class GameField:
    CELL_SIZE = 64
    ROWS_NUM = 9
    COLUMNS_NUM = 9
    WIN_WIDTH = 640
    WIN_HEIGHT = 640 - CELL_SIZE

    trees = []
    bricks = []
    boxes = []
    box_targets = []

    # игровое поле хранится в формате {(row, column1): [set, of, game_objects]}
    cells = {}

    music = media.Player()

    def __init__(self):
        source = res.backmusic
        self.music.volume = 0.3
        self.music.queue(source)
        self.music.loop = True
        # self.music.play()

    # TODO: скорее всего можно улучшить
    def can_move(self, obj, direction):
        # проверяем не кирпич ли это
        next_cell = np.add([obj.row, obj.column], direction)
        next_cell.tolist()
        r, c = next_cell
        if get_obj_by_cell(self.bricks, r, c):
            return False
        else:
            # проверяем, если это ящик, то что за ним
            old_r = r
            old_c = c
            if get_obj_by_cell(self.boxes, r, c):
                next_cell = np.add(next_cell, direction)
                next_cell.tolist()
                r, c = next_cell
                if self.get_obj_by_cell(self.boxes, r, c) or self.get_obj_by_cell(self.bricks, r, c):
                    return False
                else:
                    box = self.get_obj_by_cell(self.boxes, old_r, old_c)
                    box.move(direction)
        return True


def get_obj_by_cell(self, objects, r, c):
    for obj in objects:
        if obj.row == r and obj.column == c:
            return obj


def load_level(level_number, level_objects, batch):
    opencfg = configparser.ConfigParser()
    opencfg.read("levels/" + level_number + ".ini")

    # ast.literal_eval приводит строку к простым типам питона
    # (в данном случае в список позиций - туплу, в которой тупла)
    trees_list = ast.literal_eval(opencfg.get("GameObjects", 'trees'))
    # заполняем массив деревьев с помощью генераторного выражения
    level_objects.trees = [game_objects.Tree(batch, current_cell) for current_cell in trees_list]

    level_objects.bricks = [game_objects.Brick(batch, current_cell) for current_cell in
                            ast.literal_eval(opencfg.get("GameObjects", 'bricks'))]
    level_objects.boxes = [game_objects.Box(batch, current_cell) for current_cell in
                           ast.literal_eval(opencfg.get("GameObjects", 'boxes'))]
    level_objects.box_targets = [game_objects.BoxTarget(batch, current_cell) for current_cell in
                                 ast.literal_eval(opencfg.get("GameObjects", 'box_targets'))]

    level_objects.player = ast.literal_eval(opencfg.get("GameObjects", 'player'))
    # player_coords = ast.literal_eval(opencfg.get("GameObjects", 'player'))
    # g_o.player = player_coords

    return game_objects


def build_game_object(o_id, cell_coords, batch):
    if o_id == 1:
        return game_objects.Player(batch, cell_coords)
    elif o_id == 2:
        return game_objects.Tree(batch, cell_coords)
    elif o_id == 3:
        return game_objects.Brick(batch, cell_coords)
    elif o_id == 4:
        return game_objects.Box(batch, cell_coords)
    elif o_id == 10:
        return game_objects.BoxTarget(batch, cell_coords)


def load_level2(level_number, cells, batch):
    with open('levels/' + level_number + '.json') as f:
        d = json.load(f)
        cells_dict = d["cells"]
        # print(cell)

        for cell in cells_dict:
            r = cell["r"]
            c = cell["c"]
            num_arr = cell["objects"]
            obj_set = set()
            for obj_id in num_arr:
                obj_set.add(build_game_object(obj_id, [r, c], batch))
                cells.setdefault((r, c), obj_set)
        print(cells)


def get_cell_by_coords(x, y):
    row = GameField.ROWS_NUM - y // GameField.CELL_SIZE
    column = x // GameField.CELL_SIZE
    return row, column


def find_player(cells):
    for cell in cells:
        if cells[cell] is not None:
            for obj in cells[cell]:
                if isinstance(obj, game_objects.Player):
                    return obj
    return None


# TODO: можно через get_cell_by_coords
def is_mouse_on_gamefield(x, y):
    if (x // GameField.CELL_SIZE < GameField.COLUMNS_NUM) & (
            (GameField.COLUMNS_NUM - y // GameField.CELL_SIZE) < GameField.ROWS_NUM):
        return True
    return False


def draw_grid(batch, lines_arr):
    # grid_color = (250, 225, 30) # желтый
    # grid_color = (255, 0, 144) # магента
    # grid_color = (0, 200, 255) # голубой
    grid_color = (0, 255, 255)  # циан
    for i in range(GameField.ROWS_NUM + 1):
        lines_arr.append(shapes.Line(GameField.CELL_SIZE * i + 1, 640 - 1,
                                     GameField.CELL_SIZE * i + 1,
                                     640 - GameField.COLUMNS_NUM * GameField.CELL_SIZE - 1,
                                     width=1, color=grid_color, batch=batch))
    for i in range(GameField.COLUMNS_NUM + 1):
        lines_arr.append(shapes.Line(1, 640 - GameField.CELL_SIZE * i - 1,
                                     GameField.COLUMNS_NUM * GameField.CELL_SIZE + 1,
                                     640 - GameField.CELL_SIZE * i - 1,
                                     width=1, color=grid_color, batch=batch))
    # batch.draw()
