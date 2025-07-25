from cmu_graphics import *
from player import Player
from obstacle import Obstacle, ObstacleManager
from coin import CoinManager
import random

#make sure to move obstacle spawning to the obstacle.py file
def onAppStart(app):
    app.width = 800
    app.height = 500
    app.player = Player(100, 200)
    app.obstacles = ObstacleManager()
    app.coins = CoinManager()
    app.score = 0
    app.gameOver = False

def isOverlapping(x, y, radius, obstacles):
    for obs in obstacles:
        if (x + radius > obs.x and x - radius < obs.x + obs.width and
            y + radius > obs.y and y - radius < obs.y + obs.height):
            return True
    return False


# goal of onstep: move player, spawn obstacles and coins
def onStep(app):
    if app.gameOver:
        return

    # update player position
    app.player.update()
    app.coins.update()
    app.obstacles.update()
    collectCoins(app)

    # move obstacles, detect collision
    



def collectCoins(app):
    collected = []
    for coin in app.coins.coins:
        if isCoinCollected(app.player, coin):
            collected.append(coin)
            app.score += 1

    for coin in collected:
        app.coins.coins.remove(coin)

def isCoinCollected(player, coin):
    dx = player.x - coin.x
    dy = player.y - coin.y
    distance = (dx**2 + dy**2)**0.5
    return distance < coin.radius + 20

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

    # draw player, lasers, coins
    app.player.draw()

    app.obstacles.draw()

    app.coins.draw()
    drawLabel(f"Score: {app.score}", 60, 30, size=20, bold=True)

    # game over message
    if app.gameOver:
        drawLabel("Game Over!", app.width//2, app.height//2, size=32, bold=True, fill='red')
        drawLabel("Press R to restart", app.width//2, app.height//2 + 40, size=16)

runApp()