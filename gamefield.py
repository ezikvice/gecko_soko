__author__ = 'Dmitry'

import ast
import configparser

import numpy as np
import pyglet.media as media

import game_objects
import resources as res


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

    music = media.Player()

    def __init__(self):
        source = res.backmusic
        self.music.volume = 0.3
        self.music.queue(source)
        self.music.loop = True
        self.music.play()

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


def save_level(filename, game_objects, level):
    # lets create that config file for next time...
    cfgfile = open(filename, 'w')

    cfg = configparser.ConfigParser()
    # add the settings to the structure of the file, and lets write it out...
    cfg.add_section('GameObjects')
    cfg.set('GameObjects', 'trees', ', '.join(str(x.get_position()) for x in game_objects.trees))
    cfg.set('GameObjects', 'bricks', ', '.join(str(x.get_position()) for x in game_objects.bricks))
    cfg.set('GameObjects', 'boxes', ', '.join(str(x.get_position()) for x in game_objects.boxes))
    cfg.set('GameObjects', 'box_targets', ', '.join(str(x.get_position()) for x in game_objects.box_targets))
    cfg.set('GameObjects', 'player', str(game_objects.player))
    cfg.set('GameObjects', 'level', level)
    cfg.write(cfgfile)
    cfgfile.close()


def load_level(level_number, g_o, batch):
    opencfg = configparser.ConfigParser()
    opencfg.read("levels/" + level_number + ".ini")

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

    g_o.player = ast.literal_eval(opencfg.get("GameObjects", 'player'))
    # player_coords = ast.literal_eval(opencfg.get("GameObjects", 'player'))
    # g_o.player = player_coords

    return game_objects
