from cmu_graphics import *
import random

class SAMLetter:
    def __init__(self, letter, x, y):
        self.letter = letter
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30

    def draw(self):
        drawRect(self.x, self.y, self.width, self.height, fill='orange')
        drawLabel(self.letter, self.x + self.width/2, self.y + self.height/2, size=20, bold=True)

    def update(self, speed):
        self.x -= speed


def nextSAMLetter(app):
    if app.samProgress == []:
        return 'S'
    elif app.samProgress == ['S']:
        return 'A'
    elif app.samProgress == ['S', 'A']:
        return 'M'
    else:
        return None


def spawnSAMLetter(app):
    # long delay before initial spawn
    if app.steps < 5 * app.stepsPerSecond:
        return 

    if not app.inSAMMode and app.samCooldown <= 0 and len(app.samLetters) == 0:
        nextLetter = nextSAMLetter(app)
        if nextLetter is not None:
            # attempt to spawn the letter a max of 10 times (that should be enough)
            for _ in range(10):
                x = app.width + 100
                y = random.randint(100, app.height - 100)
                if not isOverlapping(x + 15, y + 15, 15, app.obstacles.obstacles):
                    app.samLetters.append(SAMLetter(nextLetter, x, y))
                    app.samCooldown = 500
                    break
    else:
        app.samCooldown -= 1

def updateSAMLetters(app):
    for letter in app.samLetters:
        letter.update(app.speed)


def collectSAMLetters(app):
    collected = []
    for letter in app.samLetters:
        if app.player.collidesWith(letter):
            collected.append(letter)
            app.samProgress.append(letter.letter)
            if app.samProgress == ['S', 'A', 'M']:
                app.inSAMMode = True
                app.samTimer = 20 * app.stepsPerSecond
                app.samProgress.clear()
    for letter in collected:
        app.samLetters.remove(letter)


def updateSAMMode(app):
    if app.inSAMMode:
        app.samTimer -= 1
        if app.samTimer <= 0:
            app.inSAMMode = False

def drawSAMLetters(app):
    for letter in app.samLetters:
        letter.draw()

def isOverlapping(x, y, radius, obstacles):
    for obs in obstacles:
        if (x + radius > obs.x and x - radius < obs.x + obs.width and
            y + radius > obs.y and y - radius < obs.y + obs.height):
            return True
    return False