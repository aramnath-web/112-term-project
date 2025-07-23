from cmu_graphics import *

class Coin:
    def __init__(self, x, y, radius=10):
        self.x = x
        self.y = y
        self.radius = radius
        self.collected = False

    def update(self):
        self.x -= 6

    def draw(self):
        if not self.collected:
            drawCircle(self.x, self.y, self.radius, fill='gold')

    def collect(self, player):
        dx = self.x - player.x
        dy = self.y - player.y
        distance = (dx**2 + dy**2)**0.5
        return distance <= self.radius + 20  # 20 = player's radius
