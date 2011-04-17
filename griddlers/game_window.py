from __future__ import print_function

from pyglet import window
from pyglet import clock
from pyglet import event


class GameWindow(window.Window):
    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)
        self.has_exit = False
        self.inputManager = None
        self.drawManager = WindowDrawManager(self)
        self.playerManager = None
        self.gameManager = GameManager(self)

    def on_draw(self):
        self.drawManager.draw()





class WindowDrawManager(event.EventDispatcher):
    def __init__(self, parent):
        super(WindowDrawManager, self).__init__()
        self.parent = parent

    def draw(self):
        print('window_draw')
        self.dispatch_event('window_draw')

WindowDrawManager.register_event_type('window_draw')

        


class GameManager(object):
    def __init__(self, parent):
        self.parent = parent
        self.level = None

        self.loadLevel(None)

    def loadLevel(self, level):
        self.level = Level(self)


class Level(object):
    def __init__(self, parent):
        self.parent = parent
        self.grid = None
        self.drawDisp = LevelDrawDispatcher()

        self.initialize()

    def initialize(self):
        self.parent.parent.drawManager.push_handlers(window_draw=self.drawDisp.draw)
        self.grid = None 
        
class LevelDrawDispatcher(event.EventDispatcher):
    def draw(self):
        print("level_draw")
        self.dispatch_event('level_draw')

LevelDrawDispatcher.register_event_type('level_draw')





    
