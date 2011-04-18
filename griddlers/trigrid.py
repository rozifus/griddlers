
from pyglet import gl

class Edge(object):
    def __init__(self, start, end):
        self.filling = None
        self.start = start
        self.end = end


class TriNode(object):
    def __init__(self, x, y):
        self.content = None
        self.x, self.y = x, y
        self.vx, self.vy = x, y
        self.e1 = self.e2 = self.e3 = None
        self.e4 = self.e5 = self.e6 = None 



class TriGrid(object):
    def __init__(self, parent, x, y, sizex, sizey):
        self.parent = parent
        self.x, self.y = x, y
        self.xs, self.ys = sizex, sizey
        self.nodes = {}
        self.edges = [] 

        for x,y in self.generateBaseNodePositions():
            self.nodes[(x,y)] = TriNode(x,y)

        for node in self.nodes.values():
            conn = self.getNodeAt(node.x - self.xs, node.y + self.ys)
            if conn:
                edge = Edge(conn, node)
                node.p1 = edge
                conn.p6 = edge
                self.edges.append(edge)
            conn = self.getNodeAt(node.x - self.xs * 2, node.y)
            if conn:
                edge = Edge(conn, node)
                node.p2 = edge 
                node.p5 = edge
                self.edges.append(edge)
            conn = self.getNodeAt(node.x - self.xs, node.y - self.ys)
            if conn:
                edge = Edge(conn, node)
                node.p3 = edge 
                node.p4 = edge
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
                print(li)
                line = linearMap[li*self.x: (li+1)*self.x]
                print(line)
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
            node = self.nodes[(x,y)] 
            applyContour(node, contourGen.next())
    
        
    def getNodeAt(self, x, y):
        return self.nodes.get((x,y), None)

    def activate(self):
        self.parent.push_handlers(level_draw=self.draw)

    def draw(self, camera):
        gl.glLoadIdentity()
        gl.glBegin(gl.GL_LINES)
        gl.glColor3f(1.0,1.0,1.0)
        for edge in self.edges:
            gl.glVertex2f(edge.start.vx-camera.x, edge.start.vy-camera.y)
            gl.glVertex2f(edge.end.vx-camera.x, edge.end.vy-camera.y)
        gl.glEnd()


        
            
            
            



