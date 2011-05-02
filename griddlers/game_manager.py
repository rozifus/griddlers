import level
import menu 

class GameManager(object):
    def __init__(self, p_window):
        self.p_window = p_window
        self.level = None
        self.menu = None

        #self.loadLevel(None)
        self.loadMenu()

    def loadLevel(self, levelFile):
        self.level = level.Level(self)

    def loadMenu(self):
        self.menu = menu.Menu(self)
   
