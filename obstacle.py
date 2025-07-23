from cmu_graphics import *

class Obstacle:
    def __init__(self, x, y, width=20, height=80):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update(self):
        self.x -= 6

    def draw(self):
        drawRect(self.x, self.y, self.width, self.height, fill='red')

    def isOffScreen(self):
        return self.x + self.width < 0
