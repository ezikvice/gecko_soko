import json

import pyglet
from pyglet import clock
from pyglet.window import key
from pyglet.window import mouse
from tkinter.filedialog import asksaveasfilename

import JsonCell
import game_objects
import gamefield

__author__ = 'Dmitry'

# import main

gamefield_batch = pyglet.graphics.Batch()


class LevelEditor:
    selected_figure = None
    editor_figures = []

    def __init__(self, batch):
        self.set_editor_objects(batch)
        load_level(4, game_field, gamefield_batch)

    def set_selected(self, figure):
        self.selected_figure = figure

    def set_editor_objects(self, batch):
        tree = game_objects.Tree(batch, [1, 10])
        self.editor_figures.append(tree)
        brick = game_objects.Brick(batch, [1, 11])
        self.editor_figures.append(brick)
        box = game_objects.Box(batch, [2, 10])
        self.editor_figures.append(box)
        box_target = game_objects.BoxTarget(batch, [2, 11])
        self.editor_figures.append(box_target)
        player = game_objects.Player(batch, [3, 10])
        self.editor_figures.append(player)


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


def set_selected_figure_on_gamefield(figure, row, column):
    figure.row = row
    figure.column = column
    current_cell = row, column
    obj_set = set()
    if game_field.cells.get((row, column)) is not None:
        obj_set = game_field.cells[(row, column)]

    obj_set.add(game_objects.build_game_object(figure.obj_id, current_cell, gamefield_batch))
    game_field.cells.setdefault((row, column), obj_set)

    print(game_field.cells.get((row, column)))

    label.text = "figure #" + str(figure)
    print("figure #" + str(figure))


def load_level(level_number, editor, batch):
    with open('levels/' + str(level_number) + '.json') as f:
        editor.level = int(level_number)
        d = json.load(f)
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


def save_level():
    filename = asksaveasfilename(title = 'Save file', filetypes = [('level files', '*.lvl')], defaultextension = '.lvl')
    if not filename: return

    with open(filename, 'w', encoding='utf-8') as f:
        json_cells = []
        for cell in game_field.cells:
            json_cell = JsonCell.JsonCell(cell[0], cell[1])
            json_cell.objects = game_field.cells[(json_cell.r, json_cell.c)]
            json_cells.append(json_cell)

        splitted_name = f.name.split('/')
        name_with_extension = splitted_name[len(splitted_name)-1]
        name = name_with_extension.split('.')[0]
        json_level = {}
        json_level.setdefault("level", name)
        json_level.setdefault("cells", json_cells)

        json.dump(json_level, f, cls=JsonCell.JsonCellEncoder, ensure_ascii=False, indent=4)
        return 'saved'


def update(dt):
    pass


grid_batch = pyglet.graphics.Batch()
editor_batch = pyglet.graphics.Batch()

game_field = gamefield.GameField()
level_editor = LevelEditor(editor_batch)

window = pyglet.window.Window(width=800, height=640, caption="Level Editor")
window.set_mouse_visible()

label = pyglet.text.Label('', font_name='Times New Roman', font_size=16, x=410, y=10,
                          anchor_x='right', anchor_y='baseline')

clock.schedule(update)
grid_array = []
gamefield.draw_grid(grid_batch, grid_array)


@window.event
def on_draw():
    window.clear()
    editor_batch.draw()
    grid_batch.draw()
    gamefield_batch.draw()
    label.draw()


def clear_field_under_cursor(x, y):
    row,column = gamefield.get_cell_by_coords(x, y)
    current_objects = game_field.cells.get((row, column))
    if current_objects is not None:
        label.text = 'clear field under cursor'
        game_field.cells.pop((row, column))


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        if gamefield.is_mouse_on_gamefield(x, y):
            # ставим выделенную фигуру
            row, column = gamefield.get_cell_by_coords(x, y)
            try:
                set_selected_figure_on_gamefield(level_editor.selected_figure, row, column)
            except AttributeError:
                print("Объект не выделен")
        else:
            check_figure_under_mouse(x, y, level_editor.editor_figures)
            print(level_editor.selected_figure)
    elif button == mouse.RIGHT:
        if level_editor.selected_figure is None:
            clear_field_under_cursor(x, y)
        else:
            level_editor.selected_figure = None
            label.text = 'right: {0}, is mouse on gamefield: {1}' \
                .format(gamefield.get_cell_by_coords(x, y), gamefield.is_mouse_on_gamefield(x, y))
            window.set_mouse_cursor(window.CURSOR_DEFAULT)


def load_level_dialog():
    # window = pyglet.window.Window(width=300, height=100, caption="Load level dialog")
    # filename = fd.askopenfilename()
    label.text = 'loading level'



@window.event
def on_key_press(symbol, modifiers):
    print("symbol:" + str(symbol))
    print("modifiers", str(modifiers))
    if symbol == key.S:
        if modifiers & key.MOD_CTRL:
            save_level()
            label.text = 'level saved'
    if symbol == key.L:
        if modifiers & key.MOD_CTRL:
            load_level_dialog()



@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & mouse.LEFT:
        row, column = gamefield.get_cell_by_coords(x, y)

        set_selected_figure_on_gamefield(level_editor.selected_figure, row, column)
        label.text = 'x: {0}, y:{1}, dx:{2}, dy:{3}'.format(x, y, dx, dy)
        # print('x: {0}, y:{1}, dx:{2}, dy:{dy}'.format(x, y, dx, dy))


pyglet.app.run()
