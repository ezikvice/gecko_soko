# менеджер уровней умеет работать с уровнями игры. Сохранять, загружать уровень
import json
from tkinter import Tk, filedialog

import game_metric
import game_objects
import jsoncell


def open_level(filename, editor, batch):
    with open(filename) as f:
        d = json.load(f)
        editor.level = int(d["level"])
        cells_dict = d["cells"]

        for cell in cells_dict:
            r = cell["r"]
            c = cell["c"]
            obj_set = set()
            for obj_id in cell["objects"]:
                obj_set.add(
                    game_objects.build_game_object(obj_id, [r, c], batch))
                editor.cells.setdefault((r, c), obj_set)


def save_level(editor):
    root = Tk()
    root.withdraw()
    root.filename = filedialog.asksaveasfilename(initialdir="./levels/",
                                                 title="Select file",
                                                 filetypes=[('level files',
                                                             '*.json')])
    print("FILENAMES ON SAVE!", root.filename)

    with open(root.filename, 'w', encoding='utf-8') as f:
        json_cells = []
        for cell in editor.game_field.cells:
            if 0 <= cell[0] < game_metric.ROWS_NUM \
                    and 0 <= cell[1] < game_metric.COLUMNS_NUM:
                json_cell = jsoncell.JsonCell(cell[0], cell[1])
                json_cell.objects = editor.game_field.cells[
                    (json_cell.r, json_cell.c)]
                json_cells.append(json_cell)

        splitted_name = f.name.split('/')
        name_with_extension = splitted_name[len(splitted_name) - 1]
        name = name_with_extension.split('.')[0]
        json_level = {}
        json_level.setdefault("level", name)
        json_level.setdefault("cells", json_cells)

        json.dump(json_level, f, cls=jsoncell.JsonCellEncoder,
                  ensure_ascii=False, indent=4)
        return 'saved'
