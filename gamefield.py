__author__ = 'Dmitry'

import json

import pyglet.media as media
import pyglet.shapes as shapes

import game_metric
import game_objects
import resources as res


# TODO: все-таки, где располагаются объекты, должно храниться не в объектах а в игровом поле

# TODO: игровое поле представляет собой двумерный массив ячеек, а ячейка содержит в себе список игровых объектов
# {{row, column}:[game_objects]}


class GameField:
    # игровое поле хранится в формате {(row, column1): [set, of, game_objects]}
    cells = {}
    level = 1
    player = game_objects.Player(None, [0, 0])

    music = media.Player()

    def __init__(self):
        source = res.backmusic
        self.music.volume = 0.3
        self.music.queue(source)
        self.music.loop = True
        # self.music.play()

    def draw_grid(self, batch, lines_arr):
        # grid_color = (250, 225, 30) # желтый
        # grid_color = (255, 0, 144) # магента
        # grid_color = (0, 200, 255) # голубой
        grid_color = (0, 255, 255)  # циан
        for i in range(game_metric.ROWS_NUM + 1):
            lines_arr.append(shapes.Line(game_metric.CELL_SIZE * i + 1, 640 - 1,
                                         game_metric.CELL_SIZE * i + 1,
                                         640 - game_metric.COLUMNS_NUM * game_metric.CELL_SIZE - 1,
                                         width=1, color=grid_color,
                                         batch=batch))
        for i in range(game_metric.COLUMNS_NUM + 1):
            lines_arr.append(shapes.Line(1, 640 - game_metric.CELL_SIZE * i - 1,
                                         game_metric.COLUMNS_NUM * game_metric.CELL_SIZE + 1,
                                         640 - game_metric.CELL_SIZE * i - 1,
                                         width=1, color=grid_color,
                                         batch=batch))

    def clear_level(self):
        self.cells.clear()
        self.player.delete()

    def load_level(self, level_number, batch):
        self.clear_level()
        with open('levels/' + level_number + '.json') as f:
            self.level = int(level_number)
            d = json.load(f)
            cells_dict = d["cells"]
            # print(cell)

            for cell in cells_dict:
                r = cell["r"]
                c = cell["c"]
                obj_set = set()
                for obj_id in cell["objects"]:
                    obj_set.add(game_objects.build_game_object(obj_id, [r, c],
                                                               batch))
                    self.cells.setdefault((r, c), obj_set)
            # print(game_level.cells)

    def get_cell_by_coords(self, x, y):
        row = game_metric.ROWS_NUM - y // game_metric.CELL_SIZE
        column = x // game_metric.CELL_SIZE
        return row, column

    # TODO: можно через get_cell_by_coords
    def is_mouse_on_gamefield(self, x, y):
        if (x // game_metric.CELL_SIZE < game_metric.COLUMNS_NUM) & (
                (
                        game_metric.COLUMNS_NUM - y // game_metric.CELL_SIZE) < game_metric.ROWS_NUM):
            return True
        return False


def find_player(cells):
    for cell in cells:
        if cells[cell] is not None:
            for obj in cells[cell]:
                if isinstance(obj, game_objects.Player):
                    return obj
    return None


def get_object_in_set(needed_object, obj_set):
    for obj in obj_set:
        if obj is not None:
            if isinstance(obj, needed_object):
                return obj
    return None
