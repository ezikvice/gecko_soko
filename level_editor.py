import json

import pyglet
from pyglet import clock
from pyglet.window import key
from pyglet.window import mouse

import JsonCell
import game_metric
import game_objects
import gamefield
from fileDialogs import FileOpenDialog
from fileDialogs import FileSaveDialog


class LevelEditor:
    selected_figure = None
    editor_figures = []
    game_field = gamefield.GameField()
    gamefield_batch = pyglet.graphics.Batch()
    grid_batch = pyglet.graphics.Batch()
    editor_batch = pyglet.graphics.Batch()

    def __init__(self):
        self.set_editor_objects()
        load_level("levels/0.json", self.game_field, self.gamefield_batch)

    def set_selected(self, figure):
        self.selected_figure = figure

    def set_editor_objects(self):
        tree = game_objects.Tree(self.editor_batch, [1, 10])
        self.editor_figures.append(tree)
        brick = game_objects.Brick(self.editor_batch, [1, 11])
        self.editor_figures.append(brick)
        box = game_objects.Box(self.editor_batch, [2, 10])
        self.editor_figures.append(box)
        box_target = game_objects.BoxTarget(self.editor_batch, [2, 11])
        self.editor_figures.append(box_target)
        player = game_objects.Player(self.editor_batch, [3, 10])
        self.editor_figures.append(player)

    def clear_level(self):
        self.game_field.cells.clear()

    def load_level_dialog(self):
        open_dialog = FileOpenDialog(filetypes=[("JSON", ".json"), ("LVL", ".lvl")], multiple=False)
        open_dialog.open()

        @open_dialog.event
        def on_dialog_open(filename):
            # label.text = 'loading level'
            self.clear_level()
            load_level(filename, self.game_field, self.gamefield_batch)

    def save_level(self):
        # root = Tk()
        # root.filename = asksaveasfilename(title='Save file', filetypes=[('level files', '*.lvl')], defaultextension='.lvl')
        # if not root.filename: return

        save_as = FileSaveDialog(initial_file="test", filetypes=[('level files', '*.lvl')])
        save_as.open()

        @save_as.event
        def on_dialog_save(filename):
            print("FILENAMES ON SAVE!", filename)

            with open(filename, 'w', encoding='utf-8') as f:
                json_cells = []
                for cell in self.game_field.cells:
                    if 0 <= cell[0] < game_metric.ROWS_NUM and 0 <= cell[1] < game_metric.COLUMNS_NUM:
                        json_cell = JsonCell.JsonCell(cell[0], cell[1])
                        json_cell.objects = self.game_field.cells[(json_cell.r, json_cell.c)]
                        json_cells.append(json_cell)

                splitted_name = f.name.split('/')
                name_with_extension = splitted_name[len(splitted_name) - 1]
                name = name_with_extension.split('.')[0]
                json_level = {}
                json_level.setdefault("level", name)
                json_level.setdefault("cells", json_cells)

                json.dump(json_level, f, cls=JsonCell.JsonCellEncoder, ensure_ascii=False, indent=4)
                return 'saved'

    def draw(self):
        window.clear()
        self.editor_batch.draw()
        self.grid_batch.draw()
        self.gamefield_batch.draw()
        label.draw()

    def set_selected_figure_on_gamefield(self, figure, row, column):
        figure.row = row
        figure.column = column
        current_cell = row, column
        obj_set = set()
        if self.game_field.cells.get((row, column)) is not None:
            obj_set = self.game_field.cells[(row, column)]

        obj_set.add(game_objects.build_game_object(figure.obj_id, current_cell, LevelEditor.gamefield_batch))
        self.game_field.cells.setdefault((row, column), obj_set)

        print(self.game_field.cells.get((row, column)))

        label.text = "figure #" + str(figure)
        print("figure #" + str(figure))

    def clear_field_under_cursor(self, x, y):
        row, column = gamefield.get_cell_by_coords(x, y)
        current_objects = self.game_field.cells.get((row, column))
        if current_objects is not None:
            label.text = 'clear field under cursor'
            self.game_field.cells.pop((row, column))


def change_cursor(sprt):
    # TODO: делать (или передавать копию картинки, а не менять исходный объект)
    img = sprt
    # img.scale = 1.1
    # img.opacity = 128
    current_cursor = pyglet.window.ImageMouseCursor(img.image, img.width / 2, img.height / 2)
    window.set_mouse_cursor(current_cursor)


def check_figure_under_mouse(x, y, figures_array):
    for figure in figures_array:
        if figure.x <= x <= figure.x + figure.width and figure.y <= y <= figure.y + figure.height:
            label.text = "figure #" + str(figure.obj_id)
            change_cursor(figure)
            level_editor.set_selected(figure)
            print("selected: " + str(level_editor.selected_figure))


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


# @save_as.event
# def on_dialog_save(filename):
#    print("FILENAMES ON SAVE! FROM SAVE_AS EVENT", filename)


def update(dt):
    pass


level_editor = LevelEditor()

window = pyglet.window.Window(width=800, height=640, caption="Level Editor")
window.set_mouse_visible()

label = pyglet.text.Label('', font_name='Times New Roman', font_size=16, x=410, y=10,
                          anchor_x='right', anchor_y='baseline')

clock.schedule(update)
grid_array = []
gamefield.draw_grid(LevelEditor.grid_batch, grid_array)


@window.event
def on_draw():
    level_editor.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        if gamefield.is_mouse_on_gamefield(x, y):
            # ставим выделенную фигуру
            row, column = gamefield.get_cell_by_coords(x, y)
            try:
                level_editor.set_selected_figure_on_gamefield(level_editor.selected_figure, row, column)
            except AttributeError:
                print("Объект не выделен")
        else:
            check_figure_under_mouse(x, y, level_editor.editor_figures)
            print(level_editor.selected_figure)
    elif button == mouse.RIGHT:
        if level_editor.selected_figure is None:
            level_editor.clear_field_under_cursor(x, y)
        else:
            level_editor.selected_figure = None
            label.text = 'right: {0}, is mouse on gamefield: {1}' \
                .format(gamefield.get_cell_by_coords(x, y), gamefield.is_mouse_on_gamefield(x, y))
            window.set_mouse_cursor(window.CURSOR_DEFAULT)


@window.event
def on_key_press(symbol, modifiers):
    print("symbol:" + str(symbol))
    print("modifiers", str(modifiers))
    if symbol == key.S:
        if modifiers & key.MOD_CTRL:
            level_editor.save_level()
            label.text = 'level saved'
    if symbol == key.L:
        if modifiers & key.MOD_CTRL:
            level_editor.load_level_dialog()


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & mouse.LEFT:
        row, column = gamefield.get_cell_by_coords(x, y)

        level_editor.set_selected_figure_on_gamefield(level_editor.selected_figure, row, column)
        label.text = 'x: {0}, y:{1}, dx:{2}, dy:{3}'.format(x, y, dx, dy)
        # print('x: {0}, y:{1}, dx:{2}, dy:{dy}'.format(x, y, dx, dy))


pyglet.app.run()
