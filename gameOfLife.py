import random
import sys
import time
import numpy as np
import pygame

pygame.init()


def setup(x, y):
    # x = columns, y = rows
    grid = np.zeros((x, y))  # create empty x by y array
    for i in range(0, x):  # for each column
        for j in range(0, y):  # for each row/cell
            grid[i][j] = random.randint(0, 1)  # 0 = dead cell, 1 = live cell
            # randomly populating the scene at the start
    return grid


def draw_scene(window, grid, block):
    white = (255, 255, 255)  # set the colours for the scene
    black = (0, 0, 0)
    window.fill(white)  # set background to white
    for i in range(0, grid.shape[0]):
        for j in range(0, grid.shape[1]):
            if grid[i][j] == 1:
                # draw a 15 by 15 black rectangle for every live cell
                pygame.draw.rect(window, black, [i * block, j * block, block, block], 0)


def new_value_calculator(val, neighbours):  # calculates next generation grid
    if val == 1:  # live cell
        if neighbours < 2 or neighbours > 3:  # underpopulation and overcrowding
            next_value = 0
        else:  # survival
            next_value = 1
    else:  # dead cell
        if neighbours == 3:  # creation of life
            next_value = 1
        else:  # no interactions
            next_value = 0
    return next_value


def update_scene(grid):
    # x = columns, y = rows
    x, y = grid.shape
    new_grid = np.zeros((x, y))
    for i in range(0, x):
        # Edges of the scene are stitched together
        # This toroidal array is a strategy to simulate an infinite space
        # computers have finite memory - cannot simulate an infinite space
        if i == 0:  # if at the left-most edge of the scene
            i_minus_1 = x - 1  # right-most edge column
        else:
            i_minus_1 = i - 1
        if i == x - 1:  # at the right-most edge
            i_plus_1 = 0  # left-most column
        else:
            i_plus_1 = i + 1
        for j in range(0, y):
            if j == 0:  # if on the top row of the scene
                j_minus_1 = y - 1  # bottom row of the scene
            else:
                j_minus_1 = j - 1
            if j == y - 1:  # if on the bottom row
                j_plus_1 = 0  # top row of the scene
            else:
                j_plus_1 = j + 1
            # finds number of live neighbours
            neighbours = grid[i_minus_1][j_minus_1] + grid[i_minus_1][j] + grid[i_minus_1][j_plus_1] + \
                grid[i][j_minus_1] + grid[i][j_plus_1] + \
                grid[i_plus_1][j_minus_1] + grid[i_plus_1][j] + grid[i_plus_1][j_plus_1]
            new_grid[i][j] = new_value_calculator(grid[i][j], neighbours)
    return new_grid


def start(grid):
    block_size = 10  # size of cells
    size = [grid.shape[0] * block_size, grid.shape[1] * block_size]  # window size
    window = pygame.display.set_mode(size)
    done = False
    draw_scene(window, grid, block_size)
    while not done:
        time.sleep(0.2)  # delay between generations
        draw_scene(window, grid, block_size)
        pygame.display.update()
        grid = update_scene(grid)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


scene = setup(100, 50)
start(scene)
