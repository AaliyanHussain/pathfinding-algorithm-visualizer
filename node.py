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