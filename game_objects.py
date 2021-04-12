import numpy as np
import pyglet.sprite as sprite

import resources as res
from game_metric import *

__author__ = 'Dmitry'


# TODO: разобраться с row, column. возможно, лучше сразу хранить в тупле rc например


class GameObject(sprite.Sprite):
    def __init__(self, img, obj_id, batch, arr):
        row, column = arr
        super(GameObject, self).__init__(img, column * CELL_SIZE, WIN_HEIGHT - row * CELL_SIZE, batch=batch)
        self.column = column
        self.row = row
        self.obj_id = obj_id

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
        return self.row, self.column


class Player(GameObject):
    def __init__(self, batch, arr):
        super(Player, self).__init__(res.player, obj_id=1, batch=batch, arr=arr)

    views = {'up': res.player, 'down': res.player_down, 'left': res.player_left, 'right': res.player_right}

    # TODO: научиться правильно поворачивать игрока (может, загружать в один большой спрайт и оттуда тягать по фреймам)
    for key in views:
        views[key].anchor_x = 0
        views[key].anchor_y = 0


class Tree(GameObject):
    """деревья (для красоты)"""

    def __init__(self, batch, arr):
        super(Tree, self).__init__(res.pinetree, 2, batch, arr)


class Brick(GameObject):
    """кирпичная стена"""

    def __init__(self, batch, arr):
        super(Brick, self).__init__(res.brick, 3, batch, arr)


class Box(GameObject):
    """ящик"""

    def __init__(self, batch, arr):
        super(Box, self).__init__(res.box, 4, batch, arr)


class BoxTarget(GameObject):
    """место, куда надо поставить ящик"""

    def __init__(self, batch, arr):
        super(BoxTarget, self).__init__(res.target, 10, batch, arr)
