# import
import pygame
from random import randint

#Классы
class Button():

    # инициализация переменных у кнопки
    def __init__(self, x, y, image, s_image, scale):
        height = image.get_height()
        width = image.get_width()
        s_height = s_image.get_height()
        s_width =s_image.get_width()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.s_image = pygame.transform.scale(s_image, (int(s_width * scale), int(s_height * scale)))
        self.s_rect = self.s_image.get_rect()
        self.rect.center = (x, y)
        self.s_rect.center = (x, y)
        self.clicked = False

    # функция отрисовки кнопки и возвращения значения True если на кнопку нажали
    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        if self.rect.collidepoint(pos):
            surface.blit(self.s_image, (self.s_rect.x, self.s_rect.y))
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

# Начальные значения и глобальные переменные
H = 1000
W = 1300
pygame.init()
win = pygame.display.set_mode((W, H))  # Разрешение окна
pygame.display.set_caption("Домино")  # Название окна
tiles_base = [[], [], [], []]
tiles_play = []
tile_chain = []
settings = False
game_start = False
bot_count = 1
active_player = 0
active_tail = []
tile_position = [[615, 185, 90], [550, 185, 90], [485, 185, 90], [420, 185, 90], [405, 235, 0], [405, 300, 0],
                 [405, 365, 0], [405, 430, 0], [405, 495, 0], [405, 560, 0], [405, 625, 0], [420, 675, 270],
                 [485, 675, 270], [550, 675, 270], [615, 675, 270], [680, 675, 270], [745, 675, 270], [810, 675, 270],
                 [875, 675, 270], [890, 625, 180], [890, 560, 180], [890, 495, 180], [890, 430, 180], [890, 365, 180],
                 [890, 300, 180], [890, 235, 180], [875, 185, 90], [810, 185, 90], [745, 185, 90], [680, 185, 90]]
places = []
win_func = False

# подгрузка изображений
back_img = pygame.transform.scale(pygame.image.load("images/back.jpg"), (W, H))
s_back_img = pygame.transform.scale(pygame.image.load("images/s_back.png"), (600, 300))
start_img = pygame.image.load("images/start.png")
s_start_img = pygame.image.load("images/s_start.png")
quit_img = pygame.image.load("images/quit.png")
s_quit_img = pygame.image.load("images/s_quit.png")
cancel_img = pygame.image.load("images/cancel.png")
s_cancel_img = pygame.image.load("images/s_cancel.png")
bot_count_img = pygame.transform.scale(pygame.image.load("images/bot_count.png"), (600, 250))
arrow_img = pygame.image.load("images/arrow.png")
s_arrow_img = pygame.image.load("images/s_arrow.png")
start_1_img = pygame.image.load("images/start_1.png")
s_start_1_img = pygame.image.load("images/s_start_1.png")
border_img = pygame.image.load("images/border.png")
tile_back_img = pygame.image.load("images/tile_back.png")
green_img = pygame.image.load("images/green.png")
red_img = pygame.image.load("images/red.png")
skip_img = pygame.image.load("images/skip.png")
rank_img = pygame.transform.scale(pygame.image.load("images/rank.png"), (600, 300))

# создание кнопок
start_button = Button(650, 600, start_img, s_start_img, 1.75)
quit_button = Button(650, 800, quit_img, s_quit_img, 1.75)
cancel_button = Button(650, 800, cancel_img, s_cancel_img, 1.75)
arrow_button_up = Button(740, 135, arrow_img, s_arrow_img, 1)
arrow_button_down = Button(755, 310, pygame.transform.rotate(arrow_img, 180),
                                  pygame.transform.rotate(s_arrow_img, 180), 1)
s_start_button = Button(400, 400, start_1_img, s_start_1_img, 1.75)
cancel_button_1 = Button(1070, 65, cancel_img, s_cancel_img, 0.7)
bazar_button = Button(1160, 930, tile_back_img, pygame.transform.scale(tile_back_img, (36, 72)), 2)
skip_button = Button(1020, 940, skip_img, pygame.transform.scale(skip_img, (40, 40)), 2)
cancel_button_2 = Button(650, 900, cancel_img, s_cancel_img, 1.2)

