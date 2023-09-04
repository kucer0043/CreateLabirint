import copy
import time
from ctypes import *

import pygame

from color import *
from e_socket import *
from enit import *
from files.modules import editor
from gui import *


# оснoвной файл игры
def resource_path(relative_path):  # нужно для компиляции а ЕХЕ фыйл
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


pygame.init()
size_screen = [windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)]  # берём размер экрана
dev = 0
play = 0

def screen_real_resolution(size):  # делаем карту квадратной по наименьшей стороне экрана
    x_old, y_old = size
    x_new = y_new = 0
    for y in range(0, y_old, 100):
        if y_old > y:
            y_new = y
            print(f'{y_new} y')

    for x in range(0, x_old, 100):
        if y_old > x:
            x_new = x
            print(f'{x_new} x')
    if x_old == y_old:
        x_new += 100
        y_new += 100
    return [x_new, y_new]


# разделяет строчку соообщения на список из строк
def decode(text: str):
    message = []
    val = 0
    for letter in range(len(text)):
        if text[letter] != ' ':
            if len(message) == val:
                message.append(text[letter])
            else:
                message[val] += text[letter]
        else:
            message.append('')
            val += 1
    return message


# высчитвает коодинаты для текста меню
def get_coords(text, x=1.0, y=1.0):
    return (size_screen[0] / 2 * x - text.get_width() / 2), (size_screen[1] / 2 * y - text.get_height() / 2)


def get_coords_rect(size: (int, int), x=1.0, y=1.0):
    return (size_screen[0] / 2 * x - size[0] / 2), (size_screen[1] / 2 * y - size[1] / 2), size[0], size[1]


def change_coordinates(old_coordinates):
    old_rect_x, old_rect_y = H_W_rect(org_size_screen)
    return old_coordinates[0] // old_rect_x * rect_x_end, old_coordinates[1] // old_rect_y * rect_y_end


