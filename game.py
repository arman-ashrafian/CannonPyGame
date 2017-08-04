import pygame as pg
import sys
import math
import random
import brain as mind

class Game:
    # holds x, y, angle
    hitArray = [[321],
                [387],
                [-28]]

    # Colors
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
    fps = 80

    screen = pg.display.set_mode(size)
    pg.display.set_caption("Cannon AI")
    clock = pg.time.Clock()


    # Constructor
    def __init__(self):
        pg.init() #-- initialize pygame
        self.fontObj = pg.font.SysFont('monospace', 32, bold=True)
        self.fontObj2 = pg.font.SysFont('monospace', 18, bold=True)

    def startGame(self):
        gameRunning = True
        self.screen.fill(self.LGREY)

        introText = "AI Cannon"
        pressText = "'T' for training mode, 'P' for play mode"

        while gameRunning:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    gameRunning = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_t:
                        self.user_play()
                    if event.key == pg.K_p:
                        self.cpu_play()

            self.screen.fill(self.LGREY)

            introTextObj = self.fontObj.render(introText, True, self.WHITE)
            directionTextObj = self.fontObj2.render(pressText, True, self.WHITE)

            self.screen.blit(introTextObj,
                        (int(self.WIDTH/2) - introTextObj.get_width() // 2,
                         int(self.HEIGHT/2) - introTextObj.get_height() // 2))
            self.screen.blit(directionTextObj,
                        ((int(self.WIDTH/2) - directionTextObj.get_width() // 2,
                          int(self.HEIGHT/2) - introTextObj.get_height() // 2 + 50)))

            pg.display.update()
            self.clock.tick(self.fps)

    def user_play(self):
        done = False

        cannonAngle = 0
        cannonAngleChange = 0
        ballsShot = []

        cannon = Cannon(self)
        target = Target(self)

        shotDisabled = False

        #----Main Loop----#
        while not done:
            # clear screen
            self.screen.fill(self.WHITE)

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
                            newBall = Ball(cannonAngle, 18, self.colorList[randomIndex],
                                           (cannon.xTop, cannon.yTop), self)
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
                if b.x > self.WIDTH + 30 or b.x < 0 - 30 or b.y < 0 or b.y > self.HEIGHT:
                    ballsShot.remove(b)
                    if target.hit:
                        # create new target if hit=True and ball is off screen
                        target = Target(self)
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
            self.clock.tick(self.fps)

    def cpu_play(self):
        brain = mind.Brain(self) # initialize brain

        done = False

        cannonAngle = 0
        cannonAngleChange = 0
        ballsShot = []

        cannon = Cannon(self)
        target = Target(self)

        shotDisabled = False

        #----Main Loop----#
        while not done:
            # clear screen
            self.screen.fill(self.WHITE)

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
                            newBall = Ball(brain.getAngle(target), 18, self.colorList[randomIndex],
                                           (cannon.xTop, cannon.yTop), self)
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
                if b.x > self.WIDTH + 30 or b.x < 0 - 30 or b.y < 0 or b.y > self.HEIGHT:
                    ballsShot.remove(b)
                    if target.hit:
                        # create new target if hit=True and ball is off screen
                        target = Target(self)
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
            self.clock.tick(self.fps)



class Ball:
    speedY = 0
    speedX = 0

    printOnce = False

    def __init__(self, angleShot, speed, color, pos, game):
        self.angleShot = angleShot
        self.speedX = speed
        self.speedY = speed
        self.color = color
        self.x = pos[0]
        self.y = pos[1]
        self.game = game


    def updateBall(self):
        vx0 = self.speedX * math.cos(math.radians(90 + self.angleShot))
        vy0 = self.speedY * math.sin(math.radians(90 + self.angleShot))

        self.x = int(self.x + vx0)
        self.y = int(self.y - vy0)
        self.speedY -= .3

        pg.draw.circle(self.game.screen, self.color, (self.x, self.y), 20,0)

    def checkHit(self, target, cannonAngle):
        if((self.x > target.x - target.radius and self.x < target.x + target.radius) and
           (self.y > target.y - target.radius and self.y < target.y + target.radius)):
           target.hit = True
           self.game.hitArray[0].append(target.x)
           self.game.hitArray[1].append(target.y)
           self.game.hitArray[2].append(cannonAngle)

class Cannon:
    xTop = 0
    yTop = 0

    def __init__(self, game):
        self.game = game

    def drawCannon(self, cannonDegrees):
        barrelX = 110
        barrelY = self.game.HEIGHT - 100

        # barrel surface
        bsurf = pg.Surface((40,100))
        bsurf.fill(self.game.RED)
        bsurf.set_colorkey(self.game.WHITE)

        barrelRect = pg.draw.rect(bsurf, self.game.RED, (0,0,40,100))

        rotatedSurf = pg.transform.rotate(bsurf, cannonDegrees)
        rotRect = rotatedSurf.get_rect()
        rotRect.center = (barrelX, barrelY)

        self.game.screen.blit(rotatedSurf, rotRect)

        # base
        pg.draw.rect(self.game.screen, self.game.BLUE, (10,self.game.HEIGHT-100,200,100))

        self.xTop = rotRect.center[0] + (20 * math.cos(math.radians(90 + cannonDegrees)))
        self.yTop = rotRect.center[1] - (20 * math.sin(math.radians(90 + cannonDegrees)))

class Target:
    hit = False

    def __init__(self, game):
        self.x = random.randint(150, 650)
        self.y = random.randint(150, 550)
        self.radius = 50
        self.hit = False
        self.game = game

    def show(self):
        pg.draw.circle(self.game.screen, self.game.RED, (self.x, self.y), self.radius,0)
