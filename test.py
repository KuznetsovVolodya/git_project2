import pygame
import os
import random
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtWidgets import QInputDialog

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Лабиринт')
    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)
    v = 120
    fps = 60


    def load_image(name):
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname)
        image = image.convert_alpha()
        colorkey = -1
        image.set_colorkey(colorkey)
        return image


    class Wall(pygame.sprite.Sprite):
        image = load_image("wall.png")

        def __init__(self, width, height, cell_size, left, top, size_x, size_y):
            super().__init__(all_sprites)
            self.image = Wall.image
            self.image = pygame.transform.scale(self.image, (size_x, size_y))
            self.rect = self.image.get_rect()
            self.rect.x = left + width * cell_size
            self.rect.y = top + height * cell_size
            self.mask = pygame.mask.from_surface(self.image)

        def update(self, coords):
            return self.rect.collidepoint(coords)


    class Wall_place():
        def __init__(self):
            self.x_place = self.load_level_x("walls_x")
            for i in range(len(self.x_place)):
                for j in range(len(self.x_place[i])):
                    if self.x_place[i][j] == "#":
                        a = board.zero_coords()
                        Wall(j, i, a[2], a[0], a[1], 3, a[2])
            self.y_place = self.load_level_y("walls_y")
            for i1 in range(len(self.y_place)):
                for j1 in range(len(self.y_place[i1])):
                    if self.y_place[i1][j1] == "#":
                        a1 = board.zero_coords()
                        Wall(j1, i1, a1[2], a1[0], a1[1], a1[2], 3)

        def load_level_y(self, filename):
            filename = "data/" + filename
            with open(filename, 'r') as mapFile:
                level_map = [line.strip() for line in mapFile]
            return list(map(lambda x: x.ljust(10, '.'), level_map))

        def load_level_x(self, filename):
            filename = "data/" + filename
            with open(filename, 'r') as mapFile:
                level_map = [line.strip() for line in mapFile]
            return list(map(lambda x: x.ljust(11, '#'), level_map))


    class Board:
        def __init__(self):
            self.width = 10
            self.height = 10
            self.board = [[0] * width for _ in range(height)]
            self.left = 10
            self.top = 10
            self.cell_size = 50
            self.mask = None

        def zero_coords(self):
            return self.left, self.top, self.cell_size, self.width, self.height

        def set_view(self, left, top, cell_size):
            self.left = left
            self.top = top
            self.cell_size = cell_size

        def render(self, screen):
            for i in range(self.width):
                for j in range(self.height):
                    x1 = self.left + self.cell_size * i
                    y1 = self.top + self.cell_size * j
                    pygame.draw.rect(screen, "grey", ((x1, y1), (self.cell_size, self.cell_size)), 2)

        def get_cell(self, mouse_pos, pressed_button):
            x_c, y_c = mouse_pos[0], mouse_pos[1]
            if pressed_button == "RIGHT":
                x_c += self.cell_size
            elif pressed_button == "LEFT":
                x_c -= self.cell_size
            elif pressed_button == "UP":
                y_c -= self.cell_size
            elif pressed_button == "DOWN":
                y_c += self.cell_size
            return x_c, y_c


    all_sprites = pygame.sprite.Group()
    board = Board()
    board.set_view(100, 100, 80)
    running = True
    Wall_place()
    print(all_sprites.update((100, 100)))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.draw(screen)
        pygame.draw.circle(screen, 'yellow', (520, 821), 1)

        pygame.display.flip()

pygame.quit()
