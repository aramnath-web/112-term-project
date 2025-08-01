#handle player movement

from cmu_graphics import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dy = 0
        self.gravity = 0.25
        self.thrust = -5
        self.isJetpacking = False
        self.runningSprites = ['assets/BarryRun1.svg', 'assets/BarryRun2.svg', 'assets/BarryRun3.svg']
        self.flySprite = 'assets/BarryFly.svg'
        self.deadSprite = 'assets/BarryDead.svg'
        self.state = self.flySprite
        self.count = 0

    # logic for this hitbox was made by AI (i couldn't deal with the offset of the sprite)
    def getHitbox(self):
            return (self.x + 30, self.y + 30, 50, 50)
    def update(self, stepCount, dead):

        if dead:
            self.state = self.deadSprite
            self.y += 2.5
            if self.y>380:
                self.y = 380
        else:
            if self.isJetpacking:
                self.dy = self.thrust
            else:
                self.dy += self.gravity
            
            if self.y==380:
                self.state = self.runningSprites[self.count%2]
                self.count+=1 if stepCount%6==0 else 0
            else:
                self.state = self.flySprite
                self.count=0
            self.dy = max(-8, min(8, self.dy))
            self.y += self.dy
            self.y = max(20, min(app.height-20, self.y))
            if self.y>380:
                self.y = 380

    def setJetpack(self, state):
        self.isJetpacking = state

    def draw(self):
        if app.inSAMMode:
            if app.steps%5==0:
                drawImage(self.state, self.x, self.y)
        else:
            drawImage(self.state, self.x, self.y)
    
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
