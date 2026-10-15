from node import Node
from queue import PriorityQueue

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

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos
    row = y // gap
    col = x // gap
    if row >= rows:
        row = rows - 1
    if col >= rows:
        col = rows - 1    
    return row,col

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)   
                    
            if pygame.mouse.get_pressed()[0]:  # Left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]

            # 1st click: Set Start node (if not already set and not the end node)
                if not start and node != end:
                    start = node
                    start.make_start()

            # 2nd click: Set End node (if not already set and not the start node)
                elif not end and node != start:
                    end = node
                    end.make_end()

            # Any other click: Draw barriers (walls), as long as it's not start or end
                elif node != end and node != start:
                    node.make_barrier()

        # Check if the right mouse button is pressed down (erasing nodes)
            elif pygame.mouse.get_pressed()[2]:  # Right click
               pos = pygame.mouse.get_pos()
               row, col = get_clicked_pos(pos, ROWS, width)
               node = grid[row][col]
               node.reset()  # Clears the node back to white
            
               if node == start:
                    start = None
               elif node == end:
                    end = None         
    pygame.quit()

main(WIN, 800)