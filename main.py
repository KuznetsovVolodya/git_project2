import pygame
import os

# x2 = (mouse_pos[0] - self.left) // self.cell_size
# y2 = (mouse_pos[1] - self.top) // self.cell_size
# return {x2}, {y2}

# def bump(self, image):
#     # if pygame.sprite.collide_mask(self.mask, image):
#         print(True)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Лабиринт')
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    v = 120
    fps = 60


    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname)
        image = image.convert_alpha()
        colorkey = -1
        image.set_colorkey(colorkey)
        return image


    class Wall(pygame.sprite.Sprite):
        image = load_image("lab3.png")

        def __init__(self, width, height, cell_size, left, top):
            super().__init__(all_sprites)
            self.image = Wall.image
            self.image = pygame.transform.scale(self.image, (width * cell_size + 5, height * cell_size + 5))
            self.rect = self.image.get_rect()
            self.rect.x = left - 5
            self.rect.y = top - 5
            self.mask = pygame.mask.from_surface(self.image)


    class Hero(pygame.sprite.Sprite):
        image = load_image("hero.png")

        def __init__(self, x_coord, y_coord, size):
            super().__init__(all_sprites_2)
            self.x_coord, self.y_coord, self.size = x_coord, y_coord, size
            self.image = Hero.image
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.rect = self.image.get_rect()
            self.rect.x = self.x_coord
            self.rect.y = self.y_coord
            self.back_x = self.x_coord
            self.back_y = self.y_coord
            self.x_coord_to = self.x_coord
            self.y_coord_to = self.y_coord
            self.mask = pygame.mask.from_surface(self.image)

        def aim(self, x, y):
            self.x_coord_to = x
            self.y_coord_to = y

        def stop(self):
            if (self.x_coord_to, self.y_coord_to) == (self.x_coord, self.y_coord):
                return True
            else:
                return False

        def update(self):
            if pygame.sprite.collide_mask(self, wall) and not (
                    120 <= self.x_coord <= 210 and 130 <= self.y_coord <= 150):
                self.x_coord_to = self.back_x
                self.y_coord_to = self.back_y
                self.back_x = self.x_coord
                self.back_y = self.y_coord

        def movement(self):
            if not self.stop():
                if self.x_coord_to != self.x_coord:
                    self.x_coord += ((self.x_coord_to - self.x_coord) / abs(self.x_coord_to - self.x_coord)) * v / fps
                if self.y_coord_to != self.y_coord:
                    self.y_coord += ((self.y_coord_to - self.y_coord) / abs(self.y_coord_to - self.y_coord)) * v / fps
            else:
                self.back_x = self.x_coord
                self.back_y = self.y_coord
            self.rect.x = self.x_coord
            self.rect.y = self.y_coord

        def get_coords(self):
            return self.x_coord, self.y_coord


    class Board:
        def __init__(self):
            self.width = 10
            self.height = 5
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
                    pygame.draw.rect(screen, "black", ((x1, y1), (self.cell_size, self.cell_size)), 1)

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
    all_sprites_2 = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    board = Board()
    board.set_view(100, 100, 80)
    b = board.zero_coords()
    wall = Wall(b[3], b[4], b[2], b[0], b[1])
    x_coord, y_coord, size = board.zero_coords()[0] + 30, board.zero_coords()[1] + 30, board.zero_coords()[2] - 60
    hero = Hero(x_coord, y_coord, size)
    running = True
    clock = pygame.time.Clock()
    direction = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if hero.stop():
                    if pygame.key.get_pressed()[pygame.K_RIGHT]:
                        direction = "RIGHT"
                    elif pygame.key.get_pressed()[pygame.K_LEFT]:
                        direction = "LEFT"
                    elif pygame.key.get_pressed()[pygame.K_UP]:
                        direction = "UP"
                    elif pygame.key.get_pressed()[pygame.K_DOWN]:
                        direction = "DOWN"
                    x_coord, y_coord = hero.get_coords()[0], hero.get_coords()[1]
                    x_coord2, y_coord2 = board.get_cell((x_coord, y_coord), direction)
                    hero.aim(x_coord2, y_coord2)
        screen.fill("white")
        hero.movement()
        all_sprites.draw(screen)
        board.render(screen)
        all_sprites_2.draw(screen)
        hero.update()
        clock.tick(fps)
        pygame.display.flip()
pygame.quit()
