import pygame as pg
import sys
import math

pg.init()

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
LGREY = (150,150,150)


WIDTH = 800
HEIGHT = 800
CENTERX = int(WIDTH/2)
CENTERY = int(HEIGHT/2)

size = (WIDTH, HEIGHT)
screen = pg.display.set_mode(size)
pg.display.set_caption("Boom Pow")

# Set up
clock = pg.time.Clock()
fps = 65
done = False

fontObj = pg.font.SysFont('monospace', 32, bold=True)
fontObj2 = pg.font.SysFont('monospace', 18, bold=True)

class Ball:

    speedY = 0

    def __init__(self, angleShot, speed, color, pos):
        self.angleShot = angleShot
        self.speed = speed
        self.speedY = speed
        self.color = color
        self.x = pos[0]
        self.y = pos[1]


    def updateBall(self):
        vx0 = self.speed * math.cos(math.radians(90 + self.angleShot))
        vy0 = self.speedY * math.sin(math.radians(90 + self.angleShot))

        self.x = int(self.x + vx0)
        self.y = int(self.y - vy0)

        self.speedY += -.3

        pg.draw.circle(screen, self.color, (self.x, self.y), 20,0)

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




def gameIntro():
    global screen

    buttonPressed = False
    screen.fill(LGREY)

    introText = "Shoot Some Shit Up"
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
    global done

    cannonAngle = 0
    cannonAngleChange = 0
    ballsShot = []

    cannon = Cannon()

    #----Main Loop----#
    while not done:
        # clear screen
        screen.fill(WHITE)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    cannonAngleChange = -2
                if event.key == pg.K_LEFT:
                    cannonAngleChange = 2
                if event.key == pg.K_SPACE:
                    newBall = Ball(cannonAngle, 18, BLUE, (cannon.xTop, cannon.yTop))
                    ballsShot.append(newBall)
            if event.type == pg.KEYUP:
                cannonAngleChange = 0


        # --- Game Logic
        if(cannonAngle + cannonAngleChange <= 70 and
           cannonAngle + cannonAngleChange >= -70):
           cannonAngle += cannonAngleChange


        # --- Drawing
        cannon.drawCannon(cannonAngle)


        for b in ballsShot:
            if(b.x > WIDTH or b.x < 0 or b.y < 0 or b.y > HEIGHT):
                del b
            else:
                b.updateBall()

        # --- update screen
        pg.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    gameIntro()
    gameLoop()
