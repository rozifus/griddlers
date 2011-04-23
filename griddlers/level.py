from __future__ import print_function

from pyglet import event
from pyglet.window import mouse, key

import trigrid
import mapgen

class Level(event.EventDispatcher):
    def __init__(self, p_game):
        self.p_game = p_game
        self.camera = Camera(0,0, *self.p_game.p_window.get_size())
        self.grid = trigrid.TriGrid(self, 50, 50, 30, 45)

        try:
            hmap = open('hmap.txt', 'r')
            mmap = open('mmap.txt', 'r')
            self.grid.contour(hmap)
            self.grid.materialize(mmap)
            hmap.close()
            mmap.close()
        except:
            mg = mapgen.MapGen(self.grid.x, self.grid.y)
            cont, mat = mg.createDefaultMap()
            self.grid.contour(cont)
            self.grid.materialize(mat)

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

Level.register_event_type('level_draw')


class Camera(object):
    def __init__(self, x, y, w, h):
        self.x, self.y = x,y
        self.w, self.h = w,h

    def inCamera(self, x, y, w, h):
        if x+w > self.x and x < self.x+self.w \
        and y+h > self.y and y < self.y+self.h:
            return True
        return False

 
