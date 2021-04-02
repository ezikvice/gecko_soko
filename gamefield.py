import ast
import configparser

import numpy as np

__author__ = 'Dmitry'

import game_objects


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


def load_level(levelnumber, g_o, batch):
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

