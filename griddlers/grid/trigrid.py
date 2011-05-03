from __future__ import print_function
from pyglet import gl
import math

from sector import Sector
from trinode import TriNode
from edge import Edge

class TriGrid(object):
    def __init__(self, p_level, xs, ys):
        self.p_level = p_level
        self.xs, self.ys = xs, ys
        self.x, y = None, None
        self.nodeMap = {}
        self.nodes = []
        self.sectors = []
        self.edges = [] 
        self.selected = None

    ########################
    # Initialization Methods

    def initializeBlank(self, x, y):
        self.x, self.y = x, y
        for x,y in self.generateBaseNodePositions():
            self.nodeMap[(x,y)] = TriNode(self,x,y)
    
        self.nodes = self.nodeMap.values()
        self.edges = self.initializeEdges()
        self.sectors = self.initializeSectors(None, None)

    def initializeJson(self, levelJson):
        import json
        d = json.loads(levelJson)
        self.initializeBlank(d['x'], d['y'])
        self.setAllJson(levelJson)

    def initializeEdges(self):
        edges = []
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
        return edges

    def initializeSectors(self, xs, ys):
        sectors = []
        winx, winy = self.p_level.p_game.p_window.get_size()
        #secxs, secys = winx + 2*xs, winy + 2*ys
        secxs, secys = winx*2/3, winy*2/3
        #secxs, secys = winx*2/5, winy*4/5
        #secxs, secys = winx/5, winy/5
        for nx,ny in self.nodeMap.keys():
            seced = False
            for sector in sectors:
                if sector.inSector(nx,ny):
                    seced = True
                    sector.nodes.append(self.nodeMap[nx,ny])
            if not seced:
                newx, newy = (nx/secxs)*secxs, (ny/secys)*secys
                newSector = Sector(newx, newy, secxs, secys)
                newSector.nodes.append(self.nodeMap[nx,ny])
                sectors.append(newSector)
        return sectors            

    #################
    # Helper Funtions

    def generateBaseNodePositions(self):
        shift = 1 
        for y in range(0, self.y*self.ys, self.ys):
            if shift == 1: 
                shift = 0 
            else: shift = 1 
            for x in range(0, self.x*self.xs*2, self.xs*2):
                if shift == 1: x += self.xs 
                yield x,y 
    
    def getContour(self):
        contourMap = '' 
        for x,y in self.generateBaseNodePositions():
            contourMap += self.nodeMap[(x,y)].z
        return contourMap        

    def setContour(self, contourMap):
        for i,xay in enumerate(self.generateBaseNodePositions()):
            self.nodeMap[xay].setZ(contourMap[i])

    def getMaterial(self):
        materialMap = '' 
        for x,y in self.generateBaseNodePositions():
            materialMap += self.nodeMap[(x,y)].mat
        return materialMap

    def setMaterial(self, materialMap):
        for i,xay in enumerate(self.generateBaseNodePositions()):
            self.nodeMap[xay].mat = materialMap[i]

    def getAllJson(self):
        import json
        d = {}
        d['x'], d['y'] = self.x, self.y
        d['material'] = self.getMaterial()
        d['contour'] = self.getContour()
        return json.dumps(d)

    def setAllJson(self, levelData):
        import json
        d = json.loads(levelData)
        if d['x'] == self.x and d['y'] == self.y:
            self.setMaterial(d['material'])
            self.setContour(d['contour'])
            return True
        return False

    def activate(self):
        self.p_level.push_handlers(self.level_draw)

    def deactivate(self):
        self.p_level.pop_handlers()

    ################
    # Node Functions 

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

        node0 = self.getNodeAt(left,top)
        if node0:
            minDist = getVisualDistance(node0, x, y)
            minNode = node0
            for node in generateNodeHex(node0):
                nDist = getVisualDistance(node, x, y)
                if nDist < minDist:
                    minDist = nDist
                    minNode = node

            return minNode 
        return None

    ######
    # Draw 

    def level_draw(self, camera):
        gl.glLoadIdentity()
        gl.glBegin(gl.GL_TRIANGLES)
        gl.glColor3f(1.0,1.0,1.0)
        secs = 0
        necs = 0
        for sector in self.sectors:
            if camera.inCamera(sector.x, sector.y, sector.w, sector.h):
                secs += 1
                for node in sector.nodes:
                    necs += 1
                    if node.e4:
                        node2 = node.e4.end
                        if node2.e6:
                            node3 = node2.e6.end
                            gl.glColor3f(*TriNode.color[node.mat])
                            gl.glVertex2f(node.vx-camera.x, node.vy-camera.y)
                            gl.glColor3f(*TriNode.color[node2.mat])
                            gl.glVertex2f(node2.vx-camera.x, node2.vy-camera.y)
                            gl.glColor3f(*TriNode.color[node3.mat])
                            gl.glVertex2f(node3.vx-camera.x, node3.vy-camera.y)
                    if node.e5:
                        node2 = node.e5.end
                        if node2.e3:
                            node3 = node2.e3.start
                            gl.glColor3f(*TriNode.color[node.mat])
                            gl.glVertex2f(node.vx-camera.x, node.vy-camera.y)
                            gl.glColor3f(*TriNode.color[node2.mat])
                            gl.glVertex2f(node2.vx-camera.x, node2.vy-camera.y)
                            gl.glColor3f(*TriNode.color[node3.mat])
                            gl.glVertex2f(node3.vx-camera.x, node3.vy-camera.y)
        gl.glEnd()
        #print(secs, necs)
        gl.glBegin(gl.GL_LINES)
        gl.glColor3f(1.0,1.0,1.0)
        for sector in self.sectors:
            if camera.inCamera(sector.x, sector.y, sector.w, sector.h):
                for node in sector.nodes:
                    for edge in node.leftEdgeList():
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
                    



        
            
            
            



