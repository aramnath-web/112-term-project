#handle obstacle spawning

from cmu_graphics import *
import random

class Obstacle:
    def __init__(self, x, y, width=20, height=80):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = 'assets/NewZapper.png'

    def update(self):
        self.x -= app.speed

    def draw(self):
        drawImage(self.image, self.x-5, self.y-5, width = self.width+10, height = self.height+10)

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
            if app.player.collidesWith(obs) and not app.inSAMMode:
                app.gameOver = True

    # remove off-screen obstacles
        self.obstacles = [obs for obs in self.obstacles if not obs.isOffScreen()]

    # spawn obstacles
        if self.stepCount >= 40:
            y = random.randint(30, 400)
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


