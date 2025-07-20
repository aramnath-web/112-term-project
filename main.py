from cmu_graphics import *
from player import Player

def onAppStart(app):
    app.player = Player(100, 200)
    app.width = 700
    app.length = 700

def onStep(app):
    app.player.update()

def onKeyHold(app, keys):
    app.player.setJetpack('space' in keys)

def onKeyRelease(app, key):
    if key == 'space':
        app.player.setJetpack(False)

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='skyBlue')
    app.player.draw()

runApp()