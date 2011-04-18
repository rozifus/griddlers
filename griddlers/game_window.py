from __future__ import print_function

from pyglet import window
from pyglet import clock
from pyglet import event
from pyglet.window import mouse

import trigrid


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
        self.grid = trigrid.TriGrid(self, 25, 25, 20, 20)

        self.activate()

    def activate(self):
        self.grid.activate()
        self.parent.parent.drawManager.push_handlers(
                        window_draw=self.draw)
        self.parent.parent.push_handlers(on_mouse_drag=self.mouse_drag)

    def draw(self):
        self.dispatch_event('level_draw', self.camera)

    def mouse_drag(self, x, y, dx, dy, buttons, modi):
        if buttons & mouse.RIGHT:
            self.camera.x += dx
            self.camera.y += dy

Level.register_event_type('level_draw')


class Camera(object):
    def __init__(self, x, y, w, h):
        self.x, self.y = x,y
        self.w, self.h = w,h
    
