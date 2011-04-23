from __future__ import print_function

from pyglet import window
from pyglet import clock
from pyglet import event

import level


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
    def __init__(self, p_window):
        self.p_window = p_window
        self.level = None

        self.loadLevel(None)

    def loadLevel(self, levelFile):
        self.level = level.Level(self)
   
