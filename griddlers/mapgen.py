import random



class MapGen(object):
    DEFAULT_MATERIAL = 'g'
    DEFAULT_HEIGHT = '1'
    LAKE = 23 
    MOUNT = 29 
    def __init__(self, sizex, sizey, maptype=None): 
        self.sizex, self.sizey = sizex, sizey
        self.maptype = maptype

    def createDefaultMap(self):
        hgrid = '' 
        mgrid = '' 
        for y in range(self.sizey):
            for x in range(self.sizex):
                hgrid += MapGen.DEFAULT_HEIGHT
                mgrid += MapGen.DEFAULT_MATERIAL
        return hgrid, mgrid

                
                
            


        
        
