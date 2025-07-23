from cmu_graphics import *
import random, math

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10

    def draw(self):
        drawCircle(self.x, self.y, self.radius, fill='gold', border='orange', borderWidth=2)

    def update(self, speed=6):
        self.x -= speed

    def isOffScreen(self):
        return self.x < -self.radius

class CoinManager:
    def __init__(self):
        self.coins = []
        self.stepCount = 0

    def update(self):
        self.stepCount += 1

        # Update coin positions
        for coin in self.coins:
            coin.update()

        # Remove offscreen coins
        self.coins = [coin for coin in self.coins if not coin.isOffScreen()]

        # Spawn new formations every 30 frames
        if self.stepCount % 30 == 0:
            self.spawnFormation()

    def draw(self):
        for coin in self.coins:
            coin.draw()

    def spawnFormation(self):
        formationType = random.choice(['line', 'arc', 'column'])

        # Get x-position based on last coin (or default)
        x = max((coin.x for coin in self.coins), default=app.width) + 200
        y = random.randint(100, app.height - 100)

        # Choose the formation and create coins
        if formationType == 'line':
            newCoins = self.spawnLine(x, y, count=5, spacing=30)
        elif formationType == 'arc':
            newCoins = self.spawnArc(x, y, count=7, spacing=25, amplitude=50)
        elif formationType == 'column':
            newCoins = self.spawnColumn(x, y, count=6, spacing=25)

        # Only keep coins that don't overlap obstacles
        filteredCoins = []
        for coin in newCoins:
            if not isOverlapping(coin.x, coin.y, coin.radius, app.obstacles):
                filteredCoins.append(coin)

        self.coins += filteredCoins

    def spawnLine(self, xStart, yStart, count, spacing):
        return [Coin(xStart + i * spacing, yStart) for i in range(count)]

    def spawnArc(self, xStart, yCenter, count, spacing, amplitude):
        return [Coin(xStart + i * spacing,
                     yCenter + amplitude * math.sin(i * math.pi / (count - 1)))
                for i in range(count)]

    def spawnColumn(self, xStart, yStart, count, spacing):
        return [Coin(xStart, yStart + i * spacing) for i in range(count)]
    
    
def isOverlapping(x, y, radius, obstacles):
    for obs in obstacles:
        if (x + radius > obs.x and x - radius < obs.x + obs.width and
            y + radius > obs.y and y - radius < obs.y + obs.height):
            return True
    return False