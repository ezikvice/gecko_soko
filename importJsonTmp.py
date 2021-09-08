import json

import game_objects

cells = {}


def build_game_object(o_id, cell_coords):
    if o_id == 1:
        return game_objects.Player(None, cell_coords)
    elif o_id == 2:
        return game_objects.Tree(None, cell_coords)
    elif o_id == 3:
        return game_objects.Brick(None, cell_coords)
    elif o_id == 4:
        return game_objects.Box(None, cell_coords)
    elif o_id == 10:
        return game_objects.BoxTarget(None, cell_coords)


with open('levels/1.json') as f:
    d = json.load(f)
    cell = d["cell"]
    # print(cell)

    r = cell["r"]
    c = cell["c"]
    num_arr = cell["objects"]
    obj_arr = []
    for obj_id in num_arr:
        obj_arr.append(build_game_object(obj_id, [r, c]))
    cells[(r, c)] = obj_arr
    print(cells.values())



