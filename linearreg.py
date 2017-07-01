import numpy as np
import scipy.linalg
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt

x = [321, 428, 490, 296, 578, 640, 543, 264, 512, 428, 374, 613, 610, 545, 319, 241, 488, 559, 516, 593, 643, 231, 310, 411, 547, 342, 195, 162, 320, 420, 298, 409, 253, 348, 215, 454, 303, 221, 610, 259, 253, 359, 543, 450, 481, 357, 199, 202, 541, 324, 304, 631, 443]
y = [387, 205, 285, 244, 341, 245, 426, 244, 150, 401, 327, 529, 162, 291, 369, 269, 160, 524, 464, 358, 156, 549, 169, 501, 278, 404, 238, 240, 178, 495, 258, 540, 335, 393, 194, 293, 268, 513, 279, 199, 468, 320, 299, 509, 220, 505, 451, 315, 498, 294, 357, 537, 415]
z = [-28, -20, -35, -15, -46, -43, -47, -14, -28, -44, -28, -67, -25, -35, -24, -12, -26, -63, -55, -45, -24, -34, -17, -56, -39, -29, -11, -7, -20, -48, -13, -64, -20, -39, -5, -40, -24, -24, -41, -13, -25, -34, -42, -52, -27, -48, -17, -12, -62, -26, -26, -69, -45]

data = np.c_[x,y,z]

# regular grid covering the domain of the data
# mn = np.min(data, axis=0)
# mx = np.max(data, axis=0)
# X,Y = np.meshgrid(np.linspace(mn[0], mx[0], 20), np.linspace(mn[1], mx[1], 20))

# best-fit linear plane
A = np.c_[data[:,0], data[:,1], np.ones(data.shape[0])]
C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])    # coefficients

# evaluate it on grid
# Z = C[0]*X + C[1]*Y + C[2]


def getAngle():
    angleGuess = C[0]*321 + C[1]*387 + C[2]




# plot points and fitted surface
# fig = plt.figure()
# ax = fig.gca(projection='3d')
# ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=1)
# ax.scatter(data[:, 0], data[:, 1], data[:, 2], c='r', s=50)
# plt.xlabel('X')
# plt.ylabel('Y')
# ax.set_zlabel('Z')
# ax.axis('equal')
# ax.axis('tight')
# plt.show()
