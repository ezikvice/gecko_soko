import pyglet
from pyglet import clock
from pyglet.window import key
from pyglet.window import mouse

import game_objects
import gamefield

__author__ = 'Dmitry'

gamefield_batch = pyglet.graphics.Batch()


class LevelEditor:
    selected_figure = None
    editor_figures = []

    def __init__(self, batch):
        tree = game_objects.Tree(batch, [1, 10])
        self.editor_figures.append(tree)
        brick = game_objects.Brick(batch, [1, 11])
        self.editor_figures.append(brick)
        box = game_objects.Box(batch, [2, 10])
        self.editor_figures.append(box)
        box_target = game_objects.BoxTarget(batch, [2, 11])
        self.editor_figures.append(box_target)

    def set_selected(self, figure):
        self.selected_figure = figure


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
    if gamefield.GameField.cells.get((row, column)) is not None:
        obj_set = gamefield.GameField.cells[(row, column)]

    if figure.obj_id == 2:
        gamefield.GameField.trees.append(game_objects.Tree(gamefield_batch, current_cell))
        # print(*gamefield.GameField.trees, sep='; ')
    elif figure.obj_id == 3:
        gamefield.GameField.bricks.append(game_objects.Brick(gamefield_batch, current_cell))
        # print(*gamefield.GameField.bricks, sep='; ')
    elif figure.obj_id == 4:
        gamefield.GameField.boxes.append(game_objects.Box(gamefield_batch, current_cell))
        # print(*gamefield.GameField.boxes, sep='; ')
    elif figure.obj_id == 10:
        gamefield.GameField.box_targets.append(game_objects.BoxTarget(gamefield_batch, current_cell))
        # print(*gamefield.GameField.box_targets, sep='; ')

    obj_set.add(game_objects.build_game_object(figure.obj_id, current_cell))
    gamefield.GameField.cells.setdefault((row, column), obj_set)

    print(gamefield.GameField.cells.get((row, column)))

    label.text = "figure #" + str(figure)
    print("figure #" + str(figure))


def save_level():
    with open('levels/data.json', 'w', encoding='utf-8') as f:
        for cell in gamefield.GameField.cells:
            # cell_string = "\"r\": " + cell
            print(str(cell[0]) + ", " + str(cell[1]))
        # json_str = json.dumps(gamefield.GameField.cells, ensure_ascii=False, indent=4)
        # print(json_str)


def update(dt):
    pass


grid_batch = pyglet.graphics.Batch()
editor_batch = pyglet.graphics.Batch()

level_objects = []
gamefield.GameField()
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
        label.text = 'right: {0}, is mouse on gamefield: {1}' \
            .format(gamefield.get_cell_by_coords(x, y), gamefield.is_mouse_on_gamefield(x, y))
        window.set_mouse_cursor(window.CURSOR_DEFAULT)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.S:
        print("symbol:" + str(symbol))
        print("modifiers", str(modifiers))
        save_level()


pyglet.app.run()
