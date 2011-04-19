from __future__ import print_function

from pyglet import window
from pyglet import clock
from pyglet import event
from pyglet.window import mouse

import trigrid

heightMap = """
         0000000000000000
         0000001110000000
         0000000121000000
         0010000121001000
         0011111121111100
         0112323321211111
         0122344441222111
         0112344442232111"""

materialMap = """
         wwwwwwwwwwwwwwww
         wwwwwwwggwwwwwww
         wwwwwwwggggwwwww
         wwgwwwwggggwgwww
         wwggggggggggggww
         wggggmgmgggggggg
         wggmmmmmmggggggg
         wgggmmmmmggmgggg"""



class GameWindow(window.Window):
    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)
        self.has_exit = False
        self.inputManager = InputManager(self) 
        self.drawManager = WindowDrawManager(self)
        self.playerManager = None
        self.gameManager = GameManager(self)


class InputManager(object):
    def __init__(self, parent):
        self.parent = parent


class WindowDrawManager(event.EventDispatcher):
    def __init__(self, parent):
        super(WindowDrawManager, self).__init__()
        self.parent = parent

        self.activate()

    def activate(self):
        self.parent.push_handlers(on_draw=self.draw)

    def draw(self):
        self.parent.clear()
        self.dispatch_event('window_draw')
        self.parent.flip()

WindowDrawManager.register_event_type('window_draw')



class GameManager(object):
    def __init__(self, parent):
        self.parent = parent
        self.level = None

        self.loadLevel(None)

    def loadLevel(self, level):
        self.level = Level(self)



class Level(event.EventDispatcher):
    def __init__(self, parent):
        self.parent = parent
        self.camera = Camera(0,0, *self.parent.parent.get_size())
        self.grid = trigrid.TriGrid(self, 16, 8, 20, 30)
        self.grid.contour(heightMap)
        self.grid.materialize(materialMap)

        self.activate()

    def activate(self):
        self.grid.activate()
        self.parent.parent.drawManager.push_handlers(
                        window_draw=self.draw)
        self.parent.parent.push_handlers(on_mouse_drag=self.mouse_drag)
        self.parent.parent.push_handlers(on_mouse_press=self.mouse_press)

    def draw(self):
        self.dispatch_event('level_draw', self.camera)

    def mouse_drag(self, x, y, dx, dy, buttons, modi):
        if buttons & mouse.RIGHT:
            self.camera.x += dx
            self.camera.y += dy

    def mouse_press(self, x, y, buttons, modi):
        if buttons & mouse.LEFT:
            self.grid.selected = self.grid.getVisualNodeAt(self.camera, x, y)

Level.register_event_type('level_draw')


class Camera(object):
    def __init__(self, x, y, w, h):
        self.x, self.y = x,y
        self.w, self.h = w,h
    
