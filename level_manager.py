# TODO: менеджер уровней умеет работать с уровнями игры. Сохранять, загружать уровень
#
import json


def load_level(filename, editor, batch):
    with open(filename) as f:
        d = json.load(f)
        editor.level = int(d["level"])
        cells_dict = d["cells"]
        # print(cell)

        for cell in cells_dict:
            r = cell["r"]
            c = cell["c"]
            obj_set = set()
            for obj_id in cell["objects"]:
                obj_set.add(gamefield.build_game_object(obj_id, [r, c], batch))
                editor.cells.setdefault((r, c), obj_set)
        # print(game_level.cells)