# функции
font_name = pygame.font.match_font('arial')  # выбор типа шрифта
# прорисовка текста желаемого размера в позиции x,y
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (60, 60, 60))
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)


# функция отображения домино у игрока а так же рассчет возможности и самого хода у выбранной доминошки
def draw_tile(surface, tile, x, y, scale):
    # Отрисовка домино игрока
    global active_player
    global tile_chain
    global active_tail
    tile_up = pygame.transform.scale(pygame.image.load("images/tile_" + str(tile[0]) + ".png"),
                                     (int(30 * scale), int(30 * scale)))
    tile_down = pygame.transform.scale(pygame.image.load("images/tile_" + str(tile[1]) + ".png"),
                                       (int(30 * scale), int(30 * scale)))
    tile_up_rect = tile_up.get_rect()
    tile_down_rect = tile_down.get_rect()
    tile_up_rect.midbottom = (x, y)
    tile_down_rect.midtop = (x, y)
    pos = pygame.mouse.get_pos()
    if tile_up_rect.collidepoint(pos) or tile_down_rect.collidepoint(pos) or active_tail == [tile[0], tile[1]]:
        surface.blit(
            pygame.transform.scale(tile_up, (int(tile_up.get_width() * 1.15), int(tile_up.get_height() * 1.15))),
            tile_up_rect)
        surface.blit(
            pygame.transform.scale(tile_down, (int(tile_down.get_width() * 1.15), int(tile_down.get_height() * 1.15))),
            tile_down_rect)
    else:
        surface.blit(tile_up, tile_up_rect)
        surface.blit(tile_down, tile_down_rect)

    # Функции домино игрока
    if active_player == 0:
        if tile_up_rect.collidepoint(pos) or tile_down_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                active_tail = [tile[0], tile[1]]
        if active_tail != []:

            # Если ход первый у игрока, первый ход можно сделать только самым большим дублем
            if tile_chain == []:
                green_img_rect = green_img.get_rect()
                green_img_rect.center = (tile_position[0][0], tile_position[0][1])
                b=0
                for i in tiles_base[active_player]:
                    if i[0]==i[1] and (i[0]+i[1])>b:
                        b=i[0]+i[1]
                if active_tail[0]==active_tail[1] and b == (active_tail[0]+active_tail[1]):
                    if green_img_rect.collidepoint(pos):
                        surface.blit(
                            pygame.transform.scale(green_img,
                                                   (int(green_img.get_width() * 1.30), int(green_img.get_height() * 1.30))),
                            green_img_rect)
                    else:
                        surface.blit(green_img, green_img_rect)
                    if green_img_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
                        active_player += 1
                        pygame.time.delay(300)
                        tile_chain.append([active_tail[0], active_tail[1]])
                        for tile11 in range(len(tiles_base[0])):
                            if tiles_base[0][tile11][0] == active_tail[0] and tiles_base[0][tile11][1] == active_tail[1]:
                                tiles_base[0].pop(tile11)
                                break
                        draw_tile_chain(win, tile_chain)
                        draw_tiles(win, tiles_base[0], 66, 938, 1.5)
                        pygame.display.update()
                        pygame.time.delay(500)
                        active_tail = []
                else:
                    red_img_rect = red_img.get_rect()
                    red_img_rect.center = (tile_position[0][0], tile_position[0][1])
                    surface.blit(red_img, red_img_rect)

            # Если уже добавлять к имеющимся
            else:

                # Если с начала добавить
                if active_tail[0] == tile_chain[0][0] or active_tail[1] == tile_chain[0][0]:
                    green_img_rect = green_img.get_rect()
                    green_img_rect.center = (tile_position[0][0], tile_position[0][1])
                    if green_img_rect.collidepoint(pos):
                        surface.blit(
                            pygame.transform.scale(green_img,
                                                   (int(green_img.get_width() * 1.30),
                                                    int(green_img.get_height() * 1.30))),
                            green_img_rect)
                    else:
                        surface.blit(green_img, green_img_rect)
                    if green_img_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
                        active_player += 1
                        pygame.time.delay(300)
                        if active_tail[0] == tile_chain[0][0]:
                            tile_chain.insert(0, [active_tail[1], active_tail[0]])
                        elif active_tail[1] == tile_chain[0][0]:
                            tile_chain.insert(0, [active_tail[0], active_tail[1]])
                        for tile11 in range(len(tiles_base[0])):
                            if tiles_base[0][tile11][0] == active_tail[0] and tiles_base[0][tile11][1] == \
                                    active_tail[1]:
                                tiles_base[0].pop(tile11)
                                break
                        draw_tile_chain(win, tile_chain)
                        draw_tiles(win, tiles_base[0], 66, 938, 1.5)
                        pygame.display.update()
                        pygame.time.delay(500)
                else:
                    red_img_rect = red_img.get_rect()
                    red_img_rect.center = (tile_position[0][0], tile_position[0][1])
                    surface.blit(red_img, red_img_rect)

                # Если с конца можно добавить
                if active_tail[0] == tile_chain[-1][1] or active_tail[1] == tile_chain[-1][1]:
                    green_img_rect_1 = green_img.get_rect()
                    green_img_rect_1.center = (
                        tile_position[len(tile_chain) + 1][0], tile_position[len(tile_chain) + 1][1])
                    if green_img_rect_1.collidepoint(pos):
                        surface.blit(
                            pygame.transform.scale(green_img,
                                                   (int(green_img.get_width() * 1.30),
                                                    int(green_img.get_height() * 1.30))),
                            green_img_rect_1)
                    else:
                        surface.blit(green_img, green_img_rect_1)
                    if green_img_rect_1.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
                        active_player += 1
                        pygame.time.delay(300)
                        if active_tail[0] == tile_chain[-1][1]:
                            tile_chain.append([active_tail[0], active_tail[1]])
                        elif active_tail[1] == tile_chain[-1][1]:
                            tile_chain.append([active_tail[1], active_tail[0]])
                        for tile11 in range(len(tiles_base[0])):
                            if tiles_base[0][tile11][0] == active_tail[0] and tiles_base[0][tile11][1] == \
                                    active_tail[1]:
                                tiles_base[0].pop(tile11)
                                break
                        draw_tile_chain(win, tile_chain)
                        draw_tiles(win, tiles_base[0], 66, 938, 1.5)
                        pygame.display.update()
                        pygame.time.delay(500)
                else:
                    red_img_rect = red_img.get_rect()
                    red_img_rect.center = (tile_position[len(tile_chain) + 1][0], tile_position[len(tile_chain) + 1][1])
                    surface.blit(red_img, red_img_rect)


