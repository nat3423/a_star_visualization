############
# Author: Nathaniel Welch
# Version: 11/18/2022
# Description: Houses the functions needed to apply the a* algorithm
############
from queue import PriorityQueue

import pygame


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0  # We keep track of the count of nodes added to break ties by whichever was considered first
    open_set = PriorityQueue()  # This is where we pull the next possible node for our path from
    open_set.put((0, count, start))  # Add the start node to the open set
    came_from = {}  # Keeps track of how we got to a Node
    g_score = {node: float("inf") for row in grid for node in row}  # tracks shortest distance from start to current
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}  # tracks ~ distance from current to end
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}  # tracks what is in the priority queue

    while not open_set.empty():
        # This allows us to break the loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]  # gets node from queue
        open_set_hash.remove(current)  # removes from hash since we take from queue

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False
