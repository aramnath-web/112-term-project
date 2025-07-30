'''
Name: Aarav Ramnath

15-112 Term Project: Fly-112 (Jetpack Joyride)

All sprites were obtained from Youtuber McGuy's graphics drive (link: https://drive.google.com/drive/folders/1CVSYtoVMUeBIWUkbAELKBiTWkDCn8BJs)

AI was used in some of the logic and will be cited wherever used in each file
'''


from cmu_graphics import *
from player import Player
from obstacle import Obstacle, ObstacleManager
from coin import CoinManager
import random

def onAppStart(app):
    app.stepsPerSecond=60
    app.width = 800
    app.height = 500
    app.mainMenuMusic = Sound('assets/Jetpack Joyride OST  - Main Theme.mp3')
    app.bgX = app.width/2
    app.bgSprite = 'assets/BackdropMain.png'
    app.bgWidth = app.width + 47
    app.logo = 'assets/JetpackJoyride.png'
    app.menuBG = 'assets/BackdropEntry.png'
    app.logoWidth, app.logoHeight = None, None
    app.player = None
    app.obstacles = None
    app.coins = None
    app.score = None
    app.gameOver = None
    app.steps = None
    app.speed=None


#######################################
# Menu
#######################################

def menu_onScreenActivate(app):
    app.logoWidth, app.logoHeight = getImageSize(app.logo)

def menu_redrawAll(app):
    drawImage(app.menuBG, 0, 0, width = app.width, height = app.height)
    drawImage(app.logo, app.width/2, app.height/2-100, width = app.logoWidth/2, height = app.logoHeight/2, align='center')
    drawLabel('An Aarav Ramnath Project', app.width/2, app.height/2+15, fill='white', bold=True, size=20)
    drawRect(app.width/2, app.height/2+100, 150, 75, align = 'center', fill = 'red', border = 'black', borderWidth=2)
    drawRect(app.width/2-200, app.height/2+100, 150, 75, align = 'center', fill = 'red', border = 'black', borderWidth=2)
    drawRect(app.width/2+200, app.height/2+100, 150, 75, align = 'center', fill = 'red', border = 'black', borderWidth=2)
    drawLabel('Play', app.width/2-200, app.height/2+100, bold=True, fill='white', size=30)
    drawLabel('Leaderboard', app.width/2, app.height/2+100, bold=True, fill='white', size=20)
    drawLabel('Settings', app.width/2+200, app.height/2+100, bold=True, fill='white', size=30)

def menu_onMousePress(app, mouseX, mouseY):
    # button width, height, and center y
    bw = 150
    bh = 75
    cy = app.height/2 + 100

    # play button code
    playX = app.width/2 - 200
    if (playX - bw/2 <= mouseX <= playX + bw/2 and
        cy - bh/2 <= mouseY <= cy + bh/2):
        setActiveScreen('game')
        return

    leaderboardX = app.width/2
    if (leaderboardX - bw/2 <= mouseX <= leaderboardX + bw/2 and
        cy - bh/2 <= mouseY <= cy + bh/2):
        print('placeholder')
        return

    settingsX = app.width/2 + 200
    if (settingsX - bw/2 <= mouseX <= settingsX + bw/2 and
        cy - bh/2 <= mouseY <= cy + bh/2):
        print('placeholder')
        return

#######################################
# Game
#######################################

def game_onScreenActivate(app):
    app.mainMenuMusic.play(restart=True, loop=True)
    app.player = Player(100, 200)
    app.obstacles = ObstacleManager()
    app.coins = CoinManager()
    app.score = 0
    app.gameOver = False
    app.steps = 0
    app.speed=2.5
def isOverlapping(x, y, radius, obstacles):
    for obs in obstacles:
        if (x + radius > obs.x and x - radius < obs.x + obs.width and
            y + radius > obs.y and y - radius < obs.y + obs.height):
            return True
    return False


# goal of onstep: move player, spawn obstacles and coins
def game_onStep(app):

    # update positions for each entity
    app.player.update(app.steps, app.gameOver)
    if app.gameOver:
        return
    app.coins.update()
    app.obstacles.update()
    collectCoins(app)

    app.steps+=1

    # background scrolling
    app.bgX -= app.speed
    if app.bgX <= -app.bgWidth / 2:
        app.bgX += app.bgWidth

    if not app.gameOver:
        app.speed+=.0025

def collectCoins(app):
    collected = []
    for coin in app.coins.coins:
        if isCoinCollected(app.player, coin):
            collected.append(coin)
            app.score += 1

    for coin in collected:
        app.coins.coins.remove(coin)

# new collision between hitbox and coin
def isCoinCollected(player, coin):
    playerCenterX, playercy, playerWidth, playerHeight = player.getHitbox()

    nearestX = max(playerCenterX - playerWidth/2,
                   min(coin.x, playerCenterX + playerWidth/2))
    nearestY = max(playercy - playerHeight/2,
                   min(coin.y, playercy + playerHeight/2))

    dx = coin.x - nearestX
    dy = coin.y - nearestY

    return (dx**2 + dy**2) < coin.radius**2

def game_onKeyHold(app, keys):
    if 'space' in keys:
        app.player.setJetpack(True)

def game_onKeyRelease(app, key):
    if key == 'space':
        app.player.setJetpack(False)
def game_onKeyPress(app, key):
    if key == 'r' and app.gameOver:
        setActiveScreen('game')


def game_redrawAll(app):
    drawImage(app.bgSprite, app.bgX, app.height/2+4, width=app.bgWidth, height=app.height+21, align='center')
    drawImage(app.bgSprite, app.bgX + app.bgWidth, app.height/2+4, width=app.bgWidth, height=app.height+21, align = 'center')

    # draw player, lasers, coins
    app.player.draw()

    app.obstacles.draw()

    app.coins.draw()
    drawLabel(f"Score: {app.score}", 60, 30, size=20, bold=True)

    # game over message
    if app.gameOver:
        drawLabel("Game Over!", app.width//2, app.height//2, size=32, bold=True, fill='red')
        drawLabel("Press R to restart", app.width//2, app.height//2 + 40, size=16)
        app.mainMenuMusic.pause()
def main():
    runAppWithScreens(initialScreen='menu')
main()