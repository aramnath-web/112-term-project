from cmu_graphics import *
from player import Player
from obstacle import Obstacle
import random

def onAppStart(app):
    app.width = 400
    app.height = 400
    app.player = Player(100, 200)
    app.obstacles = []
    app.spawnTimer = 0
    app.gameOver = False

def onStep(app):
    if app.gameOver:
        return

    app.player.update()

    for obs in app.obstacles:
        obs.update()
        if app.player.collidesWith(obs):
            app.gameOver = True

    app.obstacles = [obs for obs in app.obstacles if not obs.isOffScreen()]

    app.spawnTimer += 1
    if app.spawnTimer >= 60:
        y = random.randint(100, 300)
        app.obstacles.append(Obstacle(app.width, y))
        app.spawnTimer = 0

    # Update obstacles
    for obs in app.obstacles:
        obs.update()
    app.obstacles = [obs for obs in app.obstacles if not obs.isOffScreen()]

    # Obstacle spawn logic
    app.spawnTimer += 1
    if app.spawnTimer >= 60:
        y = random.randint(100, 300)
        app.obstacles.append(Obstacle(app.width, y))
        app.spawnTimer = 0


def onKeyHold(app, keys):
    app.player.setJetpack('space' in keys)

def onKeyRelease(app, key):
    if key == 'space':
        app.player.setJetpack(False)
def onKeyPress(app, key):
    if key == 'r' and app.gameOver:
        onAppStart(app)


def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='skyBlue')

    for obs in app.obstacles:
        obs.draw()
    app.player.draw()

    if app.gameOver:
        drawLabel("Game Over!", app.width//2, app.height//2, size=32, bold=True, fill='red')
        drawLabel("Press R to restart", app.width//2, app.height//2 + 40, size=16)

runApp()
