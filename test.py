import pygame
import os
import random
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtWidgets import QInputDialog

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Лабиринт')
    size = WIDTH, HEIGHT = 1000, 1000
    screen = pygame.display.set_mode(size)
    FPS = 50
    all_sprites_1 = pygame.sprite.Group()
    all_sprites_1_1 = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()


    # clock = pygame.time.Clock()

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


    class Play(pygame.sprite.Sprite):
        image = load_image("play.png")

        def __init__(self, left, top, size_x, size_y):
            super().__init__(all_sprites_1_1)
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


    def start_screen():
        intro_text = ["                                       ПРАВИЛА", "",
                      " Перед вами игра 'ЛАБИРИНТ МИНОТАВРА. Ваша цель - ", "",
                      " пройти через лабиринт к выходу, не столкнувшись", "",
                      " с минотавром. Однако это не всё - вам нужно ", "",
                      " ответить верно не меньше чем на 40 вопросов", "",
                      " из 50, которые разбросаны по всему полю, чтобы", "",
                      " пройти на следующий уровень.Так что вам придётся", "",
                      " изрядно побродить по лабиринту и не раз облиться", "",
                      " холодным потом, чувствуя, что минотавр уже близко!", "",
                      " Для удобства наверху находятся подсказки", "",
                      " (слева направо): кол-во правильных ответов, кол-во", "",
                      " неправильных, кол-во необходимых правильных ответов, ", "",
                      " чтобы пройти на следующий уровень. Передвижение ", "",
                      " осуществляется нажатием на клавиши управления", "",
                      " курсором. !ВНИМАНИЕ! Не удерживайте клавишу,  ", "",
                      " нажимайте один раз, если не хотите сломать игру", "",
                      " и испортить себе удовольствие.", "",
                      "                          УДАЧНЫХ ПОДВИГОВ!"]

        fon = pygame.transform.scale(load_image('rules.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 130
        min_im = Play(850, 950, 150, 50)
        for line in intro_text:
            string_rendered = font.render(line, 5, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            intro_rect.x = 200
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for elem in all_sprites_1_1:
                        if elem.update(event.pos):
                            terminate()

                all_sprites_1.draw(screen)
                all_sprites_1_1.draw(screen)
            pygame.display.flip()
            # clock.tick(FPS)


    start_screen()

pygame.quit()
