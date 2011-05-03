from __future__ import print_function

from pyglet import resource
from pyglet import event
from pyglet.window import mouse, key

from grid import trigrid
import data
import camera

class Level(event.EventDispatcher):
    def __init__(self, p_game):
        self.p_game = p_game
        winx, winy = self.p_game.p_window.get_size()
        self.camera = camera.Camera(0,0, winx, winy, 50)
        self.grid = trigrid.TriGrid(self, 40, 60)
        self.grid.initializeBlank(50, 50)

    def activate(self):
        self.grid.activate()
        self.p_game.p_window.push_handlers(
                self.on_draw, self.on_mouse_drag, 
                self.on_mouse_press, self.on_key_press)

    def deactivate(self):
        self.grid.deactivate()
        self.p_game.p_window.pop_handlers()

    def on_draw(self):
        self.p_game.p_window.clear()
        self.dispatch_event('level_draw', self.camera)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modi):
        if buttons & mouse.RIGHT:
            self.camera.x += dx
            self.camera.y += dy

    def on_mouse_press(self, x, y, buttons, modi):
        if buttons & mouse.LEFT:
            self.grid.selected = self.grid.getVisualNodeAt(self.camera, x, y)

    def on_key_press(self, symbol, modi):
        if symbol == key.U:
            if self.grid.selected:
                self.grid.selected.raiseZ()
        elif symbol == key.I:
            if self.grid.selected:
                self.grid.selected.lowerZ()
        elif symbol == key.S:
            wfile = data.userFile('maps', "mapone.map", 'wt')
            wfile.write(self.grid.getAllJson())
            wfile.close()
        elif symbol == key.L:
            rfile = data.userFile('maps', "mapone.map", 'r')
            self.grid.setAllJson(rfile.read())
            rfile.close()
        elif symbol == key.ESCAPE:
            self.p_game.quitEditor()
            return True

Level.register_event_type('level_draw')

 
