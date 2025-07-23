from cmu_graphics import *
from player import Player
from obstacle import Obstacle
from coin import Coin
import random

def onAppStart(app):
    app.width = 800
    app.height = 500
    app.player = Player(100, 200)
    app.obstacles = []
    app.coins = []
    app.score = 0
    app.spawnTimer = 0
    app.gameOver = False

def onStep(app):
    if app.gameOver:
        return

    app.player.update()

    # update coin if offscreen or collected
    for coin in app.coins:
        coin.update()
        if not coin.collected and coin.collect(app.player):
            coin.collected = True
            app.score+=1


    app.coins = [c for c in app.coins if c.x + c.radius >0]
    if len(app.coins)<5:
        x = max(c.x for c in app.coins) + 150 if app.coins else 400
        y = random.randint(100, 400)
        app.coins.append(Coin(x, y))


    app.spawnTimer += 1
    if app.spawnTimer >= 60:
        y = random.randint(100, 400)
        app.obstacles.append(Obstacle(app.width, y))
        app.spawnTimer = 0

    # make sure they are not off screen
    for obs in app.obstacles:
        obs.update()
    app.obstacles = [obs for obs in app.obstacles if not obs.isOffScreen()]

    # spawn lasers
    app.spawnTimer += 1
    if app.spawnTimer >= 60:
        y = random.randint(100, 400)
        app.obstacles.append(Obstacle(app.width, y))
        app.spawnTimer = 0



def onKeyHold(app, keys):
    if 'space' in keys:
        app.player.setJetpack(True)

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

    for coin in app.coins:
        coin.draw()
    drawLabel(f'Score: {app.score}', 50, 20, size=16, bold=True)
    if app.gameOver:
        drawLabel("Game Over!", app.width//2, app.height//2, size=32, bold=True, fill='red')
        drawLabel("Press R to restart", app.width//2, app.height//2 + 40, size=16)

runApp()
