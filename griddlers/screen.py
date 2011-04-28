from __future__ import print_function

from pyglet import resource
from pyglet import event
from pyglet.window import mouse, key
from pyglet import text
from pyglet import gl

import data
import camera

class Style(object):
    def __init__(self):
        pass
        

class Button(object):

    @property
    def right(self):
        return self.x + self.w/2
    
    @property
    def left(self):
        return self.x - self.w/2

    @property
    def top(self):
        return self.y + self.h/2
    
    @property
    def bottom(self):
        return self.y - self.h/2



    def __init__(self, x, y, subx, suby, w, h, title="", function=None):
        self.x, self.y = x, y
        self.subx, self.suby = subx, suby
        self.w, self.h = w, h
        self.label = text.Label(title, 
                                font_name="Arial", font_size=36,
                                x=self.subx, anchor_x = 'center',
                                y=self.suby, anchor_y = 'center'
                                )
        self.function = function

    def drawGL(self, camera):
        if camera.inCamera(self.x, self.y, self.w, self.h):
            gl.glVertex2d(self.left-camera.x, 
                          self.bottom-camera.y)
            gl.glVertex2d(self.right-camera.x, 
                          self.bottom-camera.y)
            gl.glVertex2d(self.right-camera.x, 
                          self.top-camera.y)
            gl.glVertex2d(self.left-camera.x, 
                          self.top-camera.y)

    def draw(self, camera):
        if camera.inCamera(self.x, self.y, self.w, self.h):
            self.label.draw()
            

class SubScreen(object):
    def __init__(self, p_screen, x, y):
        self.p_screen = p_screen
        self.x, self.y = x, y
        self.elements = []

    def activate(self):
        self.p_screen.push_handlers(self.screen_draw)

    def deactivate(self):
        self.p_screen.pop_handlers()

    def screen_draw(self, camera):
        gl.glLoadIdentity()
        gl.glBegin(gl.GL_QUADS)
        for elem in self.elements:
            gl.glColor3f(1.0,0.0,0.0)
            elem.drawGL(camera)
        gl.glEnd()
        for elem in self.elements:
            elem.draw(camera)
        


class Screen(event.EventDispatcher):
    def __init__(self, p_game):
        self.p_game = p_game
        self.w, self.h = self.p_game.p_window.get_size()
        self.camera = camera.Camera(0, 0, self.w, self.h, 10)
        self.subscreens = []

        subby = SubScreen(self, 0, 0)
        but1 = Button(200, 200, 200, 200, 200, 100, "button1")
        subby.elements.append(but1)
        subby.activate()
        self.subscreens.append(subby)

        self.activate()

    def activate(self):
        self.p_game.p_window.drawManager.push_handlers(self.window_draw)

    def window_draw(self):
        self.dispatch_event('screen_draw', self.camera)

Screen.register_event_type('screen_draw')


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

 
