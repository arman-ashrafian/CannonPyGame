# BRAIN
# draw plane of best fit through hitArray data points

import numpy as np
import scipy.linalg

class Brain:

    def __init__(self, game):
        self.game = game
        self.data = np.c_[game.hitArray[0],game.hitArray[1],game.hitArray[2]]

        # best-fit linear plane
        A = np.c_[self.data[:,0], self.data[:,1], np.ones(self.data.shape[0])]
        self.C,_,_,_ = scipy.linalg.lstsq(A, self.data[:,2])    # coefficients


    def getAngle(self):
        angleGuess = self.C[0]*321 + self.C[1]*387 + self.C[2]
        return int(angleGuess)
