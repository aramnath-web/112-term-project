from cmu_graphics import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dy = 0
        self.gravity = 0.5
        self.thrust = -7
        self.isJetpacking = False

    def update(self):
        if self.isJetpacking:
            self.dy = self.thrust
        else:
            self.dy += self.gravity
        self.dy = max(-8, min(8, self.dy))
        self.y += self.dy
        self.y = max(20, min(380, self.y))

    def setJetpack(self, state):
        self.isJetpacking = state

    def draw(self):
        drawCircle(self.x, self.y, 20, fill='orange')
