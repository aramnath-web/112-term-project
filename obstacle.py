#handle obstacle spawning

from cmu_graphics import *
import random

class Obstacle:
    def __init__(self, x, y, width=20, height=80):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update(self):
        self.x -= app.speed

    def draw(self):
        drawRect(self.x, self.y, self.width, self.height, fill='red')

    def isOffScreen(self):
        return self.x + self.width < 0
    
class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.stepCount = 0

    def update(self):

        self.stepCount+=1

        for obs in self.obstacles:
            obs.update()
            if app.player.collidesWith(obs):
                app.gameOver = True

    # remove off-screen obstacles
        self.obstacles = [obs for obs in self.obstacles if not obs.isOffScreen()]

    # spawn obstacles
        if self.stepCount >= 60:
            y = random.randint(100, 450)
            obstacle = Obstacle(app.width, y)

            # check coin overlap
            overlaps = False
            for coin in app.coins.coins:
                if (obstacle.x < coin.x + coin.radius and obstacle.x + obstacle.width > coin.x - coin.radius and
                    obstacle.y < coin.y + coin.radius and obstacle.y + obstacle.height > coin.y - coin.radius):
                    overlaps = True
                    break

            if not overlaps:
                self.obstacles.append(obstacle)

            self.stepCount = 0
    
    def draw(self):
        for obs in self.obstacles:
            obs.draw()