# мини функция которая в цикле отправляет по очереди каждую домино у игрока в функцию draw_tile
def draw_tiles(surface, tiles, x, y, scale):
    b = -1
    for tile in tiles:
        b += 1
        draw_tile(surface, tile, x + b * 35 * scale, y, scale)


# функция отрисовки домино у бота
def draw_tiles_bots(surface, tiles, x, y, scale, rotate):
    b = 0
    c = 0
    if rotate == 0:
        b = -1
    else:
        c = -1
    for tile in tiles:
        if rotate == 0:
            b += 1
        else:
            c += 1
        surface.blit(
            pygame.transform.rotate(pygame.transform.scale(tile_back_img, (int(30 * scale), int(60 * scale))), rotate),
            (x + b * 35 * scale, y + 35 * c * scale))


# отрисовка домино находящегося на игровом столе
def draw_tile_chain(surface, tile_chain):
    for tile in range(len(tile_chain)):
        tile_up = pygame.transform.rotate(pygame.image.load("images/tile_" + str(tile_chain[tile][0]) + ".png"),
                                          tile_position[tile + 1][2])
        tile_down = pygame.transform.rotate(pygame.image.load("images/tile_" + str(tile_chain[tile][1]) + ".png"),
                                            tile_position[tile + 1][2])
        tile_up_rect = tile_up.get_rect()
        tile_down_rect = tile_down.get_rect()
        if tile_position[tile + 1][2] == 0:
            tile_up_rect.midbottom = (tile_position[tile + 1][0], tile_position[tile + 1][1])
            tile_down_rect.midtop = (tile_position[tile + 1][0], tile_position[tile + 1][1])
        elif tile_position[tile + 1][2] == 90:
            tile_up_rect.midleft = (tile_position[tile + 1][0], tile_position[tile + 1][1])
            tile_down_rect.midright = (tile_position[tile + 1][0], tile_position[tile + 1][1])
        elif tile_position[tile + 1][2] == 180:
            tile_up_rect.midtop = (tile_position[tile + 1][0], tile_position[tile + 1][1])
            tile_down_rect.midbottom = (tile_position[tile + 1][0], tile_position[tile + 1][1])
        elif tile_position[tile + 1][2] == 270:
            tile_up_rect.midright = (tile_position[tile + 1][0], tile_position[tile + 1][1])
            tile_down_rect.midleft = (tile_position[tile + 1][0], tile_position[tile + 1][1])
        surface.blit(tile_up, tile_up_rect)
        surface.blit(tile_down, tile_down_rect)


