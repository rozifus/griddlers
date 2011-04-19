from __future__ import print_function
from pyglet import gl
import math

color = {}
color['w'] = (0.1, 0.1, 0.9)
color['g'] = (0.1, 0.9, 0.3)
color['m'] = (0.9, 0.7, 0.2)

class Edge(object):
    def __init__(self, start, end):
        self.filling = None
        self.start = start
        self.end = end

class TriNode(object):
    def __init__(self, x, y):
        self.content = None
        self.mat = None
        self.x, self.y = x, y
        self.vx, self.vy = x, y
        self.e1 = self.e2 = self.e3 = None
        self.e4 = self.e5 = self.e6 = None 

    def edgeList(self):
        if self.e1: yield self.e1
        if self.e2: yield self.e2
        if self.e3: yield self.e3
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

class TriGrid(object):
    def __init__(self, parent, x, y, sizex, sizey):
        self.parent = parent
        self.x, self.y = x, y
        self.xs, self.ys = sizex, sizey
        self.nodeMap = {}
        self.edges = [] 
        self.selected = None

        for x,y in self.generateBaseNodePositions():
            self.nodeMap[(x,y)] = TriNode(x,y)

        self.nodes = self.nodeMap.values()

        for node in self.nodes:
            conn = self.getNodeAt(node.x - self.xs, node.y + self.ys)
            if conn:
                edge = Edge(conn, node)
                node.e1 = edge
                conn.e6 = edge
                self.edges.append(edge)
            conn = self.getNodeAt(node.x - self.xs * 2, node.y)
            if conn:
                edge = Edge(conn, node)
                node.e2 = edge 
                conn.e5 = edge
                self.edges.append(edge)
            conn = self.getNodeAt(node.x - self.xs, node.y - self.ys)
            if conn:
                edge = Edge(conn, node)
                node.e3 = edge 
                conn.e4 = edge
                self.edges.append(edge)


    def generateBaseNodePositions(self):
        shift = 1 
        for y in range(0, self.y*self.ys, self.ys):
            if shift == 1: 
                shift = 0 
            else: shift = 1 
            for x in range(0, self.x*self.xs*2, self.xs*2):
                if shift == 1: x += self.xs 
                yield x,y 

    def contour(self, contourMap):
        valid = ['0', '1', '2', '3', '4', 'w']
        def getNextContour(contourMap):
            linearMap = ""
            for char in contourMap:
                if char in valid:
                    linearMap += char
            for li in range(self.y)[::-1]:
                line = linearMap[li*self.x: (li+1)*self.x]
                for char in line:
                    yield char

        def applyContour(node, char):    
            if char == '0': pass
            elif char == '1': 
                node.vy = node.y + self.ys / 5 
            elif char == '2':
                node.vy = node.y + (2 * self.ys) / 5 
            elif char == '3':
                node.vy = node.y + (3 * self.ys) / 5
            elif char == '4':
                node.vy = node.y + (4 * self.ys) / 5

        contourGen = getNextContour(contourMap)
        for x,y in self.generateBaseNodePositions():
            applyContour(self.getNodeAt(x,y), contourGen.next())

    def materialize(self, materialMap):
        valid = ['w', 'g', 'm']
        def getNextMaterial(materialMap):
            linearMap = ""
            for char in materialMap:
                if char in valid:
                    linearMap += char
            for li in range(self.y)[::-1]:
                line = linearMap[li*self.x: (li+1)*self.x]
                for char in line:
                    yield char

        materialGen = getNextMaterial(materialMap)
        for x,y in self.generateBaseNodePositions():
            self.getNodeAt(x,y).mat = materialGen.next()
        
    def getNodeAt(self, x, y):
        return self.nodeMap.get((x,y), None)

    def activate(self):
        self.parent.push_handlers(level_draw=self.draw)
 
    def getNodeAt(self, x, y):
        return self.nodeMap.get((x,y), None)

    def getVisualNodeAt(self, camera, x, y):
        def generateNodeHex(node0):
            node1 = node2 = node3 = None
            node4 = node5 = node6 = None
            if node0.e5:
                node1 = node0.e5.end
            if node0.e3:
                node2 = node0.e3.start
                if node2.e6:
                    node5 = node2.e6.end
            if node0.e6:
                node3 = node0.e6.end
                if node3.e6:
                    node6 = node3.e6.end
                if node3.e5:
                    node4 = node3.e5.end
                if node3.e6:
                    node5 = node3.e3.start
            if node1: yield node1
            if node2: yield node2
            if node3: yield node3
            if node4: yield node4
            if node5: yield node5
            if node6: yield node6
    
        def getVisualDistance(node, x, y):
            return math.sqrt((node.vx-x)**2 + (node.vy-y)**2)

        x += camera.x
        y += camera.y
        divx = x / self.xs
        divy = y / self.ys
        modx = x % self.xs 
        mody = y % self.ys 
        if divx % 2 == 0:
            divx -= 1 
        if divy % 2 == 1:
            divx -= 1
        left = divx * self.xs 
        right = left + self.xs
        bottom = divy * self.ys 
        top = bottom + self.ys

        print(left, top)
        node0 = self.getNodeAt(left,top)
        if node0:
            minDist = getVisualDistance(node0, x, y)
            minNode = node0
            for node in generateNodeHex(node0):
                nDist = getVisualDistance(node, x, y)
                print(nDist)
                if nDist < minDist:
                    minDist = nDist
                    minNode = node
                print(minNode.vx, minNode.vy)

            return minNode 
        return None


    def draw(self, camera):
        gl.glLoadIdentity()
        gl.glBegin(gl.GL_TRIANGLES)
        gl.glColor3f(1.0,1.0,1.0)
        for node in self.nodes:
            if node.e4:
                node2 = node.e4.end
                if node2.e6:
                    node3 = node2.e6.end
                    gl.glColor3f(*color[node.mat])
                    gl.glVertex2f(node.vx-camera.x, node.vy-camera.y)
                    gl.glColor3f(*color[node2.mat])
                    gl.glVertex2f(node2.vx-camera.x, node2.vy-camera.y)
                    gl.glColor3f(*color[node3.mat])
                    gl.glVertex2f(node3.vx-camera.x, node3.vy-camera.y)
            if node.e5:
                node2 = node.e5.end
                if node2.e3:
                    node3 = node2.e3.start
                    gl.glColor3f(*color[node.mat])
                    gl.glVertex2f(node.vx-camera.x, node.vy-camera.y)
                    gl.glColor3f(*color[node2.mat])
                    gl.glVertex2f(node2.vx-camera.x, node2.vy-camera.y)
                    gl.glColor3f(*color[node3.mat])
                    gl.glVertex2f(node3.vx-camera.x, node3.vy-camera.y)
        gl.glEnd()
                
        gl.glBegin(gl.GL_LINES)
        gl.glColor3f(1.0,1.0,1.0)
        for edge in self.edges:
            gl.glVertex2f(edge.start.vx-camera.x, edge.start.vy-camera.y)
            gl.glVertex2f(edge.end.vx-camera.x, edge.end.vy-camera.y)
        gl.glEnd()

        if self.selected:
            s = self.selected
            sz = 4
            gl.glBegin(gl.GL_QUADS)
            gl.glColor3f(1.0,0.0,0.0)
            gl.glVertex2d(s.vx-sz-camera.x, s.vy-sz-camera.y)
            gl.glVertex2d(s.vx-sz-camera.x, s.vy+sz-camera.y)
            gl.glVertex2d(s.vx+sz-camera.x, s.vy+sz-camera.y)
            gl.glVertex2d(s.vx+sz-camera.x, s.vy-sz-camera.y)
            gl.glEnd()




        
            
            
            



