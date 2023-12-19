import pygame
import os


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 50

    def zero_coords(self):
        return self.left, self.top, self.cell_size

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                x1 = self.left + self.cell_size * i
                y1 = self.top + self.cell_size * j
                pygame.draw.rect(screen, "white", ((x1, y1), (self.cell_size, self.cell_size)), 1)

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
        if self.left <= x_c < (self.left + self.width * self.cell_size) and \
                self.top <= y_c < (self.top + self.height * self.cell_size):
            return x_c, y_c
        else:
            return mouse_pos
            # x2 = (mouse_pos[0] - self.left) // self.cell_size
            # y2 = (mouse_pos[1] - self.top) // self.cell_size
            # return {x2}, {y2}


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Лабиринт')
    size = width, height = 600, 600
    screen = pygame.display.set_mode(size)
    board = Board(5, 5)
    board.set_view(100, 100, 80)
    running = True
    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    image = load_image("hero.png")
    x_coord, y_coord, size = board.zero_coords()[0], board.zero_coords()[1], board.zero_coords()[2]
    sprite.image = pygame.transform.scale(image, (board.zero_coords()[2], board.zero_coords()[2]))
    sprite.rect = sprite.image.get_rect()
    all_sprites.add(sprite)

    direction = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    direction = "RIGHT"
                elif pygame.key.get_pressed()[pygame.K_LEFT]:
                    direction = "LEFT"
                elif pygame.key.get_pressed()[pygame.K_UP]:
                    direction = "UP"
                elif pygame.key.get_pressed()[pygame.K_DOWN]:
                    direction = "DOWN"
                x_coord, y_coord = board.get_cell((x_coord, y_coord), direction)
        screen.fill((0, 0, 0))
        board.render(screen)
        sprite.rect.x = x_coord
        sprite.rect.y = y_coord
        all_sprites.draw(screen)
        pygame.display.flip()
pygame.quit()