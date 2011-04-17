
from pyglet import gl

class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.filled = False


class TriNode:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.e1 = self.e2 = self.e3 = None
        self.e4 = self.e5 = self.e6 = None 



class TriGrid:
    def __init__(self, parent, x, y, sizex, sizey):
        self.parent = parent
        self.x, self.y = x,y
        self.xs, self.ys = sizex, sizey
        self.nodes = {}
        self.edges = [] 

        shift = 1 
        for x in range(0, self.x*self.xs, self.xs):
            if shift == 1: 
                shift = 0 
            else: shift = 1 
            for y in range(0, self.y*self.ys + self.ys, self.ys*2):
                if shift == 1: y += self.ys 
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

        
    def getNodeAt(self, x, y):
        return self.nodes.get((x,y), None)

    def draw(self):
        gl.glLoadIdentity()
        gl.glBegin(gl.GL_LINES)
        gl.glColor3f(1.0,1.0,1.0)
        for edge in self.edges:
            gl.glVertex2f(edge.start.x, edge.start.y)
            gl.glVertex2f(edge.end.x, edge.end.y)
        gl.glEnd()


        
            
            
            



