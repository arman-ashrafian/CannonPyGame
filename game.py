import pygame as pg
import sys
import math
import random
import brain

pg.init()

# holds x, y, angle
hitArray = [[], [], []]

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
LGREY = (150,150,150)

colorList = [BLACK, GREEN, RED, BLUE]

WIDTH = 800
HEIGHT = 800
CENTERX = int(WIDTH/2)
CENTERY = int(HEIGHT/2)

size = (WIDTH, HEIGHT)
screen = pg.display.set_mode(size)
pg.display.set_caption("Boom Pow")

# Set up
clock = pg.time.Clock()
fps = 80

fontObj = pg.font.SysFont('monospace', 32, bold=True)
fontObj2 = pg.font.SysFont('monospace', 18, bold=True)

class Ball:
    global hitArray

    speedY = 0
    speedX = 0

    printOnce = False

    def __init__(self, angleShot, speed, color, pos):
        self.angleShot = angleShot
        self.speedX = speed
        self.speedY = speed
        self.color = color
        self.x = pos[0]
        self.y = pos[1]


    def updateBall(self):
        vx0 = self.speedX * math.cos(math.radians(90 + self.angleShot))
        vy0 = self.speedY * math.sin(math.radians(90 + self.angleShot))

        self.x = int(self.x + vx0)
        self.y = int(self.y - vy0)
        self.speedY -= .3

        pg.draw.circle(screen, self.color, (self.x, self.y), 20,0)

    def checkHit(self, target, cannonAngle):
        if((self.x > target.x - target.radius and self.x < target.x + target.radius) and
           (self.y > target.y - target.radius and self.y < target.y + target.radius)):
           target.hit = True
           hitArray[0].append(target.x)
           hitArray[1].append(target.y)
           hitArray[2].append(cannonAngle)

class Cannon:
    xTop = 0
    yTop = 0

    def __init__(self):
        pass

    def drawCannon(self, cannonDegrees):
        barrelX = 110
        barrelY = HEIGHT - 100

        # barrel surface
        bsurf = pg.Surface((40,100))
        bsurf.fill(RED)
        bsurf.set_colorkey(WHITE)

        barrelRect = pg.draw.rect(bsurf, RED, (0,0,40,100))

        rotatedSurf = pg.transform.rotate(bsurf, cannonDegrees)
        rotRect = rotatedSurf.get_rect()
        rotRect.center = (barrelX, barrelY)

        screen.blit(rotatedSurf, rotRect)

        # base
        pg.draw.rect(screen, BLUE, (10,HEIGHT-100,200,100))

        self.xTop = rotRect.center[0] + (20 * math.cos(math.radians(90 + cannonDegrees)))
        self.yTop = rotRect.center[1] - (20 * math.sin(math.radians(90 + cannonDegrees)))

class Target:
    hit = False

    def __init__(self):
        self.x = random.randint(150, 650)
        self.y = random.randint(150, 550)
        self.radius = 50
        self.hit = False

    def show(self):
        pg.draw.circle(screen, RED, (self.x, self.y), self.radius,0)


def gameIntro():
    global screen

    buttonPressed = False
    screen.fill(LGREY)

    introText = "Shoot Stuff"
    pressText = "Press any key to play"

    while not buttonPressed:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                buttonPressed = True

        screen.fill(LGREY)

        introTextObj = fontObj.render(introText, True, WHITE)
        directionTextObj = fontObj2.render(pressText, True, WHITE)

        screen.blit(introTextObj,
                    (int(WIDTH/2) - introTextObj.get_width() // 2,
                     int(HEIGHT/2) - introTextObj.get_height() // 2))
        screen.blit(directionTextObj,
                    ((int(WIDTH/2) - directionTextObj.get_width() // 2,
                      int(HEIGHT/2) - introTextObj.get_height() // 2 + 50)))

        pg.display.update()
        clock.tick(fps)


def gameLoop():
    done = False

    cannonAngle = 0
    cannonAngleChange = 0
    ballsShot = []

    cannon = Cannon()
    target = Target()

    shotDisabled = False

    #----Main Loop----#
    while not done:
        # clear screen
        screen.fill(WHITE)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    cannonAngleChange = -1
                if event.key == pg.K_LEFT:
                    cannonAngleChange = 1
                if event.key == pg.K_SPACE:
                    if not shotDisabled:
                        randomIndex = random.randint(0, 3)
                        # newBall = Ball(cannonAngle, 18, colorList[randomIndex],
                        #                (cannon.xTop, cannon.yTop))
                        newBall = Ball(brain.getAngle(), 18, colorList[randomIndex],
                                       (cannon.xTop, cannon.yTop))
                        ballsShot.append(newBall)
            if event.type == pg.KEYUP:
                cannonAngleChange = 0


        # --- Game Logic

        # cannon boundries
        if(cannonAngle + cannonAngleChange <= 70 and
           cannonAngle + cannonAngleChange >= -70):
            cannonAngle += cannonAngleChange


        # --- Drawing
        cannon.drawCannon(cannonAngle)
        target.show()

        for b in ballsShot:
            if b.x > WIDTH + 30 or b.x < 0 - 30 or b.y < 0 or b.y > HEIGHT:
                ballsShot.remove(b)
                if target.hit:
                    # create new target if hit=True and ball is off screen
                    target = Target()
                    shotDisabled = False
            else:
                b.updateBall()

            b.checkHit(target, cannonAngle)

            # hide target if hit
            if target.hit:
                target.radius = 0
                shotDisabled = True

        # --- update screen
        pg.display.flip()
        clock.tick(fps)

def runGame():
    gameIntro()
    gameLoop()
    pg.quit()

if __name__ == '__main__':
    runGame()
