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
    all_sprites_0 = pygame.sprite.Group()
    all_sprites_0_1 = pygame.sprite.Group()
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


    def start_screen():
        intro_text = ["", "      МИНОТАВР ПОБЕДИЛ", ""]

        fon = pygame.transform.scale(load_image('phone_lose.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 50)
        text_coord = 50
        min_im = Phone_image(100, 200, 800, 700)
        min_im = Play(850, 950, 150, 50)
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
                            terminate()

                all_sprites_0.draw(screen)
                all_sprites_0_1.draw(screen)
            pygame.display.flip()
            # clock.tick(FPS)


    start_screen()

pygame.quit()
