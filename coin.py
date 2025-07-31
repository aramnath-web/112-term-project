#handle coin spawning

from cmu_graphics import *
import random
import math

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10

    def draw(self):
        # didn't bother to use sprite, just made my own
        drawCircle(self.x, self.y, self.radius, fill='gold', border='orange', borderWidth=2)

    def update(self):
        self.x -= app.speed

    def isOffScreen(self):
        return self.x < -self.radius

class CoinManager:
    def __init__(self):
        self.coins = []
        self.stepCount = 0

    def update(self):
        self.stepCount += 1

        # move coin
        for coin in self.coins:
            coin.update()

        # remove old coins
        self.coins = [coin for coin in self.coins if not coin.isOffScreen()]

        # spawn coins
        if self.stepCount % 60 == 0:
            self.spawnFormation()

    def draw(self):
        for coin in self.coins:
            coin.draw()

    def spawnFormation(self):
        formationType = random.choice(['line', 'arc', 'column'])

        # get pos for coin
        x = max((coin.x for coin in self.coins), default=app.width) + 60 * app.speed
        y = random.randint(100, app.height - 150)

        if formationType == 'line':
            newCoins = self.spawnLine(x, y, count=5, spacing=30)
        elif formationType == 'arc':
            newCoins = self.spawnArc(x, y, count=7, spacing=25, amplitude=50)
        elif formationType == 'column':
            newCoins = self.spawnColumn(x, y, count=6, spacing=25)

        # keep coins that dont overlap
        filteredCoins = []
        for coin in newCoins: # type: ignore (it had a red line and was bothering me yet nothing was wrong)
            if not isOverlapping(coin.x, coin.y, coin.radius, app.obstacles.obstacles):
                filteredCoins.append(coin)

        self.coins += filteredCoins

    def spawnLine(self, xStart, yStart, count, spacing):
        return [Coin(xStart + i * spacing, yStart) for i in range(count)]

    # this formation was very weird to implement so i asked chatgpt the math behind it
    def spawnArc(self, xStart, yCenter, count, spacing, amplitude):
        return [Coin(xStart + i * spacing, yCenter + amplitude * math.sin(i * math.pi / (count - 1)))
                for i in range(count)]

    def spawnColumn(self, xStart, yStart, count, spacing):
        return [Coin(xStart, yStart + i * spacing) for i in range(count)]
    
    
def isOverlapping(x, y, radius, obstacles):
    for obs in obstacles:
        if (x + radius > obs.x and x - radius < obs.x + obs.width and
            y + radius > obs.y and y - radius < obs.y + obs.height):
            return True
    return False