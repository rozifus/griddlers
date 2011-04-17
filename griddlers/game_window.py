from pyglet import window
from pyglet import clock


class GameWindow(window.Window):
    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)
        self.has_exit = False
        self.inputManager = None
        self.drawManager = None
        self.playerManager = None
        self.gameManager = GameManager(self)

    def main_loop(self):
        clock.set_fps_limit(30)
        while not self.has_exit:
            self.dispatch_events()
            #self.update()
            self.clear()
            #self.draw()

            clock.tick()
            #Gets fps and draw it
            #self.fps_label.text = "%d" % clock.get_fps()
            #self.fps_label.draw()

            self.flip()

class GameManager(object):
    def __init__(self, parent):
        self.parent = parent
        self.level = None

    def loadLevel(self, level):
        self.level = Level(this)


class Level(object):
    def __init__(self, parent):
        self.parent = parent
        self.grid = None

    def initialize(self):
        self.grid = Grid()
        










    
