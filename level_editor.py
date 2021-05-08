import pyglet
from pyglet import clock
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
    img.scale = 1.1
    # img.opacity = 128
    current_cursor = pyglet.window.ImageMouseCursor(img.image, img.width / 2, img.height / 2)
    window.set_mouse_cursor(current_cursor)


def check_figure_under_mouse(x, y, figures_array):
    for figure in figures_array:
        if figure.x <= x <= figure.x + figure.width and figure.y <= y <= figure.y + figure.height:
            label.text = "figure #" + str(figure.obj_id)
            change_cursor(figure)
            level_editor.set_selected(figure)
            print("selected: " + repr(level_editor.selected_figure))


def set_selected_figure_on_gamefield(figure, row, column):
    if figure.obj_id == 2:
        current_cell = row, column

        gamefield.GameField.trees.append(game_objects.Tree(gamefield_batch, current_cell))
        print(gamefield.GameField.trees)
    label.text = "figure #" + str(figure)
    print("figure #" + str(figure))


def update(dt):
    pass


pyglet.resource.path = ["res"]
pyglet.resource.reindex()

grid_batch = pyglet.graphics.Batch()
editor_batch = pyglet.graphics.Batch()

level_objects = []
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


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        if gamefield.is_mouse_on_gamefield(x, y):
            # ставим выделенную фигуру
            row, column = gamefield.get_cell_by_coords(x, y)
            set_selected_figure_on_gamefield(level_editor.selected_figure, row, column)
        else:
            check_figure_under_mouse(x, y, level_editor.editor_figures)
            print(level_editor.selected_figure)
    elif button == mouse.RIGHT:
        label.text = 'right: {0}, is mouse on gamefield: {1}' \
            .format(gamefield.get_cell_by_coords(x, y), gamefield.is_mouse_on_gamefield(x, y))
        window.set_mouse_cursor(window.CURSOR_DEFAULT)


pyglet.app.run()
