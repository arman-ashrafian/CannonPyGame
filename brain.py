# BRAIN
# draw plane of best fit through hitArray data points

import numpy as np
import scipy.linalg
import math

class Brain:

    def __init__(self, game):
        self.game = game

    # Distance Function
    # -- returns euclidiean distance between two points p1 and p2
    def getDist(self, p1, p2):
        return math.sqrt((p1[0]-p2[0])**2 -
                         (p1[1]-p2[1])**2 -
                         (p1[2]-p2[2])**2)

    # Minimum Distance
    # -- returns angle of nearest neighbor
    def getAngle(self, target):
        dist = 10000 # -- some big number
        angle = 0
        point = [target.x, target.y, 0]
        print(point)
        print(self.game.hitArray)
        for existing_point in self.game.hitArray:
            tempDist = self.getDist(existing_point, point)
            if tempDist < dist:
                dist = tempDist
                angle = existing_point[2]
        return angle