# функция добирания домино из колоды(базара) при необходимости
def bazar():
    global active_player
    global tiles_play
    global tiles_base
    if len(tiles_play) > 0:
        tile_luck = int(randint(0, len(tiles_play) - 1))
        tiles_base[active_player] += [tiles_play[tile_luck]]
        tiles_play.pop(tile_luck)


# функция хода ботов
def bot_move():
    global active_player
    global tiles_base
    global tile_chain
    tile_hod = -1

    # если самый первый ходу у бота, ставит дубль с самым большим количеством очков
    if len(tile_chain) == 0:
        pygame.time.delay(1000)
        b = 0
        tile_hod = -1
        for tile in range(len(tiles_base[active_player])):
            if (tiles_base[active_player][tile][0] + tiles_base[active_player][tile][1] > b) and (
                    tiles_base[active_player][tile][0] == tiles_base[active_player][tile][1]):
                b = tiles_base[active_player][tile][0] + tiles_base[active_player][tile][1]
                tile_hod = tile
        tile_chain += [tiles_base[active_player][tile_hod]]
        tiles_base[active_player].pop(tile_hod)
        active_player = (active_player + 1) % (bot_count + 1)

    # если добавлять то выбирает самую большую домино по очкам и ставит сначала с начала, или в конце по доступности
    else:
        tile_hod = -1
        while tile_hod == -1:
            b = 0
            for tile in range(len(tiles_base[active_player])):
                if (tile_chain[0][0] == tiles_base[active_player][tile][0]
                    or tile_chain[0][0] == tiles_base[active_player][tile][1]
                    or tile_chain[-1][1] == tiles_base[active_player][tile][0]
                    or tile_chain[-1][1] == tiles_base[active_player][tile][1]) and (
                        (tiles_base[active_player][tile][0] + tiles_base[active_player][tile][1]) > b):
                    b = tiles_base[active_player][tile][0] + tiles_base[active_player][tile][1]
                    tile_hod = tile
            if tile_hod == -1:

                # берет из базара если не нашлось подходящей
                bazar()
                if len(tiles_play) == 0:
                    tile_hod = -2  # показывает что базар пуст и домино нет подходящей, означает что бот пропускает ход
                draw_text(win, str("X" + str(len(tiles_play))), 50, 1250, 960)
                draw_tiles_bots(win, tiles_base[active_player], 190, 20, 1.5, 0)
                pygame.display.update()
                pygame.time.delay(1000)
        if tile_hod != -2:
            if tiles_base[active_player][tile_hod][0] == tile_chain[0][0]:
                tile_chain.insert(0, [tiles_base[active_player][tile_hod][1], tiles_base[active_player][tile_hod][0]])
            elif tiles_base[active_player][tile_hod][1] == tile_chain[0][0]:
                tile_chain.insert(0, [tiles_base[active_player][tile_hod][0], tiles_base[active_player][tile_hod][1]])
            elif tiles_base[active_player][tile_hod][0] == tile_chain[-1][1]:
                tile_chain.append([tiles_base[active_player][tile_hod][0], tiles_base[active_player][tile_hod][1]])
            elif tiles_base[active_player][tile_hod][1] == tile_chain[-1][1]:
                tile_chain.append([tiles_base[active_player][tile_hod][1], tiles_base[active_player][tile_hod][0]])
            tiles_base[active_player].pop(tile_hod)
            draw_tile_chain(win, tile_chain)
            draw_tiles_bots(win, tiles_base[active_player], 190, 20, 1.5, 0)
            pygame.display.update()
        active_player = (active_player + 1) % (bot_count + 1)


