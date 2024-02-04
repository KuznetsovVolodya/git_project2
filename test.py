import pygame
import os
from random import choice, shuffle
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLineEdit, QDesktopWidget, QLabel, QLayout
from PyQt5 import QtGui
import sqlite3


#
class Play(pygame.sprite.Sprite):
    def __init__(self, picture, left, top, size_x, size_y, group):
        super().__init__(group)
        self.image = load_image(picture)
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


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name):
    # преобразование изображения из папки data
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    colorkey = -1
    image.set_colorkey(colorkey)
    return image


class Phone_image(pygame.sprite.Sprite):
    def __init__(self, picture, left, top, size_x, size_y, group):
        super().__init__(group)
        self.image = load_image(picture)
        self.image = pygame.transform.scale(self.image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = left
        self.rect.y = top


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Лабиринт')
    size = width, height = (1000, 1000)
    screen = pygame.display.set_mode(size)
    # создание окна
    v = 420
    fps = 60
    all_sprites_0 = pygame.sprite.Group()
    all_sprites_0_1 = pygame.sprite.Group()
    FPS = 5

    intro_text = ["                                       И... ЭТО ОКОНЧАТЕЛЬНАЯ ПОБЕДА!", "",
                  "                                 Поздравляем! Вы прошли последний уровень! ",
                  "                Увидимся в следующий раз! И не забывайте - подвиги вокруг вас!"]

    fon = pygame.transform.scale(load_image('fin_win_phone.png'), (width, height))
    circle_be = True

    Play('sign.png', 300, 200, 550, 800, all_sprites_0_1)
    x_pos = 300
    y_pos = 200
    arg = 1
    Phone_image('fin_win_2.png', 100, 300, 800, 600, all_sprites_0)
    clock = pygame.time.Clock()

    while True:
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 35)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for elem in all_sprites_0_1:
                    if elem.update(event.pos):
                        circle_be = False
        if circle_be:
            if x_pos < 300:
                arg = 1
            elif x_pos > 400:
                arg = -1
            x_pos += v / fps * arg
            y_pos += v / fps * arg
            all_sprites_0_2 = pygame.sprite.Group()
            Play('press.png', 100, 600, x_pos, y_pos, all_sprites_0_2)
            all_sprites_0_1.draw(screen)
            all_sprites_0_2.draw(screen)
        else:
            all_sprites_0.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
