'''
Name: Aarav Ramnath

15-112 Term Project: Fly-112 (Jetpack Joyride)

Most sprites were obtained from Youtuber McGuy's graphics drive (link: https://drive.google.com/drive/folders/1CVSYtoVMUeBIWUkbAELKBiTWkDCn8BJs)

AI was used in some of the logic and will be cited wherever used in each file

Main logo image was taken from the Jetpack Joyride fandom
'''


from cmu_graphics import *
from player import Player
from obstacle import Obstacle, ObstacleManager
from coin import CoinManager
from leaderboard import * 
from powerup import *
import random

def onAppStart(app):
    app.stepsPerSecond=60
    app.width = 800
    app.height = 500
    app.mainTheme = Sound('assets/Jetpack Joyride OST  - Main Theme.mp3')
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
    app.leaderboardData = loadLeaderboard()
    app.ran = False
    app.username = ''
    app.maxNameLength = 10  # don't want to mess up the leaderboards with a super long name
    app.muted = False
    app.samLetters = []
    app.samProgress = []
    app.samCooldown = 1200
    app.inSAMMode = False
    app.samTimer = 0 


#######################################
# Settings
#######################################

def settings_onScreenActivate(app):
    pass

def settings_redrawAll(app):
    drawImage(app.menuBG, 0, 0, width = app.width, height = app.height)
    drawLabel('Settings', app.width/2, 50, size=40, bold=True, fill='white')

    # music button
    drawRect(app.width/2, 150, 200, 50, align='center', fill='gray')
    drawLabel(f'Music: {"Off" if app.muted else "On"}', app.width/2, 150, size=20, fill='white')

    # username button
    drawRect(app.width/2, 240, 200, 50, align='center', fill='gray')
    drawLabel('Change User', app.width/2, 240, size=20, fill='white')

    # back button
    drawRect(app.width/2, 330, 150, 40, align='center', fill='red')
    drawLabel('Back', app.width/2, 330, size=20, fill='white')

def settings_onMousePress(app, x, y):
    if app.width/2 - 100 <= x <= app.width/2 + 100 and 125 <= y <= 175:
        app.muted = not app.muted

    elif app.width/2 - 100 <= x <= app.width/2 + 100 and 215 <= y <= 265:
        setActiveScreen('nameInput')

    elif app.width/2 - 75 <= x <= app.width/2 + 75 and 310 <= y <= 350:
        setActiveScreen('menu')

#######################################
# Input
#######################################

def nameInput_onScreenActivate(app):
    app.username = ''
    app.maxNameLength = 10 
def nameInput_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='black')
    drawLabel('Username:', app.width/2, app.height/2 - 50, size=30, fill='red')
    drawLabel(app.username + '|', app.width/2, app.height/2, size=24, fill='red')
    drawLabel('Press Enter to continue', app.width/2, app.height/2 + 50, size=16, fill='red')

def nameInput_onKeyPress(app, key):
    if key == 'enter' and app.username != '':
        setActiveScreen('menu')
    elif key == 'backspace':
        app.username = app.username[:-1]
    elif len(key) == 1 and len(app.username) < app.maxNameLength:
        app.username += key



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
    if (playX - bw/2 <= mouseX <= playX + bw/2 and cy - bh/2 <= mouseY <= cy + bh/2):
        setActiveScreen('game')

    # leaderboard button code
    leaderboardX = app.width/2
    if (leaderboardX - bw/2 <= mouseX <= leaderboardX + bw/2 and cy - bh/2 <= mouseY <= cy + bh/2):
        setActiveScreen('leaderboard')

    # settings button code
    settingsX = app.width/2 + 200
    if (settingsX - bw/2 <= mouseX <= settingsX + bw/2 and cy - bh/2 <= mouseY <= cy + bh/2):
        setActiveScreen('settings')

######################################
# Leaderboard
######################################


def leaderboard_onScreenActivate(app):
    app.leaderboardData = loadLeaderboard()

def leaderboard_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='black')

    drawLabel("Leaderboard", app.width//2, 50, size=40, bold=True, fill='white')
    
    if not app.leaderboardData:
        drawLabel("No scores found", app.width//2, app.height//2, size=20, fill='white')
    else:
        # AI recommended I use enumerate to parse list data, but the code was implemented by me
        for i, entry in enumerate(app.leaderboardData):
            name, score = entry
            drawLabel(f"{i+1}. {name} - {score}", app.width//2, 100 + i*30, size=20, fill='white')

    drawRect(app.width//2, app.height - 60, 150, 50, align='center', fill='red')
    drawLabel("Back", app.width//2, app.height - 60, size=20, fill='white', bold=True)


def leaderboard_onMousePress(app, mouseX, mouseY):
    backX = app.width//2
    backY = app.height - 60
    if (backX - 75 <= mouseX <= backX + 75 and backY - 25 <= mouseY <= backY + 25):
        setActiveScreen('menu')


#######################################
# Game
#######################################

def game_onScreenActivate(app):
    if not app.muted:
        app.mainTheme.play(restart=True, loop=True)
    app.player = Player(100, 200)
    app.obstacles = ObstacleManager()
    app.coins = CoinManager()
    app.score = 0
    app.gameOver = False
    app.steps = 0
    app.speed=2.5
    app.ran = False
    app.samLetters = []
    app.samProgress = []
    app.samCooldown = 1200
    app.inSAMMode = False
    app.samTimer = 0 



# goal of onstep: move player, spawn obstacles and coins

def game_onStep(app):
    app.player.update(app.steps, app.gameOver)
    if not app.gameOver:
        takeStep(app)
    elif app.gameOver and not app.ran:
        if not app.muted:
            app.mainTheme.pause()
        addScore(app.username, app.score)
        app.ran=True

def takeStep(app):
    # update positions for each entity    
    app.coins.update()
    app.obstacles.update()
    spawnSAMLetter(app)
    updateSAMLetters(app)
    collectSAMLetters(app)
    updateSAMMode(app)
    collectCoins(app)

    app.steps+=1

    # background scrolling
    app.bgX -= app.speed
    if app.bgX <= -app.bgWidth / 2:
        app.bgX += app.bgWidth

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

    nearestX = max(playerCenterX - playerWidth/2, min(coin.x, playerCenterX + playerWidth/2))
    nearestY = max(playercy - playerHeight/2, min(coin.y, playercy + playerHeight/2))

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
    elif key =='m' and app.gameOver:
        setActiveScreen('menu')


def game_redrawAll(app):
    drawImage(app.bgSprite, app.bgX, app.height/2+4, width=app.bgWidth, height=app.height+21, align='center')
    drawImage(app.bgSprite, app.bgX + app.bgWidth, app.height/2+4, width=app.bgWidth, height=app.height+21, align = 'center')

    # draw player, lasers, coins
    app.player.draw()

    app.obstacles.draw()

    app.coins.draw()
    drawLabel(f"Score: {app.score}", 60, 30, size=20, bold=True)

    drawSAMLetters(app)

    # game over message
    if app.gameOver:
        drawLabel("Game Over!", app.width//2, app.height//2, size=32, bold=True, fill='red')
        drawLabel("Press R to restart", app.width//2, app.height//2 + 40, size=16)
        drawLabel("Press M to return to the menu", app.width//2, app.height//2 + 60, size=16)
def main():
    runAppWithScreens(initialScreen='nameInput')
main()