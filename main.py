############
# Author: Nathaniel Welch
# Version: 11/21/2022
# Description: Manages the GUI and execution of the algorithm
############

import pygame
from Algo import algorithm
from Node import Node

WIDTH = 800  # This value is the width of the window to display

# This creates a square window of size WIDTH that can be accessed from many different functions
WIN = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption("A* Path Finding")  # This sets the title of the window

# These tuples allow us to access colors by name
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


# This function creates a grid of squares based on the window size and number of rows
def make_grid(rows, width):
    grid = []
    dist = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, dist, rows)
            grid[i].append(node)

    return grid


# This function draws a grid of lines to the window to separate the squares
def draw_grid(win, rows, width):
    dist = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * dist), (width, i * dist))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * dist, 0), (j * dist, width))


# This function clears the window and draws the current grid to the window
def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


# This function calculates which square is hovered over when a click occurs
def get_clicked_posit(pos, rows, width):
    dist = width // rows
    y, x = pos

    row = y // dist
    col = x // dist

    return row, col


# Main uses the global window and other global variables to draw the inital grid and wait on user input
def main(win, width):
    ROWS = 50 # Default number of rows. Also the number of columns since its a square grid
    grid = make_grid(ROWS, width) # creates a list of nodes to represent the grid

    # Defaults the start and end for the pathfinding algorithm to None until the user chooses
    start = None
    end = None

    # Loop variable
    run = True

    # Used to control whether user input is allowed
    started = False

    # While we should continue the loop
    while run:
        # Draw the current grid to the window
        draw(win, grid, ROWS, width)
        # For every event the window receives
        for event in pygame.event.get():
            # If the event is to close the window. We exit the loop
            if event.type == pygame.QUIT:
                run = False

            # If the user clicks
            if pygame.mouse.get_pressed()[0]:
                # Get the current position of the mouse in the window
                pos = pygame.mouse.get_pos()
                # Use the position to determine what square should be affected
                row, col = get_clicked_posit(pos, ROWS, width)
                # Get the node representing that square
                node = grid[row][col]

                # If the start has not been selected, and the selected node is not the end
                if not start and node != end:
                    # make it the start node
                    start = node
                    start.make_start()
                # If the end has not been selected, and the selected node is not the start
                elif not end and node != start:
                    # make it the end node
                    end = node
                    end.make_end()
                # Else if we have selected the end and start, and the selected isnt one of them
                elif node != end and node != start:
                    # we set that node to blocked
                    node.make_blocked()
            # A right click clears the status of a square
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_posit(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            # If a key was pressed
            if event.type == pygame.KEYDOWN:
                # if the key was space and we have start and end, then create the graph and run the algorithm
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                # If the key was 'c', reset everything
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()


main(WIN, WIDTH)
