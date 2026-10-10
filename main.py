from node import Node

def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid
import pygame
import sys
pygame.init()
WIN = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Pathfinding Algorithm Visualizer by Aaliyan Hussain")
def draw(win, grid, rows, width):
    WIN.fill((255, 255, 255))

    for row in grid:
        for node in row:
            node.draw(win)

    pygame.display.update()

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None 

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              run = False
    pygame.quit()

main(WIN, 800)