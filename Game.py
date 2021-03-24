import numpy as np

__author__ = 'Dmitry'


class Game:
    CELL_SIZE = 64
    ROWS_NUM = 9
    COLUMNS_NUM = 9
    WIN_WIDTH = 640
    WIN_HEIGHT = 640 - CELL_SIZE

    trees = []
    bricks = []
    boxes = []
    box_targets = []

    def can_move(self, obj, direction):
        # проверяем не кирпич ли это
        next_cell = np.add([obj.row, obj.column], direction)
        next_cell.tolist()
        r, c = next_cell
        if self.get_obj_by_coords(self.bricks, r, c):
            return False
        else:
            # проверяем, если это ящик, то что за ним
            old_r = r
            old_c = c
            if self.get_obj_by_coords(self.boxes, r, c):
                next_cell = np.add(next_cell, direction)
                next_cell.tolist()
                r, c = next_cell
                if self.get_obj_by_coords(self.boxes, r, c) or self.get_obj_by_coords(self.bricks, r, c):
                    return False
                else:
                    box = self.get_obj_by_coords(self.boxes, old_r, old_c)
                    box.move(direction)
        return True

    def get_obj_by_coords(self, objects, r, c):
        for obj in objects:
            if obj.row == r and obj.column == c:
                return obj
