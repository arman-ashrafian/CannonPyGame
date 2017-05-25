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
fps = 60
done = False

fontObj = pg.font.SysFont('monospace', 32, bold=True)
fontObj2 = pg.font.SysFont('monospace', 18, bold=True)

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

def drawCannon(cannonDegrees):
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

    pg.draw.rect(screen, BLUE, (10,HEIGHT-100,200,100))


def gameLoop():
    global done
    #----Main Loop----#
    cannonAngle = 0
    cannonAngleChange = 0
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    cannonAngleChange = -2
                if event.key == pg.K_LEFT:
                    cannonAngleChange = 2
            if event.type == pg.KEYUP:
                cannonAngleChange = 0


        # --- Game Logic
        if(cannonAngle + cannonAngleChange <= 70 and
           cannonAngle + cannonAngleChange >= -70):
           cannonAngle += cannonAngleChange


        screen.fill(WHITE)
        # --- Drawing
        drawCannon(cannonAngle)

        pg.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    gameIntro()
    gameLoop()
