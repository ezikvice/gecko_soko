import numpy as np
import pyglet
import pyglet.sprite as sprite

import resources as res
from game_metric import *

__author__ = 'Dmitry'


# TODO: разобраться с row, column. возможно, лучше сразу хранить в тупле rc например
# TODO: game_metric вынести в конфиг (может, даже в настройки уровня)

class GameObject(sprite.Sprite):
    def __init__(self, img, obj_id, batch, group, row_column):
        row, column = row_column
        super(GameObject, self).__init__(img, column * CELL_SIZE,
                                         WIN_HEIGHT - row * CELL_SIZE,
                                         batch=batch, group=group)
        self.column = column
        self.row = row
        self.obj_id = obj_id

    def __eq__(self, other):
        if not isinstance(other, GameObject):
            return NotImplemented
        return self.obj_id == other.obj_id

    def __hash__(self):
        return hash(self.obj_id)

    def move(self, direction):
        next_cell = np.add([self.row, self.column], direction)
        next_cell.tolist()
        row, column = next_cell
        self.column = column
        self.row = row
        pos = (column * CELL_SIZE, WIN_HEIGHT - row * CELL_SIZE)
        self.position = pos

    def get_position(self):
        # для удобства сначала строка, потом колонка
        return str(self.row), str(self.column)


class Player(GameObject):
    def __init__(self, batch, row_column):
        super(Player, self).__init__(res.player, obj_id=1, batch=batch,
                                     group=pyglet.graphics.OrderedGroup(2),
                                     row_column=row_column)

    views = {'up': res.player, 'down': res.player_down, 'left': res.player_left,
             'right': res.player_right}

    # TODO: научиться правильно поворачивать игрока (может, загружать в один большой спрайт и оттуда тягать по фреймам)
    for key in views:
        views[key].anchor_x = 0
        views[key].anchor_y = 0


class Tree(GameObject):
    """деревья (для красоты)"""

    def __init__(self, batch, row_column):
        super(Tree, self).__init__(res.pinetree, 2, batch,
                                   pyglet.graphics.OrderedGroup(0), row_column)

    def __str__(self):
        return "tree: r=" + str(self.row) + ", c=" + str(self.column)


class Brick(GameObject):
    """кирпичная стена"""

    def __init__(self, batch, row_column):
        super(Brick, self).__init__(res.brick, 3, batch,
                                    pyglet.graphics.OrderedGroup(0), row_column)

    def __str__(self):
        return "brick: r=" + str(self.row) + ", c=" + str(self.column)


class Box(GameObject):
    """ящик"""

    def __init__(self, batch, row_column):
        super(Box, self).__init__(res.box, 4, batch,
                                  pyglet.graphics.OrderedGroup(0), row_column)

    def __str__(self):
        return "box: r=" + str(self.row) + ", c=" + str(self.column)


class BoxTarget(GameObject):
    """место, куда надо поставить ящик"""

    def __init__(self, batch, row_column):
        super(BoxTarget, self).__init__(res.target, 10, batch,
                                        pyglet.graphics.OrderedGroup(1),
                                        row_column)

    def __str__(self):
        return "box target: r=" + str(self.row) + ", c=" + str(self.column)


def build_game_object(o_id, cell_coords, batch):
    if o_id == 1:
        return Player(batch, cell_coords)
    elif o_id == 2:
        return Tree(batch, cell_coords)
    elif o_id == 3:
        return Brick(batch, cell_coords)
    elif o_id == 4:
        return Box(batch, cell_coords)
    elif o_id == 10:
        return BoxTarget(batch, cell_coords)
