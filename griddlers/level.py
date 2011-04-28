from __future__ import print_function

from pyglet import resource
from pyglet import event
from pyglet.window import mouse, key

from grid import trigrid
import data

class Level(event.EventDispatcher):
    def __init__(self, p_game):
        self.p_game = p_game
        winx, winy = self.p_game.p_window.get_size()
        self.camera = Camera(0,0, winx, winy, 50)
        self.grid = trigrid.TriGrid(self, 40, 60)
        self.grid.initializeBlank(50, 50)

        self.activate()

    def activate(self):
        self.grid.activate()
        self.p_game.p_window.drawManager.push_handlers(
                        window_draw=self.draw)
        self.p_game.p_window.push_handlers(on_mouse_drag=self.mouse_drag)
        self.p_game.p_window.push_handlers(on_mouse_press=self.mouse_press)
        self.p_game.p_window.push_handlers(on_key_press=self.key_press)

    def draw(self):
        self.dispatch_event('level_draw', self.camera)

    def mouse_drag(self, x, y, dx, dy, buttons, modi):
        if buttons & mouse.RIGHT:
            self.camera.x += dx
            self.camera.y += dy

    def mouse_press(self, x, y, buttons, modi):
        if buttons & mouse.LEFT:
            self.grid.selected = self.grid.getVisualNodeAt(self.camera, x, y)

    def key_press(self, symbol, modi):
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

Level.register_event_type('level_draw')


class Camera(object):
    def __init__(self, x, y, w, h, margin):
        self.x, self.y = x,y
        self.w, self.h = w,h
        self.m = margin

    def inCamera(self, x, y, w, h):
        if x+w > self.x-self.m and x < self.x+self.w+self.m \
        and y+h > self.y-self.m and y < self.y+self.h+self.m:
            return True
        return False

 
