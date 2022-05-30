from Velocity import Velocity
from Cube import Cube
from Type import Type
from random import random


n = 5
grid = [[None] * n for _ in range(n)]
for l in range(n):
    print(grid[l])
wall_velocity = Velocity(0, 0, 0, 0, 0, 0)

air_velocity = Velocity(2, 5, 2, 5, 0, 0)
pollution_rate = 0.2


def add_neighbors(cube):
    r = (-1, 1)
    for k in r:
        if 0 <= cube.coordinates[0] + k < n:
            cube.add_neighbor(grid[cube.coordinates[0] + k][cube.coordinates[1]], (k, 0, 0))
    for k in r:
        if 0 <= cube.coordinates[1] + k < n:
            cube.add_neighbor(grid[cube.coordinates[0]][cube.coordinates[1] + k], (0, k, 0))


for i in range(n):
    for j in range(n):
        if i == n - 1 or j == n - 1 or i == 0 or j == 0:
            grid[i][j] = Cube(Type.WALL, (i, j, 0), (2, 2, 0), 0, wall_velocity, 0)
        else:
            grid[i][j] = Cube(Type.AIR, (i, j, 0), (2, 2, 0), random(), air_velocity, 0)
        # add_neighbors(grid[i][j])

for i in range(n):
    for j in range(n):
        add_neighbors(grid[i][j])

# for i in range(n):
#     for j in range(n):
#         print(f"neighbors of cube {(i, j)}")
#         for (neigh, coord) in grid[i][j].neighbors.items():
#             print(neigh.type, coord)
#         print('\n')
#     print('\n')

for i in range(n):
    for j in range(n):
        print(grid[i][j].pollution_rate, end=' ')
    print('\n')

for q in range(10):
    for i in range(n):
        for j in range(n):
            grid[i][j].move()

for i in range(n):
    for j in range(n):
        print(grid[i][j].pollution_rate, end=' ')
    print('\n')