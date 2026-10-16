from node import Node
from queue import PriorityQueue

def make_grid(rows, total_width, total_height):
    grid = []
    gap = total_height // rows
    cols = total_width // gap

    for i in range(rows):
        grid.append([])
        for j in range(cols):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid
import pygame
import sys
pygame.init()
pygame.mixer.init()
WIN = pygame.display.set_mode((1600, 950))
pygame.display.set_caption("Pathfinding Algorithm Visualizer by Aaliyan Hussain")
def draw(win, grid, rows, total_width, reset_btn_img):
    WIN.fill((22, 24, 29))

    for row in grid:
        for node in row:
            node.draw(win)
    win.blit(reset_btn_img, (1500, 20))

    pygame.display.update()

def get_clicked_pos(pos, rows, total_width, total_height):
    gap = total_height // rows
    x, y = pos
    row = y // gap
    col = x // gap

    max_rows = rows
    max_cols = total_width // gap

    row = max(0, min(row, max_rows - 1))
    col = max(0, min(col, max_cols - 1))
    return row, col

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
    step = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

        step += 1
        if step % 5 == 0:
            draw()

        if current != start:
            current.make_closed()

    return False

def main(win, total_width):
    ROWS = 50
    total_height = 950
    grid = make_grid(ROWS, 1600, 950)
    start = grid[5][7]
    start.make_start()

    cols = len(grid[0])
    end = grid[ROWS - 6][cols - 6]
    end.make_end()
    

    reset_btn_img = pygame.image.load('reset_btn.png').convert_alpha()
    reset_btn_img = pygame.transform.scale(reset_btn_img, (70, 70))
    btn_rect = pygame.Rect(1500, 20, 70, 70)

    is_drawing = False

    run = True
    
    while run:
        draw(win, grid, ROWS, total_width, reset_btn_img)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, total_width, reset_btn_img), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, 1600, 950)   
                    
            if pygame.mouse.get_pressed()[0]:  # Left click
                pos = pygame.mouse.get_pos()

                if btn_rect.collidepoint(pos):
                    grid = make_grid(ROWS, 1600, total_height)
                    start = grid[5][7]
                    start.make_start()
                    end = grid[ROWS - 6][len(grid[0]) - 6]
                    end.make_end()
                elif pos[0] < total_width:
                    row, col = get_clicked_pos(pos, ROWS, 1600, total_height)
                    node = grid[row][col]
                    if node != end and node != start and not node.is_barrier():
                        node.make_barrier()
       
            elif pygame.mouse.get_pressed()[2]:  # Right click
               pos = pygame.mouse.get_pos()
               if pos[0] < total_width:
                   row, col = get_clicked_pos(pos, ROWS, 1600, 950)
                   node = grid[row][col]
                   node.reset()  # Clears the node back to white
            
                   if node == start:
                       start = None
                   elif node == end:
                       end = None         
    pygame.quit()

main(WIN, 1600)