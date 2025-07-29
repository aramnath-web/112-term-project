#handle player movement

from cmu_graphics import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dy = 0
        self.gravity = 0.5
        self.thrust = -7
        self.isJetpacking = False
        self.runningSprites = ['cmu://1055491/39834473/BarryRun1.svg', 'cmu://1055491/39834474/BarryRun2.svg', 'cmu://1055491/39834425/BarryRun3.svg']
        self.flySprite = 'assets/BarryFly.svg'
        self.state = self.flySprite

    def getHitbox(self):
            # This matches the red rectangle you're currently drawing
            return (self.x + 30, self.y + 30, 50, 50)

    def update(self):
        if self.isJetpacking:
            self.dy = self.thrust
        else:
            self.dy += self.gravity
        self.dy = max(-8, min(8, self.dy))
        self.y += self.dy
        self.y = max(20, min(app.height-20, self.y))
        if self.y>380:
            self.y = 380

    def setJetpack(self, state):
        self.isJetpacking = state

    def draw(self):
        drawImage(self.state, self.x, self.y)
        drawRect(self.x+30, self.y+30, 50, 50, align='center', fill=None, border='red')
    
    # rectangle and obstacle collision
    def collidesWith(self, rect):
        cx, cy, w, h = self.x + 30, self.y + 30, 50, 50
        rx, ry, rw, rh = rect.x, rect.y, rect.width, rect.height

        left1 = cx - w/2
        right1 = cx + w/2
        top1 = cy - h/2
        bottom1 = cy + h/2

        left2 = rx
        right2 = rx + rw
        top2 = ry
        bottom2 = ry + rh

        return (left1 < right2 and right1 > left2 and
                top1 < bottom2 and bottom1 > top2)