size_screen = screen_real_resolution(size_screen)
org_size_screen = copy.copy(size_screen)
screen = pygame.display.set_mode(size_screen, pygame.RESIZABLE)
rect_x_end, rect_y_end = H_W_rect(size_screen)
font = pygame.font.Font(resource_path("files/fonts/better-vcr_0.ttf"), (rect_x_end + rect_y_end) // 2)
font_small = pygame.font.Font(resource_path("files/fonts/better-vcr_0.ttf"), (rect_x_end + rect_y_end) // 2 // 2)
print(rect_x_end, rect_y_end)
clock = pygame.time.Clock()
bg_color = Gray
# ip = get_lan_ip()
ip = ""
menu_text_1 = font.render('Текст заглушка', True, White)
menu_text_2 = font.render('Текст заглушка', True, White)
menu_text_3 = font.render('Текст заглушка', True, White)
menu_text_4 = font.render('Текст заглушка', True, White)
lobby_text = font.render('Текст заглушка', True, White)

pygame.display.set_caption(f"by kucer0043 Labirint ip:{ip}")
text_disconnect = font.render('Подключение разорвано', True, White)
game_type = str('None')


def disconnect_action():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill((128, 128, 128))
        screen.blit(text_disconnect, get_coords(text_disconnect))
        pygame.display.update()
    pass


# функция отбражения меню
def menu():
    global game_type, play, rect_x_end, rect_y_end, size_screen, font
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_type = '1'
                    running = False
                if event.key == pygame.K_2:
                    game_type = '2'
                    running = False
                if event.key == pygame.K_e:
                    editor.load_map_editor(screen, size_screen)
                if event.key == pygame.K_q:
                    play = 1
                    game_type = 'dev'
                    running = False
            if event.type == pygame.VIDEORESIZE:
                size_screen[0] = event.w
                size_screen[1] = event.h
                rect_x_end, rect_y_end = H_W_rect(size_screen)
                reload_text()
        screen.fill(Gray)
        screen.blit(menu_text_1, get_coords(menu_text_1, y=10))
        screen.blit(menu_text_2, get_coords(menu_text_2, y=80))
        # screen.blit(menu_text_5, get_text_coords(menu_text_5, y=150))  # добавление Нового пункта меню
        pygame.display.update()
        '''game_type = '3'
        running = False'''
    return


def lobby():
    global rect_x_end, rect_y_end, font
    running = True
    while running:
        screen.fill((128, 128, 128))
        screen.blit(lobby_text, get_coords(lobby_text, y=0.5))
        Rect(screen, get_coords_rect(change_coordinates((500, 400)), x=0.7)).draw()
        create_game_butt = Button(screen, get_coords_rect(change_coordinates((100, 100)), x=1.5), "Host",
                                  (255, 255, 255), font_small, color_text=(0, 0, 0))
        create_game_butt.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.VIDEORESIZE:
                size_screen[0] = event.w
                size_screen[1] = event.h
                rect_x_end, rect_y_end = H_W_rect(size_screen)
                reload_text()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if create_game_butt.is_clicked(pygame.mouse.get_pos()):
                    print('LOL')

        pygame.display.update()

def reload_text():
    global menu_text_1, menu_text_2, menu_text_3, menu_text_4, lobby_text, font
    font = pygame.font.Font(resource_path("files/fonts/better-vcr_0.ttf"), (rect_x_end + rect_y_end) // 2)
    menu_text_1 = font.render('Нажмите 1 для создания лобби', True, White)
    menu_text_2 = font.render('Нажмите 2 для клиента', True, White)
    menu_text_3 = font.render('Запустите 2 клиент', True, White)
    menu_text_4 = font.render('Не найдено сервера - Переподключение', True, White)
    lobby_text = font.render('Лобби', True, White)


reload_text()
if dev == 0:
    menu()
    screen.fill((128, 128, 128))
    screen.blit(menu_text_3, get_coords(menu_text_3))
    pygame.display.update()
    if game_type == 'dev':
        dev = 1
        play = 1
        print('Вы в режиме разработчика')
    elif dev == 0:
        if game_type == '2':
            ip_adress = find_local_servers()
            e_socket = multiplayer_socket(ip_adress[0], ip_adress[1], game_type)
            '''try:
                e_socket = multiplayer_socket('localhost', 8080, type)
            except ConnectionRefusedError:
                running = True
                while running:
                    screen.fill(Gray)
                    screen.blit(menu_text_4, get_text_coords(menu_text_1))
                    pygame.display.update()
                    time.sleep(1)
                    ip = input('ip\n>> ')
                    try:
                        e_socket = multiplayer_socket(ip, 8080, type)
                        running = False
                    except:
                        running = True'''

        elif game_type == '1':
            # ip = input('set ip\n>> ')
            # e_socket = multiplayer_socket(input('ip\n>> '), 8080, type)
            e_socket = multiplayer_socket(ip, 8085, game_type, action_on_disconnect=disconnect_action)
        elif game_type == '3':  # Добавление Реакции на кнопку открытия окна с подсказаками
            lobby()
        else:
            print(game_type)
            raise ValueError("Invalid Input")
players = [player(rect_x_end, rect_y_end, White, 0, 0) for i in range(1)]
bg_c1 = bg_c2 = bg_c3 = 0
end_x = -1
end_y = -1


# функция отключена
def respawn():
    players[0].x = 0
    players[0].y = 0


wait_text = font.render('Ожидание противника', True, White)

yes_continue = 0
# основной цикл игры
while True:
    if play == 0:
        data = None
        map_data = editor.load_map_editor(screen, size_screen)
        map_send = map_data[0]
        run_check_map = True
        spawn_x, spawn_y = map_data[2]
        end_x_check, end_y_check = map_data[3]
        players[0].x, players[0].y = (spawn_x * rect_x_end, spawn_y * rect_y_end)
        while run_check_map:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        players[0].move('UP', map_send)
                    if event.key == pygame.K_s:
                        players[0].move('DOWN', map_send)
                    if event.key == pygame.K_a:
                        players[0].move('LEFT', map_send)
                    if event.key == pygame.K_d:
                        players[0].move('RIGHT', map_send)
                    if event.key == pygame.K_q:
                        data = None
                        map_data = editor.load_map_editor(screen, size_screen, map_input=map_send)
                        map_send = map_data[0]
                        run_check_map = True
                        spawn_x, spawn_y = map_data[2]
                        end_x_check, end_y_check = map_data[3]
                        players[0].x, players[0].y = (spawn_x * rect_x_end, spawn_y * rect_y_end)
                if event.type == pygame.VIDEORESIZE:
                    size_screen[0] = event.w
                    size_screen[1] = event.h
                    rect_x_end, rect_y_end = H_W_rect(size_screen)
                    reload_text()
            screen.fill(map_data[1])
            for y in range(len(map_send)):
                for x in range(len(map_send[y])):
                    if map_send[y][x] == 1:
                        pygame.draw.rect(screen, (0, 0, 0),
                                         (x * rect_x_end, y * rect_y_end, rect_x_end, rect_y_end))
                    if map_send[y][x] == 2:
                        pygame.draw.rect(screen, (255, 0, 0),
                                         (x * rect_x_end, y * rect_y_end, rect_x_end, rect_y_end))
                    if map_send[y][x] == 3:
                        pygame.draw.rect(screen, (0, 0, 255),
                                         (x * rect_x_end, y * rect_y_end, rect_x_end, rect_y_end))

            for p in players:
                pygame.draw.rect(screen, p.color, (p.x, p.y, rect_x_end, rect_y_end))
            pygame.display.update()
            if int(players[0].x / rect_x_end) == end_x_check and int(players[0].y / rect_y_end) == end_y_check:
                run_check_map = False
                print("Ожидание игрока")
        screen.fill(bg_color)
        screen.blit(wait_text,
                    (size_screen[0] / 2 - wait_text.get_width() / 2, size_screen[1] / 2 - wait_text.get_height() / 2))
        pygame.display.update()
        for y in range(len(map_send)):
            for x in range(len(map_send[y])):
                e_socket.data = f'm {map_send[y][x]} {x} {y}'
                data = e_socket.update()
                data = decode(data)
                if data[0] == 'm':
                    # print(f'Получена карта {data[2]} {data[3]} {data}')
                    try:
                        map[int(data[3])][int(data[2])] = int(data[1])
                    except ValueError:
                        # print('Дублирована отправка исправление')
                        map[y][int(data[2])] = int(data[1])
                        map[int(data[6])][int(data[5])] = int(data[4])
                    # bg_color = data[1]
                if map[y][x] == 2:
                    players[0].x = x * rect_x_end
                    players[0].y = y * rect_y_end
                    spawn_x_run = x
                    spawn_y_run = y
                if map[y][x] == 3:
                    end_x = x
                    end_y = y

        bg_send = map_data[1]
        for i in range(0, 3):
            e_socket.data = f'{bg_send[i]} {i}'
            bg_data = e_socket.update()
            print(bg_data)
            bg_data = decode(bg_data)
            if i == 0:
                bg_c1 = int(bg_data[0])
            if i == 1:
                bg_c2 = int(bg_data[0])
            if i == 2:
                try:
                    bg_c3 = int(bg_data[0])
                except:
                    bg_c3 = 128
        bg_color = (bg_c1, bg_c2, bg_c3)
        play = 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if play == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    players[0].move('UP')
                if event.key == pygame.K_s:
                    players[0].move('DOWN')
                if event.key == pygame.K_a:
                    players[0].move('LEFT')
                if event.key == pygame.K_d:
                    players[0].move('RIGHT')
                if event.key == pygame.K_q and dev == 1:
                    play = 0
            if event.type == pygame.VIDEORESIZE:
                size_screen[0] = event.w
                size_screen[1] = event.h
                rect_x_end, rect_y_end = H_W_rect(size_screen)
                reload_text()
    if play == 1:
        # e_socket.data = f'{players[0].x} {players[0].y}'
        screen.fill(bg_color)
        for y in range(len(map)):
            for x in range(len(map[y])):
                try:
                    if map[y][x] == 1:
                        pygame.draw.rect(screen, (0, 0, 0),
                                         (x * rect_x_end, y * rect_y_end, rect_x_end, rect_y_end))
                    if map[y][x] == 2:
                        pygame.draw.rect(screen, (255, 0, 0),
                                         (x * rect_x_end, y * rect_y_end, rect_x_end, rect_y_end))
                    if map[y][x] == 3:
                        pygame.draw.rect(screen, (0, 0, 255),
                                         (x * rect_x_end, y * rect_y_end, rect_x_end, rect_y_end))
                    if y == int(players[0].y / rect_y_end) and x == int(players[0].x / rect_x_end):
                        pygame.draw.rect(screen, White,
                                         (x * rect_x_end, y * rect_y_end, rect_x_end, rect_y_end))
                except IndexError:
                    # print('LIST INDEX OUT RANGE')
                    pass
        if int(players[0].x / rect_x_end) == end_x and int(players[0].y / rect_y_end) == end_y:
            screen.blit(font.render('Вы победили!', True, White),
                        get_coords(font.render('Вы победили!', True, White), 0, 0))
            pygame.display.update()
            if dev == 0:
                e_socket.data = f's'
                data = e_socket.update(0)
                play = 0
                time.sleep(1)
        else:
            if dev == 0:
                e_socket.data = f'{bg_data[0]}'
                data = e_socket.update()
                if data == f's':
                    screen.blit(font.render('Вы проиграли!', True, White), (
                        size_screen[0] / 2 - font.size('Вы проиграли!')[0] / 2,
                        size_screen[1] / 2 - font.size('Вы проиграли!')[1] / 2))
                    pygame.display.update()
                    time.sleep(1)  # :)
                    play = 0
    pygame.display.update()
