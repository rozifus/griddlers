
class Sector(object):
    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.nodes = []
    
    def inSector(self, x, y):
        if x >= self.x and x < self.x+self.w \
        and y >= self.y and y < self.y+self.h:
            return True
        return False


