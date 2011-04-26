from __future__ import print_function


class TriNode(object):
    color = {}
    color['w'] = (0.1, 0.1, 0.9)
    color['g'] = (0.1, 0.9, 0.3)
    color['m'] = (0.9, 0.7, 0.2)

    def __init__(self, grid, x, y):
        self.grid = grid
        self.content = None
        self.mat = None
        self.z = None
        self.x, self.y = x, y
        self.vx, self.vy = x, y
        self.e1 = self.e2 = self.e3 = None
        self.e4 = self.e5 = self.e6 = None 

    def setZ(self, char):
        self.z = char 
        if char == '0': 
            self.vy = self.y
            self.mat = 'w'
        elif char == '1': 
            self.vy = self.y + self.grid.ys / 5 
            self.mat = 'g'
        elif char == '2':
            self.vy = self.y + (2 * self.grid.ys) / 5 
            self.mat = 'g'
        elif char == '3':
            self.vy = self.y + (3 * self.grid.ys) / 5
            self.mat = 'm'
        elif char == '4':
            self.vy = self.y + (4 * self.grid.ys) / 5
            self.mat = 'm'

    def raiseZ(self):
        if self.z == '0':
            self.setZ('1')
        elif self.z == '1':
            self.setZ('2')
        elif self.z == '2':
            self.setZ('3')
        elif self.z == '3':
            self.setZ('4')

    def lowerZ(self):
        if self.z == '4':
            self.setZ('3')
        elif self.z == '3':
            self.setZ('2')
        elif self.z == '2':
            self.setZ('1')
        elif self.z == '1':
            self.setZ('0')

    def edgeList(self):
        if self.e1: yield self.e1
        if self.e2: yield self.e2
        if self.e3: yield self.e3
        if self.e4: yield self.e4
        if self.e5: yield self.e5
        if self.e6: yield self.e6

    def leftEdgeList(self):
        if self.e1: yield self.e1
        if self.e2: yield self.e2
        if self.e3: yield self.e3

    def rightEdgeList(self):
        if self.e4: yield self.e4
        if self.e5: yield self.e5
        if self.e6: yield self.e6

    def nodeList(self):
        if self.e1: yield self.e1.start
        if self.e2: yield self.e2.start
        if self.e3: yield self.e3.start
        if self.e4: yield self.e4.end
        if self.e5: yield self.e5.end
        if self.e6: yield self.e6.end

