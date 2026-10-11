class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.color = (255, 255, 255)
        self.rect_width = width
        self.total_rows = total_rows

        self.g_cost = float("inf")
        self.h_cost = float("inf")
        self.f_cost =float("inf")
        self.neighbours = []
        self.from_node = None


    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == (255, 0, 0)

    def is_open(self):
        return self.color == (0, 255, 0)

    def is_barrier(self):
        return self.color == (0, 0, 0)

    def is_start(self):
        return self.color == (255, 165, 0)

    def is_end(self):
        return self.color == (128, 0, 128)


    def make_closed(self):
        self.color = (255, 0, 0)

    def make_open(self):
        self.color = (0, 255, 0)

    def make_barrier(self):
        self.color = (0, 0, 0)

    def make_start(self):
        self.color = (255, 165, 0)

    def make_end(self):
        self.color = (128, 0, 128)

    def make_path(self):
        self.color = (0, 0, 255)  # Blue: Final computed path

    def reset(self):
        self.color = (255, 255, 255)

    def draw(self, win):
        import pygame
        pygame.draw.rect(win, self.color, (self.x, self.y, self.rect_width, self.rect_width))

    def update_neighbors(self, grid):
        self.neighbors = []
        
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        # UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])