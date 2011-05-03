from __future__ import print_function

from pyglet import window
from pyglet import clock
from pyglet import event

import game_manager

class GameWindow(window.Window):
    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)
        self.has_exit = False
        self.playerManager = None
        self.gameManager = game_manager.GameManager(self)


wm = """
class WindowDrawManager(event.EventDispatcher):
    def __init__(self, parent):
        super(WindowDrawManager, self).__init__()
        self.parent = parent

        self.activate()

    def activate(self):
        self.parent.push_handlers(self.on_draw)

    def deactivate(self):
        self.parent.pop_handlers()

    def on_draw(self):
        self.parent.clear()
        self.dispatch_event('window_draw')
        self.parent.flip()

WindowDrawManager.register_event_type('window_draw')
"""

   
