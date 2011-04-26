import level

class GameManager(object):
    def __init__(self, p_window):
        self.p_window = p_window
        self.level = None

        self.loadLevel(None)

    def loadLevel(self, levelFile):
        self.level = level.Level(self)
   
