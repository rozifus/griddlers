from __future__ import print_function

from pyglet import resource
from pyglet import event
from pyglet.window import mouse, key
from pyglet import text
from pyglet import gl

import data
import camera


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
    @property
    def lb(self):
        return (self.left, self.bottom)
    @property
    def rb(self):
        return (self.right, self.bottom)
    @property
    def lt(self):
        return (self.left, self.top)
    @property
    def rt(self):
        return (self.right, self.top)
    
    def __init__(self, x, y, w, h, title="", function=None):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.label = text.Label(title, 
                                font_name="Arial", font_size=36,
                                x=self.x, anchor_x = 'center',
                                y=self.y, anchor_y = 'center'
                                )
        self.function = function
        self.isHover, self.isDown = False, False

    def drawGL(self):
        gl.glVertex2d(*self.rt)
        gl.glVertex2d(*self.rb)
        gl.glVertex2d(*self.lb)
        gl.glVertex2d(*self.lt)

    def draw(self):
        self.label.draw()
            
    def inButton(self, x, y, w=0, h=0):
        if x+w > self.left and x < self.right \
        and y+h > self.bottom and y < self.top:
            return True
        return False


class SubMenu(object):
    def __init__(self, p_menu):
        self.p_menu = p_menu
        self.elements = []
        self.red = (1.0,0.0,0.0)
        self.green = (0.0,1.0,0.0)

    def activate(self):
        self.p_menu.push_handlers(
                self.menu_draw, self.menu_mouse_press, self.menu_mouse_motion)

    def deactivate(self):
        self.p_menu.pop_handlers()

    def menu_draw(self):
        gl.glLoadIdentity()
        gl.glBegin(gl.GL_QUADS)
        for elem in self.elements:
            if elem.isHover:
                gl.glColor3f(*self.red)
            else:
                gl.glColor3f(*self.green)
            elem.drawGL()
        gl.glEnd()
        for elem in self.elements:
            elem.draw()
        
    def menu_mouse_press(self, x, y, buttons, modi):
        if buttons & mouse.LEFT:
            for elem in self.elements:
                if elem.inButton(x,y):
                    elem.function()


    def menu_mouse_motion(self, x, y, dx, dy):
        for elem in self.elements:
            if elem.inButton(x,y):
                elem.isHover = True
            else: elem.isHover = False        

class Menu(event.EventDispatcher):
    def __init__(self, p_game):
        self.p_game = p_game
        self.w, self.h = self.p_game.p_window.get_size()
        self.submenus = []

        self.loadData()

    def loadData(self):
        subby = SubMenu(self)
        but1loc = [x/2 for x in self.p_game.p_window.get_size()]
        but1 = Button(but1loc[0], but1loc[1], 260, 80, "Map Editor", 
                      self.p_game.startEditor)
        subby.elements.append(but1)
        self.submenus.append(subby)
        subby.activate()

    def activate(self):
        self.p_game.p_window.push_handlers(
                self.on_draw, self.on_mouse_press, self.on_mouse_motion)

    def deactivate(self):
        self.p_game.p_window.pop_handlers()

    def on_draw(self):
        self.p_game.p_window.clear()
        self.dispatch_event('menu_draw')

    def on_mouse_press(self, x, y, buttons, modi):
        self.dispatch_event('menu_mouse_press', x, y, buttons, modi)

    def on_mouse_motion(self, x, y, dx, dy):
        self.dispatch_event('menu_mouse_motion', x, y, dx, dy)

Menu.register_event_type('menu_draw')
Menu.register_event_type('menu_mouse_press')
Menu.register_event_type('menu_mouse_motion')


