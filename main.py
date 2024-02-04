import pygame
import os
from random import choice, shuffle
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QDesktopWidget, QLabel
from PyQt5 import QtGui
import sqlite3

if __name__ == '__main__':
    pygame.init()
    # создание окна
    pygame.display.set_caption('Лабиринт')
    size = width, height = (1000, 1000)
    screen = pygame.display.set_mode(size)
    # скорость и частота кадров
    v = 240
    fps = 60


    def load_image(name):
        # загрузка изображения из папки data, удаление фона
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname)
        image = image.convert_alpha()
        colorkey = -1
        image.set_colorkey(colorkey)
        return image


    def load_level_y(filename):
        # создание списка списков из текстового файла с координатами стенок по горизонтали
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        return list(map(lambda y: y.ljust(10, '.'), level_map))
        # заполнение занятых клеток соответствующим знаком(отсутствуют в файле с правой стороны для экономии места и
        # памяти)


    def load_level_x(filename):
        # создание списка списков из текстового файла с координатами стенок по вертикали
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        return list(map(lambda x: x.ljust(11, '#'), level_map))
        # заполнение пустых клеток соответствующим знаком(отсутствуют в файле с правой стороны для экономии места и
        # памяти)


    def terminate():
        # осуществляет выход из игры и закрытие окна
        pygame.quit()
        sys.exit()


    class Transform_image(pygame.sprite.Sprite):
        # преобразование изображения в спрайт
        def __init__(self, picture, left, top, size_x, size_y, group):
            super().__init__(group)
            self.image = load_image(picture)
            self.image = pygame.transform.scale(self.image, (size_x, size_y))
            self.rect = self.image.get_rect()
            self.size_x = size_x
            self.size_y = size_y
            # переменные с размерами изображения
            self.rect.x = left
            self.rect.y = top

        def update(self, pos):
            # проверка столкновения - если координаты курсора внутри границ изображения вывести True; иначе False
            if self.rect.x <= pos[0] <= self.rect.x + self.size_x and \
                    self.rect.y <= pos[1] <= self.rect.y + self.size_y:
                return True
            return False


    class Wall(pygame.sprite.Sprite):
        # создание спрайтов стенок
        image = load_image("wall.png")

        # загрузить изображение 1 стенки

        def __init__(self, wall_width, wall_height, wall_cell_size, wall_left, wall_top, wall_size_x,
                     wall_size_y, wall_group):
            super().__init__(wall_group)
            self.image = Wall.image
            self.image = pygame.transform.scale(self.image, (wall_size_x, wall_size_y))
            self.rect = self.image.get_rect()
            self.rect.x = wall_left + wall_width * wall_cell_size - 1
            self.rect.y = wall_top + wall_height * wall_cell_size - 1
            self.mask = pygame.mask.from_surface(self.image)

        def update(self, coords):
            # проверка столкновения со стенками
            if self.rect.collidepoint(coords):
                return True
            return False


    class Wall_place:
        # размещение спрайтов стенок
        def __init__(self, wall_place_group, boardy, lvlx='walls_x', lvly='walls_y'):
            self.x_place = load_level_x(lvlx)
            # расстановка стенок по вертикали
            for ix in range(len(self.x_place)):
                for jx in range(len(self.x_place[ix])):
                    if self.x_place[ix][jx] == "#":
                        #  если клетка занята('#'), то создаём соответствующий спрайт
                        board_co_x = boardy.zero_coords()
                        # задаём размеры, пользуясь размерами клетчатого поля(задано далее);
                        # стенка повёрнута вертикально
                        Wall(jx, ix, board_co_x[2], board_co_x[0], board_co_x[1], 5, board_co_x[2] + 2,
                             wall_place_group)
            self.y_place = load_level_y(lvly)
            # расстановка стенок по горизонтали; выполняется аналогично
            for iy in range(len(self.y_place)):
                for jy in range(len(self.y_place[iy])):
                    if self.y_place[iy][jy] == "#":
                        board_co_y = boardy.zero_coords()
                        Wall(jy, iy, board_co_y[2], board_co_y[0], board_co_y[1], board_co_y[2] + 2, 5,
                             wall_place_group)


    def rules():
        # дисплей с правилами
        all_sprites_rul = pygame.sprite.Group()
        intro_text = ["                                       ПРАВИЛА", "",
                      " Перед вами игра 'ЛАБИРИНТ МИНОТАВРА. Ваша цель - ", "",
                      " пройти через лабиринт к выходу, не столкнувшись", "",
                      " с минотавром. Однако это не всё - вам нужно ", "",
                      " ответить верно не меньше чем на x вопросов", "",
                      " из 50(первый уровень - 20, второй - 40),", "",
                      " которые разбросаны по всему полю, чтобы", "",
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

        fon = pygame.transform.scale(load_image('rules.png'), (width, height))
        # здесь и далее - фоном становится соответствующая загруженная картинка
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 130
        Transform_image('play.png', 700, 900, 300, 100, all_sprites_rul)
        # здесь и далее - создание кнопки перехода к уровню или правилам
        # здесь и далее - построчный вывод текста
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
                #     здесь и далее - закрытие игры
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for elem in all_sprites_rul:
                        if elem.update(event.pos):
                            # здесь и далее - срабатывает при нажатии кнопки
                            first_game()
                            #  здесь и далее - запуск последнего непройденного уровня
            all_sprites_rul.draw(screen)
            pygame.display.flip()


    def hello():
        all_sprites_hello = pygame.sprite.Group()
        all_sprites_hello_1 = pygame.sprite.Group()
        intro_text = ["'become a legend' представляет", "",
                      "      ЛАБИРИНТ МИНОТАВРА", "",
                      "         Компьютерная игра",
                      "по мотивам знаменитого мифа"]
        fon = pygame.transform.scale(load_image('phone.png'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 50)
        text_coord = 50
        Transform_image('min_phone.png', 100, 400, 800, 500, all_sprites_hello)
        Transform_image('rules_but.png', 700, 900, 300, 100, all_sprites_hello_1)
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
                    for elem in all_sprites_hello_1:
                        if elem.update(event.pos):
                            rules()
                all_sprites_hello.draw(screen)
                all_sprites_hello_1.draw(screen)
            pygame.display.flip()


    def min_win():
        all_sprites_mw = pygame.sprite.Group()
        all_sprites_mw_1 = pygame.sprite.Group()
        FPS = 5
        intro_text = ["", "                                  МИНОТАВР ПОБЕДИЛ", "",
                      "        Готовы взять реванш? Тогда пройдите этот уровень ещё раз!"]

        fon = pygame.transform.scale(load_image('phone_lose.png'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 35)
        text_coord = 50
        Transform_image('min_win.png', 100, 200, 800, 700, all_sprites_mw)
        Transform_image('play.png', 700, 900, 300, 100, all_sprites_mw_1)
        clock = pygame.time.Clock()
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('grey'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for elem in all_sprites_mw_1:
                        if elem.update(event.pos):
                            first_game()

            all_sprites_mw.draw(screen)
            all_sprites_mw_1.draw(screen)
            clock.tick(FPS)
            pygame.display.flip()


    def hero_win():
        all_sprites_hw = pygame.sprite.Group()
        all_sprites_hw_1 = pygame.sprite.Group()
        FPS = 5

        intro_text = ["                                              ВЫ ПОБЕДИЛИ", "",
                      "        Готовы поднять ставки? Тогда пройдите следующий уровень!"]

        fon = pygame.transform.scale(load_image('phone_win.png'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 35)
        text_coord = 50
        Transform_image('hero_win.png', 100, 200, 800, 700, all_sprites_hw)
        Transform_image('play.png', 700, 900, 300, 100, all_sprites_hw_1)
        clock = pygame.time.Clock()
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('green'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for elem in all_sprites_hw_1:
                        if elem.update(event.pos):
                            first_game(2)
                            # переход ко второму уровню

            all_sprites_hw.draw(screen)
            all_sprites_hw_1.draw(screen)
            clock.tick(FPS)
            pygame.display.flip()


    def no_win():
        all_sprites_nw = pygame.sprite.Group()
        all_sprites_nw_1 = pygame.sprite.Group()
        FPS = 5

        intro_text = ["        БАЛЛОВ НЕДОСТАТОЧНО, ЧТОБЫ ПРОЙТИ НА СЛЕДУЮЩИЙ УРОВЕНЬ", "",
                      "                                  Увы, победа далась слишком дорогой ценой. ",
                      "                                    Но вы можете испытать удачу ещё раз!"]

        fon = pygame.transform.scale(load_image('less_win_phone.png'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 35)
        text_coord = 50
        Transform_image('less_win.png', 100, 200, 800, 700, all_sprites_nw)
        Transform_image('play.png', 700, 900, 300, 100, all_sprites_nw_1)
        clock = pygame.time.Clock()
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for elem in all_sprites_nw_1:
                        if elem.update(event.pos):
                            first_game()

            all_sprites_nw.draw(screen)
            all_sprites_nw_1.draw(screen)
            clock.tick(FPS)
            pygame.display.flip()


    def fin_win():
        all_sprites_fw = pygame.sprite.Group()
        all_sprites_fw_1 = pygame.sprite.Group()
        FPS = 5

        intro_text = ["                                       И... ЭТО ОКОНЧАТЕЛЬНАЯ ПОБЕДА!", "",
                      "                                 Поздравляем! Вы прошли последний уровень! ",
                      "                Увидимся в следующий раз! И не забывайте - подвиги вокруг вас!"]

        fon = pygame.transform.scale(load_image('fin_win_phone.png'), (width, height))
        press_be = False
        # проверка нажатия
        Transform_image('sign.png', 300, 200, 550, 800, all_sprites_fw_1)
        # изображение, появляющееся до нажатия(эмблема фирмы)
        x_pos = 300
        y_pos = 200
        arg = 1
        # размеры в длину/высоту и знак изменения(увеличение или уменьшение)
        Transform_image('fin_win_2.png', 100, 300, 800, 600, all_sprites_fw)
        # изображение, появляющееся после нажатия
        clock = pygame.time.Clock()

        while True:
            screen.blit(fon, (0, 0))
            font = pygame.font.Font(None, 35)
            # вывод текста
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
                    for elem in all_sprites_fw_1:
                        if elem.update(event.pos):
                            # если нажали на первое изображение - начать выводить второе
                            press_be = True
            if not press_be:
                # если ширина изображеня < 300 - увеличивать, если больше 400 - уменьшать его
                if x_pos < 300:
                    arg = 1
                elif x_pos > 400:
                    arg = -1
                x_pos += v / fps * arg
                y_pos += v / fps * arg
                # изменение размеров
                all_sprites_0_2 = pygame.sprite.Group()
                Transform_image('press.png', 100, 600, x_pos, y_pos, all_sprites_0_2)
                # создание спрайта-стрелки с текущим размером
                all_sprites_fw_1.draw(screen)
                all_sprites_0_2.draw(screen)
                # вывод стрелки и первого изображения
            else:
                all_sprites_fw.draw(screen)
                # после нажатия выводить только второе изображение
            pygame.display.flip()
            clock.tick(FPS)


    def first_game(num=1):
        # основное игровое поле
        class Questt(QWidget):
            # создание диалогового окна для ответа на вопросы
            def __init__(self, numy, db='questions.db'):
                super().__init__()
                self.label = QLabel(self)
                self.db = db
                # вызов базы данных с вопросами и ответами на них
                self.num = numy
                #  номер вопроса
                self.c = None
                self.b = None
                self.a = None
                # ячейки для записи вариантов ответа
                con = sqlite3.connect('questions.db')
                cur = con.cursor()
                self.res = cur.execute(
                    f'''SELECT question, a, b, c, ans FROM questions WHERE id == {self.num + 1}''').fetchall()
                self.corr = 0
                self.incorr = 0
                #
                con.close()
                self.initUI()

            def initUI(self):
                self.setGeometry(0, 0, 800, 450)
                qr = self.frameGeometry()
                qr.moveCenter(QDesktopWidget().availableGeometry().center())
                self.move(qr.topLeft())
                self.setWindowTitle('Question')
                # создание окна
                self.c = QPushButton(f'c) {self.res[0][3]}', self)
                self.b = QPushButton(f'b) {self.res[0][2]}', self)
                self.a = QPushButton(f'a) {self.res[0][1]}', self)
                # вывод вариантов ответа
                self.a.move(50, 300)
                self.a.resize(200, 50)
                self.a.clicked.connect(lambda: self.hello('a'))
                self.b.move(300, 300)
                self.b.resize(200, 50)
                self.b.clicked.connect(lambda: self.hello('b'))
                self.c.move(550, 300)
                self.c.resize(200, 50)
                self.c.clicked.connect(lambda: self.hello('c'))
                self.label.setText(self.res[0][0])
                # размещение и задание размеров ячеек с ответами, подсоединение к функции для проверки
                self.label.move(20, 60)
                self.label.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                #  вывод вопроса

            def hello(self, answered):
                # после проверки на верность зачисляет балл игроку(если верный) или минотавру(если неверный)
                if self.iscorrect(answered):
                    self.corr = 1
                else:
                    self.incorr = 1
                self.close()

            def iscorrect(self, n=''):
                # проверяет, совпадает ли выбранный вариант с верным(указан таковым в базе данных)
                if n != self.res[0][4]:
                    return False
                return True

        class Quest(pygame.sprite.Sprite):
            # взаимодействие с полем(вывод вопроса при переходе на соответствующую клетку)
            image = load_image("quest.png")
            image2 = load_image("quest_ans.png")

            # загрузка изображения вопроса(неотвеченного и отвеченного)

            def __init__(self, quest_width, quest_height, quest_cell_size, quest_left, quest_top, quest_size_x,
                         quest_size_y):
                global count_quests
                global min_ans
                count_quests = 0
                min_ans = 0
                # здесь и далее count_quests - количество правильных ответов; min_ans - количество неправильных ответов
                super().__init__(all_sprites_quests)
                self.y_pos = quest_top + quest_height * quest_cell_size
                self.x_pos = quest_left + quest_width * quest_cell_size
                # определение координат вопроса
                if f'{self.x_pos}{self.y_pos}' not in ans:
                    ans[f'{self.x_pos}{self.y_pos}'] = None
                    # добавление вопроса в словарь всех вопросов(статус - неотвеченный)
                if ans[f'{self.x_pos}{self.y_pos}'] is None:
                    # выбор картинки в зависимости от статуса
                    self.image = Quest.image
                else:
                    self.image = Quest.image2
                self.place = list(ans.keys()).index(f'{self.x_pos}{self.y_pos}')
                # определение номера вопроса
                self.x = quest_size_x
                self.y = quest_size_y
                # размеры вопроса
                self.image = pygame.transform.scale(self.image, (self.x, self.y))
                self.rect = self.image.get_rect()
                self.rect.x = self.x_pos
                self.rect.y = self.y_pos
                # задание координат
                self.mask = pygame.mask.from_surface(self.image)
                # создание маски (проверка столкновения)

            def update(self, q_coord):
                # реализация взаимодействия с героем, за которого играет пользователь
                if self.rect.collidepoint(q_coord) and not (ans[f'{self.x_pos}{self.y_pos}']):
                    # проверка на столкновение(вступил ли игрок на зону вопроса) и статус вопроса
                    # (дан ли ранее ответ на этот вопрос)
                    global count_quests
                    global min_ans
                    app = QApplication(sys.argv)
                    ex = Questt(self.place)
                    ex.show()
                    app.exec()
                    # вывод диалогового окна
                    count_quests += ex.corr
                    min_ans += ex.incorr
                    # изменение количества правильных и неправильных ответов в зависимости от ответа пользователя
                    ans[f'{self.x_pos}{self.y_pos}'] = True
                    # изменение статуса вопроса на "отвеченный"
                    self.image = Quest.image2
                    self.image = pygame.transform.scale(self.image, (self.x, self.y))
                    self.rect = self.image.get_rect()
                    self.rect.x = self.x_pos
                    self.rect.y = self.y_pos
                    self.mask = pygame.mask.from_surface(self.image)
                    # изменение картинки на отвеченную

        class Quest_place():
            # расположение вопросов
            def __init__(self):
                num_quests = []
                for k in range(1, 100):
                    num_quests.append(k)
                # создание списка всех вопросов(их номеров)
                shuffle(num_quests)
                num_quests = num_quests[:50]
                # выбор случайных 50 вопросов из общего количества(100)
                for i in range(50):
                    bzc = board.zero_coords()
                    # выбор параметров клетчатого поля для дальнейшей работы с ними
                    j1 = num_quests[i] // 10
                    i1 = num_quests[i] % 10
                    # координаты вопроса(номер клетки по вертикали и горизонтали(клетки нумеруются последовательно,
                    # каждая новая строка - новый десяток))
                    Quest(j1, i1, bzc[2], bzc[0], bzc[1], bzc[2], bzc[2])
                    # создание соответствующего  класса

        class Hero(pygame.sprite.Sprite):
            # класс, реализующий движение и взаимодействия героя, за которого играет пользователь
            image = load_image("hero.png")

            # загрузка изображения героя

            def __init__(self, hero_x, hero_y, hero_size):
                super().__init__(all_sprites_hero)
                self.x_coord, self.y_coord, self.size = hero_x, hero_y, hero_size
                self.image = Hero.image
                self.image = pygame.transform.scale(self.image, (self.size, self.size))
                self.rect = self.image.get_rect()
                self.rect.x = self.x_coord
                self.rect.y = self.y_coord
                # текущие координаты героя
                self.orig_x = self.x_coord
                self.orig_y = self.y_coord
                # изначальные координаты клетки(нужны, чтобы определить, вернулся ли герой обратно после столкновения
                # или перешёл на другую клетку)
                self.x_coord_to = self.x_coord
                self.y_coord_to = self.y_coord
                # координаты, на которые должен переместиться герой(определяются нажатием соответствующей
                # кнопки на клавиатуре) - далее координаты цели
                self.mask = pygame.mask.from_surface(self.image)
                #  маска для определения столкновения с минотавром или стенками

            def aim(self, x_to, y_to):
                # задаёт координаты, к которым движется герой
                self.x_coord_to = x_to
                self.y_coord_to = y_to
                self.orig_x, self.orig_y = self.x_coord, self.y_coord
                # изначальные координаты - текущие координаты героя

            def stop(self):
                # проверка окнчания движения(совпали ли текущие координаты с координатами цели)
                if (self.x_coord_to, self.y_coord_to) == (self.x_coord, self.y_coord):
                    return True
                return False

            def next(self):
                # проверка завершения хода - игрок остановился и его текущие координаты не равны его
                # изначальным координатам(откуда он начал движение)
                if self.stop() and (self.orig_x, self.orig_y) != (self.x_coord, self.y_coord):
                    self.orig_x, self.orig_y = self.x_coord, self.y_coord
                    # изменить изначальные координаты на текущие(т.к. ход завершён)
                    return 1
                return 0

            def update(self):
                # проверка столкновения со стенками(по маске)
                for elem in all_sprites_walls:
                    # проверка для каждой стенки
                    if pygame.sprite.collide_mask(self, elem):
                        self.x_coord_to = self.orig_x
                        self.y_coord_to = self.orig_y
                        # при столкновении координатами цели становятся изначальные координаты
                        # (герой возвращается туда, откуда начал движение)
                        break

            def update_quest(self):
                # реализация столкновения с вопросом(по маске); если герой вступает на клетку, на которой
                # находится вопрос, всплывает диалоговое окно(функция описана в классе Quest)
                for elem in all_sprites_quests:
                    # для каждого вопроса проверяется, не столкнулся ли с ним герой
                    elem.update((self.x_coord, self.y_coord))

            def catched(self):
                # проверка на столкновение с минотавром(по маске)
                if pygame.sprite.collide_mask(self, evil):
                    return True
                return False

            def movement(self):
                # реализует движение героя
                if not self.stop():
                    # осуществляется, если герой не остановился, и координаты цели не соответствуют
                    # текущим(по отдельности)
                    if self.x_coord_to != self.x_coord:
                        self.x_coord += ((self.x_coord_to - self.x_coord) / abs(
                            self.x_coord_to - self.x_coord)) * v / fps
                        # к текущей координате по горизонтали прибавляется(с учётом направления) кол-во пикселей,
                        # определяемых скоростью(аналогично по вертикали)
                    if self.y_coord_to != self.y_coord:
                        self.y_coord += ((self.y_coord_to - self.y_coord) / abs(
                            self.y_coord_to - self.y_coord)) * v / fps
                self.rect.x = self.x_coord
                self.rect.y = self.y_coord
                #  изменяются текущие координаты

            def get_coords(self):
                # возвращает текущие координаты героя
                return self.x_coord, self.y_coord

            def win(self):
                # определяет вышел ли герой за пределы поля
                if self.y_coord > board.zero_coords()[2] * board.zero_coords()[4] + board.zero_coords()[0]:
                    # учитывается только вертикальная ось, т.к. по горизонтали выхода нет
                    return True
                return False

        class Evil(pygame.sprite.Sprite):
            # класс, реализующий движение и взаимодействия минотавра
            image = load_image("min.png")
            # загрузка изображения минотавра

            def __init__(self, evil_x, evil_y, evil_size):
                super().__init__(all_sprites_evil)
                self.x_coord, self.y_coord, self.size = evil_x, evil_y, evil_size
                self.image = Evil.image
                self.image = pygame.transform.scale(self.image, (self.size, self.size))
                self.rect = self.image.get_rect()
                self.rect.x = self.x_coord
                self.rect.y = self.y_coord
                # текущие координаты минотавра
                self.x_coord_to = self.x_coord
                self.y_coord_to = self.y_coord
                # координаты, на которые должен переместиться минотавр - далее координаты цели
                self.orig_x = self.x_coord
                self.orig_y = self.y_coord
                # изначальные координаты минотавра
                self.mask = pygame.mask.from_surface(self.image)
                #  маска для определения столкновения с героем
                self.prev = None
                # направление предыдущего хода(в какую сторону сходил минотавр)

            def aim(self, x, y):
                # задаёт координаты, к которым движется минотавр
                self.x_coord_to = x
                self.y_coord_to = y
                self.orig_x, self.orig_y = self.x_coord, self.y_coord
                # изначальные координаты - текущие координаты минотавра

            def stop(self):
                # проверка окнчания движения(совпали ли текущие координаты с координатами цели)
                if (self.x_coord_to, self.y_coord_to) == (self.x_coord, self.y_coord):
                    return True
                else:
                    return False

            def next(self):
                # проверка завершения хода - игрок остановился и его текущие координаты не равны его
                # изначальным координатам(откуда он начал движение)
                if self.stop() and (self.orig_x, self.orig_y) != (self.x_coord, self.y_coord):
                    self.orig_x, self.orig_y = self.x_coord, self.y_coord
                    return 0
                else:
                    return 1

            def movement(self):
                # реализует движение минотавра
                if not self.stop():
                    # осуществляется, если минотавр не остановился, и координаты цели не соответствуют
                    # текущим(по отдельности)
                    if self.x_coord_to != self.x_coord:
                        self.x_coord += ((self.x_coord_to - self.x_coord) / abs(
                            self.x_coord_to - self.x_coord)) * v / fps
                        # к текущей координате по горизонтали прибавляется(с учётом направления) кол-во пикселей,
                        # определяемых скоростью(аналогично по вертикали)
                    if self.y_coord_to != self.y_coord:
                        self.y_coord += ((self.y_coord_to - self.y_coord) / abs(
                            self.y_coord_to - self.y_coord)) * v / fps
                self.rect.x = self.x_coord
                self.rect.y = self.y_coord
                #  изменяются текущие координаты

            def get_coords(self):
                # возвращает текущие координаты минотавра
                return self.x_coord, self.y_coord

            def go(self):
                # выбирает направление движения минотавра
                go_variants = []
                # создание списка вариантов возможных напрвлений
                move = board.zero_coords()[2]
                # определение длины клетки поля(для вычисления, не находится ли в данной координате стенка)
                left = True
                right = True
                up = True
                down = True
                for elem in all_sprites_walls:
                    # проверка на нахождение стенок: если в заданной координате находится стена(к текущей координате
                    # прибавляется длина клетки и вычитается расстояние, на которое минотавр отдален от границы
                    # текущей клетки(оно постоянно и задано изначально)), данное направление удаляется из возможных
                    if elem.update((self.x_coord - 20, self.y_coord)):
                        left = False
                    if elem.update((self.x_coord + move - 20, self.y_coord)):
                        right = False
                    if elem.update((self.x_coord, self.y_coord + move - 15)) or self.y_coord + move - 15 >= \
                            board.zero_coords()[2] * board.zero_coords()[4] + board.zero_coords()[1]:
                        # дополнительная проверка на выход из лабиринта(возможно только при движении вертикально вниз)
                        down = False
                    if elem.update((self.x_coord, self.y_coord - 15)):
                        up = False
                # добавление в список всех возможных вариантов
                if left:
                    go_variants.append("LEFT")
                if right:
                    go_variants.append("RIGHT")
                if down:
                    go_variants.append("DOWN")
                if up:
                    go_variants.append("UP")
                if self.prev is not None and len(go_variants) > 1:
                    # удаление из списка направления, по которому минотавр может вернуться назад
                    # (если имеются другие варианты движения); из списка удаляется направление, обратное направлению,
                    # выбранному в прошлый раз
                    if self.prev == "LEFT":
                        go_variants.pop(go_variants.index("RIGHT"))
                    elif self.prev == "RIGHT":
                        go_variants.pop(go_variants.index("LEFT"))
                    elif self.prev == "UP":
                        go_variants.pop(go_variants.index("DOWN"))
                    elif self.prev == "DOWN":
                        go_variants.pop(go_variants.index("UP"))
                evil_direction = choice(go_variants)
                # направление выбирается случайным образом из списка возможных
                self.prev = evil_direction
                # в переменную с последним направлением записывается текущее
                x_coord_to, y_coord_to = board.get_cell((evil.get_coords()[0], evil.get_coords()[1]), evil_direction)
                evil.aim(x_coord_to, y_coord_to)
                # с помощью функции класса Board определяются координаты, к которым движется минотавр, и
                # передаются в соответствующую функцию данного класса

        class Board:
            # создание и взаимодействие с клеточным полем
            def __init__(self):
                self.width = 10
                self.height = 10
                # количество клеток по горизонтали и вертикали
                self.board = [[0] * width for _ in range(height)]
                # список списков всех клеток
                self.left = 10
                self.top = 10
                # координаты левого верхнего края
                self.cell_size = 50
                # ширина клетки

            def zero_coords(self):
                # возвращает координаты левого верхнего края, ширину клетки, ширину и высоту таблицы в клетках
                return self.left, self.top, self.cell_size, self.width, self.height

            def set_view(self, left, top, cell_size):
                # изменение координат верхнего левого края и ширины клетки
                self.left = left
                self.top = top
                self.cell_size = cell_size

            def render(self, screen):
                # создание таблицы(клеточного поля) и вывод её на экран
                for i in range(self.width):
                    for j in range(self.height):
                        x1 = self.left + self.cell_size * i
                        y1 = self.top + self.cell_size * j
                        pygame.draw.rect(screen, "grey", ((x1, y1), (self.cell_size, self.cell_size)), 2)
                        # толщина границы - 2 пикселя

            def get_cell(self, mouse_pos, pressed_button):
                # определение координаты, к которой необходимо двигаться, по текущему положению и направлению
                x_c, y_c = mouse_pos[0], mouse_pos[1]
                # текущие координаты
                if pressed_button == "RIGHT":
                    x_c += self.cell_size
                elif pressed_button == "LEFT":
                    x_c -= self.cell_size
                elif pressed_button == "UP":
                    y_c -= self.cell_size
                elif pressed_button == "DOWN":
                    y_c += self.cell_size
                # изменение положения клетки(перемещение на ширину клетки в соответствующем направлении)
                return x_c, y_c

        global count_quests
        global min_ans
        all_sprites_walls = pygame.sprite.Group()
        all_sprites_hero = pygame.sprite.Group()
        all_sprites_evil = pygame.sprite.Group()
        all_sprites_quests = pygame.sprite.Group()
        all_sprites_ans_labels = pygame.sprite.Group()
        board = Board()
        board.set_view(100, 100, 80)
        # создание клеточного поля и задание размеров и положения
        b = board.zero_coords()
        if num == 1:
            Wall_place(all_sprites_walls, board)
        elif num == 2:
            Wall_place(all_sprites_walls, board, 'walls_x2', 'walls_y2')
        # выбор поля в зависимости от раунда
        ans = {}
        Quest_place()
        # размещение вопросов и создание словаря для них
        x_first_h, y_first_h, size_first_h = b[0] + 20, b[1] + 15, b[2] - 35
        hero = Hero(x_first_h, y_first_h, size_first_h)
        x_first_e, y_first_e, size_first_e = b[0] + (b[2] * (b[3] - 1)) + 20, b[1] + (b[2] * (b[4] - 1)) + 15, b[2] - 35
        evil = Evil(x_first_e, y_first_e, size_first_e)
        # задание изначальных координат героя и минотавра
        evil_move = 0
        # счётчик ходов минотавра(т.к. он ходит 2 раза подряд)
        running = True
        clock = pygame.time.Clock()
        direction = None
        player = 0
        # определяет текущего игрока; 0 - герой, 1 - минотавр
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
                        # определение направления по нажатой кнопке; учитывается нажатие только во время хода героя
                        x_coord, y_coord = hero.get_coords()[0], hero.get_coords()[1]
                        x_coord2, y_coord2 = board.get_cell((x_coord, y_coord), direction)
                        hero.aim(x_coord2, y_coord2)
                        # с помощью функции класса Board определяются координаты, к которым движется герой, и
                        # передаются в соответствующую функцию данного класса
            fon = pygame.transform.scale(load_image('floor.png'), (width, height))
            screen.blit(fon, (0, 0))
            font = pygame.font.Font(None, 120)
            # создание фона
            intro_text = [f"   {count_quests}           {min_ans}            20"]
            Transform_image('right.png', 110, 10, 90, 90, all_sprites_ans_labels)
            Transform_image('next.png', 720, 10, 80, 80, all_sprites_ans_labels)
            Transform_image('min_speed.png', 400, 10, 80, 80, all_sprites_ans_labels)
            # создание значков для отображения количества правильных, неправильных и необходимых для перехода
            # на следующий уровень ответов
            text_coord = 10
            for line in intro_text:
                string_rendered = font.render(line, 1, pygame.Color('red'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 120
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
            # вывод значений для каждого значка
            if player == 0:
                # если ходит герой
                hero.movement()
                player = hero.next()
                # проверка, завершил ли свой ход герой; если да, ход переходит к минотавру
                if player == 1:
                    evil_move = 1
                    evil.go()
            else:
                evil.movement()
                player = evil.next()
                if player == 0 and evil.stop() and evil_move != 0:
                    # если минотавр походил меньше чем 2 раза, повторить действие(засчитав ход)
                    player = 1
                    evil_move -= 1
                    evil.go()

            board.render(screen)
            all_sprites_walls.draw(screen)
            all_sprites_quests.draw(screen)
            all_sprites_hero.draw(screen)
            all_sprites_evil.draw(screen)
            all_sprites_ans_labels.draw(screen)
            # вывод всех изображений так, чтобы они не закрывали друг друга
            hero.update()
            hero.update_quest()
            # проверка на столкновение героя со стенками или с вопросом
            if hero.catched():
                # если герой столкнулся с минотавром вывести дисплей проигрыша
                min_win()
            if hero.win():
                # если герой вышел за пределы поля: проверить уровень; в зависимости от проходного балла на текущем
                # уровне вывести либо дисплей победы, либо недостаточного количества баллов
                if num == 1:
                    if count_quests < 20:
                        no_win()
                    else:
                        hero_win()
                elif num == 2:
                    if count_quests < 40:
                        no_win()
                    else:
                        # в случае победы на последнем уровне вывести финальный дисплей
                        fin_win()
            clock.tick(fps)
            pygame.display.flip()
        terminate()


    hello()
    #  запустить дисплей приветствия
pygame.quit()
