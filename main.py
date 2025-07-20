from cmu_graphics import *

def onAppStart(app):
    app.width = 400
    app.height = 400
    app.playerY = 200
    app.playerDY = 0
    app.gravity = .5
    app.jetpackThrust = -7
    app.scrollX = 0

def onStep(app):
    # Update gravity
    app.playerDY += app.gravity
    app.playerY += app.playerDY
    app.scrollX -= 2
    app.playerY = max(20, min(app.height, app.playerY))
    app.playerY = min(380, min(app.height, app.playerY))

def onKeyHold(app, keys):
    if 'space' in keys:
        app.playerDY = app.jetpackThrust

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='skyBlue')
    drawCircle(100, app.playerY, 20, fill='orange')  # Player
    drawLabel("Jetpack Joyride", app.width//2, 20, size=20, bold=True)

runApp()