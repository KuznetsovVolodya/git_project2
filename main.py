import pygame
import os
from random import choice
from random import shuffle
import sys

# from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
# from PyQt5.QtWidgets import QInputDialog

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Лабиринт')
    size = width, height = (1000, 1000)
    screen = pygame.display.set_mode(size)
    v = 240
    fps = 60


    def load_image(name):
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname)
        image = image.convert_alpha()
        colorkey = -1
        image.set_colorkey(colorkey)
        return image


    def terminate():
        pygame.quit()
        sys.exit()


    def hello():
        all_sprites_0 = pygame.sprite.Group()
        all_sprites_0_1 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()

        class Play(pygame.sprite.Sprite):
            image = load_image("play.png")

            def __init__(self, left, top, size_x, size_y):
                super().__init__(all_sprites_0_1)
                self.image = Play.image
                self.image = pygame.transform.scale(self.image, (size_x, size_y))
                self.rect = self.image.get_rect()
                self.size_x = size_x
                self.size_y = size_y
                self.rect.x = left
                self.rect.y = top

            def update(self, pos):
                if self.rect.x <= pos[0] <= self.rect.x + self.size_x and \
                        self.rect.y <= pos[1] <= self.rect.y + self.size_y:
                    return True
                return False

        class Phone_image(pygame.sprite.Sprite):
            image = load_image("min_phone.png")

            def __init__(self, left, top, size_x, size_y):
                super().__init__(all_sprites_0)
                self.image = Phone_image.image
                self.image = pygame.transform.scale(self.image, (size_x, size_y))
                self.rect = self.image.get_rect()
                self.rect.x = left
                self.rect.y = top

        intro_text = ["'become a legend' представляет", "",
                      "      ЛАБИРИНТ МИНОТАВРА", "",
                      "         Компьютерная игра",
                      "по мотивам знаменитого мифа"]

        fon = pygame.transform.scale(load_image('phone.png'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 50)
        text_coord = 50
        min_im = Phone_image(100, 400, 800, 500)
        min_im = Play(850, 950, 150, 50)
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('orange'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 240
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for elem in all_sprites_0_1:
                        if elem.update(event.pos):
                            first_game()

                all_sprites_0.draw(screen)
                all_sprites_0_1.draw(screen)
            pygame.display.flip()
            # clock.tick(FPS)


    def min_win():
        all_sprites_0 = pygame.sprite.Group()
        all_sprites_0_1 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        FPS = 5

        class Play(pygame.sprite.Sprite):
            image = load_image("play.png")

            def __init__(self, left, top, size_x, size_y):
                super().__init__(all_sprites_0_1)
                self.image = Play.image
                self.image = pygame.transform.scale(self.image, (size_x, size_y))
                self.rect = self.image.get_rect()
                self.size_x = size_x
                self.size_y = size_y
                self.rect.x = left
                self.rect.y = top

            def update(self, pos):
                if self.rect.x <= pos[0] <= self.rect.x + self.size_x and \
                        self.rect.y <= pos[1] <= self.rect.y + self.size_y:
                    return True
                return False

        class Phone_image(pygame.sprite.Sprite):
            image = load_image("min_win.png")

            def __init__(self, left, top, size_x, size_y):
                super().__init__(all_sprites_0)
                self.image = Phone_image.image
                self.image = pygame.transform.scale(self.image, (size_x, size_y))
                self.rect = self.image.get_rect()
                self.rect.x = left
                self.rect.y = top

        intro_text = ["", "        МИНОТАВР ПОБЕДИЛ", ""]

        fon = pygame.transform.scale(load_image('phone_lose.png'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 50)
        text_coord = 50
        min_im = Phone_image(100, 200, 800, 700)
        min_im = Play(850, 950, 150, 50)
        clock = pygame.time.Clock()
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('grey'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 240
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for elem in all_sprites_0_1:
                        if elem.update(event.pos):
                            first_game()

            all_sprites_0.draw(screen)
            all_sprites_0_1.draw(screen)
            clock.tick(FPS)
            pygame.display.flip()


    def hero_win():
        all_sprites_0 = pygame.sprite.Group()
        all_sprites_0_1 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        FPS = 5

        class Play(pygame.sprite.Sprite):
            image = load_image("play.png")

            def __init__(self, left, top, size_x, size_y):
                super().__init__(all_sprites_0_1)
                self.image = Play.image
                self.image = pygame.transform.scale(self.image, (size_x, size_y))
                self.rect = self.image.get_rect()
                self.size_x = size_x
                self.size_y = size_y
                self.rect.x = left
                self.rect.y = top

            def update(self, pos):
                if self.rect.x <= pos[0] <= self.rect.x + self.size_x and \
                        self.rect.y <= pos[1] <= self.rect.y + self.size_y:
                    return True
                return False

        class Phone_image(pygame.sprite.Sprite):
            image = load_image("hero_win.png")

            def __init__(self, left, top, size_x, size_y):
                super().__init__(all_sprites_0)
                self.image = Phone_image.image
                self.image = pygame.transform.scale(self.image, (size_x, size_y))
                self.rect = self.image.get_rect()
                self.rect.x = left
                self.rect.y = top

        intro_text = ["", "        ВЫ ПОБЕДИЛИ", ""]

        fon = pygame.transform.scale(load_image('phone_win.png'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 50)
        text_coord = 50
        min_im = Phone_image(100, 200, 800, 700)
        min_im = Play(850, 950, 150, 50)
        clock = pygame.time.Clock()
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('grey'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 240
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for elem in all_sprites_0_1:
                        if elem.update(event.pos):
                            first_game()

            all_sprites_0.draw(screen)
            all_sprites_0_1.draw(screen)
            clock.tick(FPS)
            pygame.display.flip()


    def first_game():
        class Wall(pygame.sprite.Sprite):
            image = load_image("wall.png")

            def __init__(self, width, height, cell_size, left, top, size_x, size_y):
                super().__init__(all_sprites)
                self.image = Wall.image
                self.image = pygame.transform.scale(self.image, (size_x, size_y))
                self.rect = self.image.get_rect()
                self.rect.x = left + width * cell_size - 1
                self.rect.y = top + height * cell_size - 1
                self.mask = pygame.mask.from_surface(self.image)

            def update(self, coords):
                if self.rect.collidepoint(coords):
                    return True
                else:
                    return False

        class Floor(pygame.sprite.Sprite):
            image = load_image("floor.png")

            def __init__(self, width, height, cell_size, left, top):
                super().__init__(all_sprites_4)
                self.image = Floor.image
                self.image = pygame.transform.scale(self.image, (width * cell_size, height * cell_size))
                self.rect = self.image.get_rect()
                self.rect.x = left
                self.rect.y = top

        class Wall_place():
            def __init__(self):
                self.x_place = self.load_level_x("walls_x")
                for i in range(len(self.x_place)):
                    for j in range(len(self.x_place[i])):
                        if self.x_place[i][j] == "#":
                            a = board.zero_coords()
                            Wall(j, i, a[2], a[0], a[1], 5, a[2] + 2)
                self.y_place = self.load_level_y("walls_y")
                for i1 in range(len(self.y_place)):
                    for j1 in range(len(self.y_place[i1])):
                        if self.y_place[i1][j1] == "#":
                            a1 = board.zero_coords()
                            Wall(j1, i1, a1[2], a1[0], a1[1], a1[2] + 2, 5)

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

        class Quest(pygame.sprite.Sprite):
            image = load_image("quest.png")
            image2 = load_image("quest_ans.png")

            def __init__(self, width, height, cell_size, left, top, size_x, size_y):
                super().__init__(all_sprites_5)
                self.b = top + height * cell_size
                self.a = left + width * cell_size
                if f'{self.a}{self.b}' not in ans:
                    ans[f'{self.a}{self.b}'] = None
                if ans[f'{self.a}{self.b}'] is None:
                    self.image = Quest.image
                else:
                    self.image = Quest.image2
                self.x = size_x
                self.y = size_y
                self.image = pygame.transform.scale(self.image, (self.x, self.y))
                self.rect = self.image.get_rect()
                self.rect.x = self.a
                self.rect.y = self.b
                self.mask = pygame.mask.from_surface(self.image)

            def update(self, coords):
                if self.rect.collidepoint(coords):
                    ans[f'{self.a}{self.b}'] = True
                    self.image = Quest.image2
                    self.image = pygame.transform.scale(self.image, (self.x, self.y))
                    self.rect = self.image.get_rect()
                    self.rect.x = self.a
                    self.rect.y = self.b
                    self.mask = pygame.mask.from_surface(self.image)


        class Quest_place():
            def __init__(self):
                b = []
                for k in range(1, 100):
                    b.append(k)
                shuffle(b)
                b = b[:50]
                for i in range(50):
                    a = board.zero_coords()
                    j1 = b[i] // 10
                    i1 = b[i] % 10
                    Quest(j1, i1, a[2], a[0], a[1], a[2], a[2])


        #

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
                self.orig_x = self.x_coord
                self.orig_y = self.y_coord
                self.x_coord_to = self.x_coord
                self.y_coord_to = self.y_coord
                self.mask = pygame.mask.from_surface(self.image)

            def aim(self, x, y):
                self.x_coord_to = x
                self.y_coord_to = y
                self.orig_x, self.orig_y = self.x_coord, self.y_coord

            def stop(self):
                if (self.x_coord_to, self.y_coord_to) == (self.x_coord, self.y_coord):
                    return True
                else:
                    return False

            def next(self):
                if self.stop() and (self.orig_x, self.orig_y) != (self.x_coord, self.y_coord):
                    self.orig_x, self.orig_y = self.x_coord, self.y_coord
                    return 1
                else:
                    return 0

            def update(self):
                for elem in all_sprites:
                    if pygame.sprite.collide_mask(self, elem) or self.y_coord < board.zero_coords()[1]:
                        self.x_coord_to = self.back_x
                        self.y_coord_to = self.back_y
                        self.back_x = self.x_coord
                        self.back_y = self.y_coord

            def update_quest(self):
                for elem in all_sprites_5:
                    elem.update((self.x_coord, self.y_coord))

            def catched(self):
                if pygame.sprite.collide_mask(self, evil):
                    return True
                else:
                    return False

            def movement(self):
                if not self.stop():
                    if self.x_coord_to != self.x_coord:
                        self.x_coord += ((self.x_coord_to - self.x_coord) / abs(
                            self.x_coord_to - self.x_coord)) * v / fps
                    if self.y_coord_to != self.y_coord:
                        self.y_coord += ((self.y_coord_to - self.y_coord) / abs(
                            self.y_coord_to - self.y_coord)) * v / fps
                else:
                    self.back_x = self.x_coord
                    self.back_y = self.y_coord
                self.rect.x = self.x_coord
                self.rect.y = self.y_coord

            def get_coords(self):
                return self.x_coord, self.y_coord

            def win(self):
                if self.y_coord > board.zero_coords()[2] * board.zero_coords()[4] + board.zero_coords()[0]:
                    return True
                return False

        class Evil(pygame.sprite.Sprite):
            image = load_image("min.png")

            def __init__(self, x_coord, y_coord, size):
                super().__init__(all_sprites_3)
                self.x_coord, self.y_coord, self.size = x_coord, y_coord, size
                self.image = Evil.image
                self.image = pygame.transform.scale(self.image, (self.size, self.size))
                self.rect = self.image.get_rect()
                self.rect.x = self.x_coord
                self.rect.y = self.y_coord
                self.back_x = self.x_coord
                self.back_y = self.y_coord
                self.x_coord_to = self.x_coord
                self.y_coord_to = self.y_coord
                self.orig_x = self.x_coord
                self.orig_y = self.y_coord
                self.mask = pygame.mask.from_surface(self.image)
                self.prev = None

            def aim(self, x, y):
                self.x_coord_to = x
                self.y_coord_to = y
                self.orig_x, self.orig_y = self.x_coord, self.y_coord
                self.back_x = self.x_coord
                self.back_y = self.y_coord

            def stop(self):
                if (self.x_coord_to, self.y_coord_to) == (self.x_coord, self.y_coord):
                    return True
                else:
                    return False

            def next(self):
                if self.stop() and (self.orig_x, self.orig_y) != (self.x_coord, self.y_coord):
                    self.orig_x, self.orig_y = self.x_coord, self.y_coord
                    return 0
                else:
                    return 1

            def movement(self):
                if not self.stop():
                    if self.x_coord_to != self.x_coord:
                        self.x_coord += ((self.x_coord_to - self.x_coord) / abs(
                            self.x_coord_to - self.x_coord)) * v / fps
                    if self.y_coord_to != self.y_coord:
                        self.y_coord += ((self.y_coord_to - self.y_coord) / abs(
                            self.y_coord_to - self.y_coord)) * v / fps
                else:
                    self.back_x = self.x_coord
                    self.back_y = self.y_coord
                self.rect.x = self.x_coord
                self.rect.y = self.y_coord

            def get_coords(self):
                return self.x_coord, self.y_coord

            def go(self):
                vari = []
                move = board.zero_coords()[2]
                left = True
                right = True
                up = True
                down = True
                for elem in all_sprites:
                    if elem.update((self.x_coord - 20, self.y_coord)):
                        left = False
                    if elem.update((self.x_coord + move - 20, self.y_coord)):
                        right = False
                    if elem.update((self.x_coord, self.y_coord + move - 15)) or self.y_coord + move - 15 >= \
                            board.zero_coords()[2] * board.zero_coords()[4] + board.zero_coords()[1]:
                        down = False
                    if elem.update((self.x_coord, self.y_coord - 15)):
                        up = False
                if left:
                    vari.append("LEFT")
                if right:
                    vari.append("RIGHT")
                if down:
                    vari.append("DOWN")
                if up:
                    vari.append("UP")
                if self.prev is not None and len(vari) > 1:
                    if self.prev == "LEFT":
                        vari.pop(vari.index("RIGHT"))
                    elif self.prev == "RIGHT":
                        vari.pop(vari.index("LEFT"))
                    elif self.prev == "UP":
                        vari.pop(vari.index("DOWN"))
                    elif self.prev == "DOWN":
                        vari.pop(vari.index("UP"))
                direction = choice(vari)
                self.prev = direction
                x_coord, y_coord = evil.get_coords()[0], evil.get_coords()[1]
                x_coord2, y_coord2 = board.get_cell((x_coord, y_coord), direction)
                evil.aim(x_coord2, y_coord2)

            def catched(self):
                if pygame.sprite.collide_mask(self, hero):
                    return True
                else:
                    return False

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
        all_sprites_2 = pygame.sprite.Group()
        all_sprites_3 = pygame.sprite.Group()
        all_sprites_4 = pygame.sprite.Group()
        all_sprites_5 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        board = Board()
        board.set_view(100, 100, 80)
        b = board.zero_coords()
        Wall_place()
        ans = {}
        Quest_place()
        x_coord, y_coord, size = b[0] + 20, b[1] + 15, b[2] - 35
        hero = Hero(x_coord, y_coord, size)
        x_coord_e, y_coord_e, size_e = b[0] + (b[2] * (b[3] - 1)) + 20, b[1] + (b[2] * (b[4] - 1)) + 15, b[2] - 35
        evil = Evil(x_coord_e, y_coord_e, size_e)
        evil_move = 0
        running = True
        clock = pygame.time.Clock()
        direction = None
        player = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if hero.stop() and player == 0:
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
            fon = pygame.transform.scale(load_image('floor.png'), (width, height))
            screen.blit(fon, (0, 0))
            # Floor(b[3], b[4], b[2], b[0], b[1])
            # all_sprites_4.draw(screen)
            if player == 0:
                hero.movement()
                player = hero.next()
                if player == 1:
                    evil_move = 1
                    evil.go()
            else:
                evil.movement()
                player = evil.next()
                if player == 1 and evil.stop():
                    evil.go()
                elif player == 0 and evil.stop() and evil_move != 0:
                    player = 1
                    evil_move -= 1
                    evil.go()

            board.render(screen)
            all_sprites.draw(screen)
            all_sprites_5.draw(screen)
            all_sprites_2.draw(screen)
            all_sprites_3.draw(screen)
            hero.update()
            hero.update_quest()
            evil.update()
            if hero.catched() or evil.catched():
                min_win()
            if hero.win():
                hero_win()
            clock.tick(fps)
            pygame.display.flip()
        terminate()


    hello()
pygame.quit()
