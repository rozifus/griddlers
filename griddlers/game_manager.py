import level
import menu 

class GameManager(object):
    def __init__(self, p_window):
        self.p_window = p_window
        self.level = None
        self.mainMenu = None

        #self.loadLevel(None)
        self.initExtra()

    def initExtra(self):
        self.mainMenu = menu.Menu(self)
        self.mainMenu.activate()

    def startEditor(self):
        self.mainMenu.deactivate()
        self.mainMenu = None
        self.level = level.Level(self)
        print(dir(self.level))
        self.level.activate()

    def quitEditor(self):
        self.level.deactivate()
        self.level = None
        self.mainMenu = menu.Menu(self)
        self.mainMenu.activate()

        
        
        
   
