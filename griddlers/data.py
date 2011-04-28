'''Simple data loader module.

Loads data files from the "data" directory shipped with a game.

Enhancing this to handle caching etc. is left as an exercise for the reader.

Note that pyglet users should probably just add the data directory to the
pyglet.resource search path.
'''
import pyglet
import os

def userFile(filepath, filename, options='wt'):
    userdir = pyglet.resource.get_settings_path('griddlers')
    filedir = os.path.join(userdir, filepath)
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    fullpath = os.path.join(filedir, filename)
    userfile = open(fullpath, options)
    return userfile
    
maps = pyglet.resource.Loader('data'+os.sep+'maps')

pyglet.resource.reindex()

