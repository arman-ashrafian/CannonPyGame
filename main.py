from game import runGame, hitArray
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

runGame()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_zlabel('Angle')

print(hitArray[0])
print(hitArray[1])
print(hitArray[2])
ax.scatter(hitArray[0], hitArray[1], hitArray[2], c='r', marker='o')
plt.show()