# функция проверки конца игры, если кто либо выдал все домино или игра не может продолжатся, тк у игроков не осталось доступных ходов
def win_func1():
    global win_func
    for i in range(bot_count + 1):
        if len(tiles_base[i]) == 0:
            win_func = True
    if len(tiles_play) == 0 and tile_chain != []:
        b = 1
        for i in range(bot_count + 1):
            for y in tiles_base[i]:
                if y[0] == tile_chain[0][0] or y[1] == tile_chain[0][0] or y[0] == tile_chain[-1][1] or y[1] == \
                        tile_chain[-1][1]:
                    b = 0
        if b == 1:
            win_func = True


# простая функция надписи показывающая кто ходит
def log():
    if active_player != 0:
        draw_text(win, "Ходит бот №" + str(active_player), 30, 250, 800)
    else:
        draw_text(win, "Ваш ход!", 30, 250, 800)


# считает суммарные очки у указаного игрока в конце игры
def points(tiles):
    b = 0
    for i in tiles:
        b = b + i[0] + i[1]
    return b


# Начало цикла приложения
run = True  # Отвечает за работу основного цикла, False для закрытия приложения
while run:

    # цикл проверки евентов в приложении, позволяет закрыть приложение без зависаний, и показывает что приложение "отвечает"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    win.blit(back_img, (0, 0))

    # начальный экран
    if settings == False and game_start == False:
        win.blit(s_back_img, (350, 100))
        if start_button.draw(win) == True:
            settings = True
        if quit_button.draw(win) == True:
            run = False

    # экран настроек с выбором колва ботов и задание начальных значений для будующей игры
    if settings == True and game_start == False:
        win.blit(bot_count_img, (100, 100))
        if cancel_button.draw(win) == True:
            settings = False
            pygame.time.delay(200)
        if arrow_button_up.draw(win) == True:
            bot_count += 1
            if bot_count == 4:
                bot_count = 1
            pygame.time.delay(200)
        if arrow_button_down.draw(win) == True:
            bot_count -= 1
            if bot_count == 0:
                bot_count = 3
            pygame.time.delay(200)

        # при нажатии кнопки определяется домино у игроков и ботов, идет выбор первого игрока по принципу у кого больший дубль
        if s_start_button.draw(win) == True:
            game_start = True
            tiles_play = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 1], [1, 2], [1, 3], [1, 4],
                          [1, 5], [1, 6], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [3, 3], [3, 4], [3, 5], [3, 6],
                          [4, 4], [4, 5], [4, 6], [5, 5], [5, 6], [6, 6]]
            tiles_base = [[], [], [], []]
            active_player = 0
            tile_chain = []

            # Раздача домино игрокам
            for tile in range(7):
                if bot_count >= 1:
                    tile_luck = int(randint(0, len(tiles_play) - 1))
                    tiles_base[0] += [tiles_play[tile_luck]]
                    tiles_play.pop(tile_luck)
                    tile_luck = int(randint(0, len(tiles_play) - 1))
                    tiles_base[1] += [tiles_play[tile_luck]]
                    tiles_play.pop(tile_luck)
                if bot_count >= 2:
                    tile_luck = int(randint(0, len(tiles_play) - 1))
                    tiles_base[2] += [tiles_play[tile_luck]]
                    tiles_play.pop(tile_luck)
                if bot_count >= 3:
                    tile_luck = int(randint(0, len(tiles_play) - 1))
                    tiles_base[3] += [tiles_play[tile_luck]]
                    tiles_play.pop(tile_luck)

            # Нахождение первого игрока
            biggest = [0, 0, 0, 0]
            for tile in range(7):
                if bot_count >= 1:
                    if tiles_base[0][tile][0] == tiles_base[0][tile][1] and tiles_base[0][tile][0] + \
                            tiles_base[0][tile][1] > biggest[0]:
                        biggest[0] = tiles_base[0][tile][0] + tiles_base[0][tile][1]
                    if tiles_base[1][tile][0] == tiles_base[1][tile][1] and tiles_base[1][tile][0] + \
                            tiles_base[1][tile][1] > biggest[1]:
                        biggest[1] = tiles_base[1][tile][0] + tiles_base[1][tile][1]
                if bot_count >= 2:
                    if tiles_base[2][tile][0] == tiles_base[2][tile][1] and tiles_base[2][tile][0] + \
                            tiles_base[2][tile][1] > biggest[2]:
                        biggest[2] = tiles_base[2][tile][0] + tiles_base[2][tile][1]
                if bot_count >= 3:
                    if tiles_base[3][tile][0] == tiles_base[3][tile][1] and tiles_base[3][tile][0] + \
                            tiles_base[3][tile][1] > biggest[3]:
                        biggest[3] = tiles_base[3][tile][0] + tiles_base[3][tile][1]
            b = 0
            for i in range(4):
                if biggest[i] > b:
                    b = biggest[i]
                    active_player = i
        draw_text(win, str(bot_count), 70, 740, 225)

    # игровое окно
    if settings == True and game_start == True and win_func != True:

        # Разметка игрового стола
        win.blit(back_img, (0, 0))
        win.blit(pygame.transform.scale(border_img, (1100, 150)), (0, 850))
        win.blit(pygame.transform.scale(border_img, (200, 150)), (1100, 850))
        win.blit(pygame.transform.rotate(pygame.transform.scale(border_img, (850, 150)), 180), (150, 0))
        win.blit(pygame.transform.rotate(pygame.transform.scale(border_img, (150, 150)), 180), (1000, 0))
        win.blit(pygame.transform.rotate(pygame.transform.scale(border_img, (850, 150)), 90), (1150, 0))
        win.blit(pygame.transform.rotate(pygame.transform.scale(border_img, (850, 150)), -90), (0, 0))
        draw_text(win, str("X" + str(len(tiles_play))), 50, 1250, 960)
        draw_tile_chain(win, tile_chain)
        draw_tiles_bots(win, tiles_base[1], 190, 20, 1.5, 0)
        if bot_count >= 2:
            draw_tiles_bots(win, tiles_base[2], 20, 40, 1.5, 90)
        if bot_count >= 3:
            draw_tiles_bots(win, tiles_base[3], 1180, 40, 1.5, 90)

        # кнопки
        if bazar_button.draw(win) == True and active_player == 0:
            bazar()
            draw_text(win, str("X" + str(len(tiles_play))), 50, 1250, 960)
        if cancel_button_1.draw(win) == True:
            game_start = False
            pygame.time.delay(200)
        if skip_button.draw(win) == True:
            active_player = (active_player + 1) % (bot_count + 1)
            pygame.time.delay(500)
        win_func1()
        draw_tiles(win, tiles_base[0], 66, 938, 1.5)
        if active_player != 0:
            log()
            win_func1()
            pygame.display.update()
            active_tail = []
            pygame.time.delay(1000)
            bot_move()
        log()

    # окно с статистикой игры и занятами местами, кнопка возвращает в меню настроек
    if win_func == True:
        draw_text(win, "Игра закончена!", 50, 650, 200)
        win.blit(rank_img, (360, 380))
        v = []
        for i in range(bot_count + 1):
            if i == 0:
                v.append([points(tiles_base[i]), "Вы"])
            else:
                v.append([points(tiles_base[i]), "Бот №" + str(i)])
            if i == 0:
                draw_text(win, "У вас осталось домино на " + str(points(tiles_base[i])) + " очков", 30, 650,
                          700 + 40 * (i + 1))
            else:
                draw_text(win, "У бота №" + str(i) + " осталось домино на " + str(points(tiles_base[i])) + " очков", 30,
                          650, 700 + 40 * (i + 1))
        v.sort()
        for i in range(bot_count + 1):
            if i == 0:
                draw_text(win, str(v[i][1]), 30, 640, 410)
            if i == 1:
                draw_text(win, str(v[i][1]), 30, 525, 480)
            if i == 2:
                draw_text(win, str(v[i][1]), 30, 750, 550)
            if i == 3:
                draw_text(win, str(v[i][1]), 30, 900, 640)
        if cancel_button_2.draw(win) == True:
            win_func = False
            game_start = False
            pygame.time.delay(500)
    pygame.display.update()

# закрыть приложение точно
pygame.quit()
