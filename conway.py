"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

ON = 255
OFF = 0
vals = [ON, OFF]
height=0
lenght = 0

def readCSV(name):
    df = pd.read_csv(name)
    grid = df.to_numpy()
    global lenght
    lenght = len(grid)
    global height
    height = len(grid[0])

    return grid
def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N * N, p=[0, 1]).reshape(N, N)


def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 255, 255]])
    grid[i:i + 3, j:j + 3] = glider
def addSpaceShip(i,j,grid):
    grid[3+i][1+j] = 255
    grid[3+i][2+j] = 255
    grid[3+i][3+j] = 255
    grid[2+i][3+j] = 255
    grid[1+i][2+j] = 255

    grid[0+i][0+j] = 255
    grid[2+i][0+j] = 255

    grid[3+i][1+j] = 255
    grid[3+i][2+j] = 255
    grid[3+i][3+j] = 255
    grid[3+i][4+j] = 255

    grid[0+i][3+j] = 255

    grid[1+i][4+j] = 255
    grid[2+i][4+j] = 255


def countBorders(x, y, grid, N):
    counter = 0
    # Check left
    #print('Lenght: ', lenght, 'Height: ', height)
    if x - 1 >= 0:
        if grid[x - 1][y] == 255:
            counter += 1
    if x - 1 >= 0 and y + 1 < height:
        if grid[x - 1][y + 1] == 255:
            counter += 1
    if x - 1 >= 0 and y - 1 >= 0:
        if grid[x - 1][y - 1] == 255:
            counter += 1
    # check right
    if x + 1 < lenght:
        if grid[x + 1][y] == 255:
            counter += 1
    if x + 1 < lenght and y + 1 < height:
        if grid[x + 1][y + 1] == 255:
            counter += 1
    if x + 1 < lenght and y - 1 >= 0:
        if grid[x + 1][y - 1] == 255:
            counter += 1
    # check up
    if y + 1 < height:
        if grid[x][y + 1] == 255:
            counter += 1
    # Check down
    if y - 1 >= 0:
        if grid[x][y - 1] == 255:
            counter += 1

    return counter


def update(frameNum, img, grid, N):

    # copy grid since we require 8 neighbors for calculation
    # and we go line by line 
    newGrid = grid.copy()

    # TODO: Implement the rules of Conway's Game of Life
    for x, i in enumerate(grid):
        for y, j in enumerate(grid[x]):
            count = countBorders(x, y, grid, N)
            if count == 2 or count == 3:
                if grid[x][y] == 255:
                    newGrid[x][y] = 255
            if count == 3 and grid[x][y] == 0:
                newGrid[x][y] = 255
            if count < 2 or count > 3:
                newGrid[x][y] = 0

    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,


# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life system.py.")
    # TODO: add arguments

    # set grid size
    N = 100

    # set animation update interval
    updateInterval = 10

    # declare grid
    grid = np.array([])
    # populate grid with random on/off - more off than on
    grid = randomGrid(N)
    # Uncomment lines to see the "glider" demo
    grid = np.zeros(N * N).reshape(N, N)
    addGlider(8, 5, grid)
    addSpaceShip(7,7,grid)
    addGlider(20, 5, grid)
    addSpaceShip(50, 40, grid)
    file = input('Write the name of the file you want to run \n')
    grid = readCSV(file)
    #   Y  X

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N,),
                                  frames=10,
                                  interval=updateInterval,
                                  save_count=50)

    plt.show()


# call main
if __name__ == '__main__':
    main()
