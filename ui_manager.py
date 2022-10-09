import pyglet
from game_metric import *


class UiManager:
    window = pyglet.window.Window(width=(CELL_SIZE * 10), height=(CELL_SIZE * 10),
                                  caption="Gecko Soko")

    label = pyglet.text.Label('', font_name='Arial', font_size=24,
                              x=310, y=10, anchor_x='right', anchor_y='baseline')

    label_victory = pyglet.text.Label('', font_name='Times New Roman', font_size=64, color=(255, 0, 0, 255),
                                      x=550, y=310, anchor_x='right', anchor_y='baseline')

    batch = pyglet.graphics.Batch()

    fps_display = pyglet.window.FPSDisplay(window)

    @classmethod
    def draw_all(cls):
        cls.window.clear()
        cls.batch.draw()
        cls.label.draw()
        cls.label_victory.draw()
        cls.fps_display.draw()

    @classmethod
    def show_victory(cls):
        cls.label_victory.text = 'VICTORY!'

    @classmethod
    def show_level(cls, level_number):
        cls.label.text = 'Level ' + str(level_number)



