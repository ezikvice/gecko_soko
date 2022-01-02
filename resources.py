import pyglet
import pyglet.resource as res

pyglet.options['audio'] = ('directsound', 'silent')
res.path = ["res", "res/sound"]
res.reindex()

brick = res.image("bricks3.png")
# brick = res.image("brick-wall.png")
tree = res.image("beech.png")
pinetree = res.image("pine-tree2.png")
box = res.image("wooden-crate3.png")
player = res.image("gecko4.png")
player_down = res.image("gecko4.png", rotate=180)
player_left = res.image("gecko4.png", rotate=270)
player_right = res.image("gecko4.png", rotate=90)
target = res.image("boxtarget_2.png")

backmusic = res.media("backmusic.mp3", streaming=False)
