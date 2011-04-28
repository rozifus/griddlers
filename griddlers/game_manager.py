import level
import screen

class GameManager(object):
    def __init__(self, p_window):
        self.p_window = p_window
        self.level = None
        self.screen = None

        #self.loadLevel(None)
        self.loadScreen()

    def loadLevel(self, levelFile):
        self.level = level.Level(self)

    def loadScreen(self):
        self.screen = screen.Screen(self)
   
