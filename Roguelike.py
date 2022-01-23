import csv

import pygame
import os, sys, random
import sqlite3


WIN_WIDTH = 1920
WIN_HEIGHT = 1000
FLOOR_COLOR = (102, 91, 60)
WALL_COLOR = (134, 143, 97)
DOOR_COLOR = (112, 72, 17)
MAX_BULLETS_ON_SRCEEN = 30
FPS = 60

pygame.init()
pygame.display.set_caption('Какой-то рогалик(типо айзека)')
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
running = True
ROOMCLEAR = True
NEWROOM = False
ROOMUPDATE = False
SPAWNMOBS = False
LEVELUPDATE = False
CURENTLEVEL = 1
POINTS = 0
game_over = False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением {fullname} не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Рогалик", "",
                  "Управление:",
                  "W, A, S, D - ходьба",
                  "Стрелки - стрельба",
                  "Цель игры - пройти все уровни как можно быстрее",
                  "Вашему прохождению будут мешать монстры, которые будут пытаться вас убить",
                  "А погут вам (не факт) предметы, которые могут появится после зачистки комнаты",
                  "Удачи :)"]

    fon = pygame.transform.scale(load_image('background.jpg'), (WIN_WIDTH, WIN_HEIGHT))
    screen.blit(fon, (100, 100))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def game_over_screen():
    if game_over:
        sprite = pygame.sprite.Sprite()
        im = load_image('gameover.png')
        sprite.image = pygame.transform.scale(im, (WIN_WIDTH, WIN_HEIGHT))
        sprites = pygame.sprite.Group()
        sprite.rect = sprite.image.get_rect()
        sprites.add(sprite)
        sprite.rect.x = -WIN_WIDTH
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return
            screen.fill((0, 0, 0))
            sprites.draw(screen)
            if sprite.rect.x != 0:
                sprite.rect.x += 480 // 30
            pygame.display.flip()
            clock.tick(FPS)
    elif CURENTLEVEL == 4:
        screen.fill((0, 0, 0))
        end_score = POINTS * 1000 - score
        name = ''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        name += 'q'
                    elif event.key == pygame.K_w:
                        name += 'w'
                    elif event.key == pygame.K_e:
                        name += 'e'
                    elif event.key == pygame.K_r:
                        name += 'r'
                    elif event.key == pygame.K_t:
                        name += 't'
                    elif event.key == pygame.K_y:
                        name += 'y'
                    elif event.key == pygame.K_u:
                        name += 'u'
                    elif event.key == pygame.K_i:
                        name += 'i'
                    elif event.key == pygame.K_o:
                        name += 'o'
                    elif event.key == pygame.K_p:
                        name += 'p'
                    elif event.key == pygame.K_a:
                        name += 'a'
                    elif event.key == pygame.K_s:
                        name += 's'
                    elif event.key == pygame.K_d:
                        name += 'd'
                    elif event.key == pygame.K_f:
                        name += 'f'
                    elif event.key == pygame.K_g:
                        name += 'g'
                    elif event.key == pygame.K_h:
                        name += 'h'
                    elif event.key == pygame.K_j:
                        name += 'j'
                    elif event.key == pygame.K_k:
                        name += 'k'
                    elif event.key == pygame.K_l:
                        name += 'l'
                    elif event.key == pygame.K_z:
                        name += 'z'
                    elif event.key == pygame.K_x:
                        name += 'x'
                    elif event.key == pygame.K_c:
                        name += 'c'
                    elif event.key == pygame.K_v:
                        name += 'v'
                    elif event.key == pygame.K_b:
                        name += 'b'
                    elif event.key == pygame.K_n:
                        name += 'n'
                    elif event.key == pygame.K_m:
                        name += 'm'
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_RETURN and bool(name):
                        save_result(name, end_score)
                        return

            screen.fill((0, 0, 0))
            text = ["Поздравляю вы прошли игру",
                    f"Ваш счёт {end_score}",
                    f"Для сохранения результата введите своё имя: {name}" ]
            font = pygame.font.Font(None, 50)
            text_coord = 50
            for line in text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
            pygame.display.flip()
            clock.tick(FPS)

    else:
        pass


def item_screen(name, description, damage, hp, speed, tears, path_to_file):
    text = [name,
            description,
            "Чтобы подобрать предмет нажмите <e>",
            "Чтобы отказаться от предмета нажмите <q>"]
    fon = pygame.transform.scale(load_image(path_to_file), (500, 500))
    screen.fill((0, 0, 0))
    screen.blit(fon, (1000, 500))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if player.hp + hp >= 1:
                    player.hp += hp
                if player.damage + damage >= 0.5:
                    player.damage += damage
                if player.speed + speed >= 1:
                    player.speed += speed
                if player.rate_of_fire - tears >= 5:
                    player.rate_of_fire -= tears
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return
        pygame.display.flip()
        clock.tick(FPS)


def save_result(name, score):
    with open('players.csv', mode='a', newline='', encoding='utf8') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"')
        writer.writerow([name, score])



class Player():
    def __init__(self):
        self.hp = 20
        self.speed = 5
        self.position_x = WIN_WIDTH // 2
        self.position_y = WIN_HEIGHT // 2
        self.rate_of_fire = 240
        self.damage = 1

    def move(self, direction):
        global ROOMUPDATE
        if direction == 'up':
            if self.position_y - self.speed >= 150 \
                    or (890 <= self.position_x <= 940 and CAN_MOVE_UP and ROOMCLEAR):
                self.position_y -= self.speed
                if self.position_y < 100:
                    NEWROOM = True
                    self.position_y = 750
                    for x in range(10):
                        for y in range(10):
                            if game_map[x][y] == '#' and NEWROOM:
                                game_map[x][y] = '@'
                                game_map[x - 1][y] = '#'
                                NEWROOM = False
                                ROOMUPDATE = True
                                break
        elif direction == 'down':
            if self.position_y + self.speed <= WIN_HEIGHT - 250 \
                    or (890 <= self.position_x <= 940 and CAN_MOVE_DOWN and ROOMCLEAR):
                self.position_y += self.speed
                if self.position_y > 820:
                    NEWROOM = True
                    self.position_y = 250
                    for x in range(10):
                        for y in range(10):
                            if game_map[x][y] == '#' and NEWROOM:
                                game_map[x][y] = '@'
                                game_map[x + 1][y] = '#'
                                NEWROOM = False
                                ROOMUPDATE = True
                                break
        elif direction == 'right':
            if self.position_x + self.speed <= WIN_WIDTH - 250 \
                    or (410 <= self.position_y <= 460 and CAN_MOVE_RIGHT and ROOMCLEAR):
                self.position_x += self.speed
                if self.position_x > 1750:
                    NEWROOM = True
                    self.position_x = 250
                    for x in range(10):
                        for y in range(10):
                            if game_map[x][y] == '#' and NEWROOM:
                                game_map[x][y] = '@'
                                game_map[x][y + 1] = '#'
                                NEWROOM = False
                                ROOMUPDATE = True
                                break
        elif direction == 'left':
            if self.position_x - self.speed >= 150 \
                    or (410 <= self.position_y <= 460 and CAN_MOVE_LEFT and ROOMCLEAR):
                self.position_x -= self.speed
                if self.position_x < 100:
                    NEWROOM = True
                    self.position_x = 1600
                    for x in range(10):
                        for y in range(10):
                            if game_map[x][y] == '#' and NEWROOM:
                                game_map[x][y] = '@'
                                game_map[x][y - 1] = '#'
                                NEWROOM = False
                                ROOMUPDATE = True
                                break

    def get_position(self):
        return (self.position_x, self.position_y)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color, shot_speed, facing):
        super().__init__(all_sprites)

        self.x = x + 50
        self.y = y + 50
        self.radius = radius

        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("white"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(self.x, self.y, 2 * radius, 2 * radius)
        self.rect.x = self.x
        self.rect.y = self.y
        self.mask = pygame.mask.from_surface(self.image)

        self.color = color
        self.shot_speed = shot_speed
        self.facing = facing
        if facing == 'up' or facing == 'left':
            self.vel = shot_speed * -1
        elif facing == 'down' or facing == 'right':
            self.vel = shot_speed

    def update(self):
        if not pygame.sprite.spritecollide(self, vertical_borders, dokill=False) and not pygame.sprite.spritecollide(self, horizontal_borders, dokill=False)\
                and not pygame.sprite.spritecollide(self, mobs, dokill=False):
            self.rect.x = self.x
            self.rect.y = self.y
            if self.facing == 'up' or self.facing == 'down':
                self.y += self.vel
            elif self.facing == 'left' or self.facing == 'right':
                self.x += self.vel
        else:
            self.kill()
        if self.x < 150 or self.x > WIN_WIDTH - 150 or self.y < 150 or self.y > WIN_HEIGHT - 150:
            self.kill()


class Mob(pygame.sprite.Sprite):

    def __init__(self, hp):
        super().__init__(all_sprites)
        path = random.choice(["mob1.png", "mob2.png", "mob3.png", "mob4.png", "mob5.png", "mob6.png", "mob7.png"])
        image = load_image(path)
        image = pygame.transform.scale(image, (100, 100))
        self.id = id
        self.hp = hp
        self.x = random.randint(150, WIN_WIDTH - 250)
        self.y = random.randint(150, WIN_HEIGHT - 250)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = 3
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        global POINTS
        x, y = player.get_position()
        if self.rect.x != x or self.rect.y != y:
            if self.rect.x > x:
                self.rect.x -= self.speed
            if self.rect.x < x:
                self.rect.x += self.speed
            if self.rect.y > y:
                self.rect.y -= self.speed
            if self.rect.y < y:
                self.rect.y += self.speed
        if bool(pygame.sprite.spritecollide(self, bullets, dokill=False)):
            self.hp -= player.damage
        if self.hp <= 0:
            self.kill()
            POINTS += 1


def DrawWin(screen):
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, FLOOR_COLOR, (150, 150, 1620, 715), 0)
    pygame.draw.rect(screen, WALL_COLOR, (0, 0, WIN_WIDTH, 150), 0)
    pygame.draw.rect(screen, WALL_COLOR, (0, 0, 150, WIN_HEIGHT), 0)
    pygame.draw.rect(screen, WALL_COLOR, (0, WIN_HEIGHT - 150, WIN_WIDTH, WIN_HEIGHT), 0)
    pygame.draw.rect(screen, WALL_COLOR, (WIN_WIDTH - 150, 0, WIN_WIDTH, WIN_HEIGHT), 0)
    pygame.draw.line(screen, 'black', (0, 0), (150, 150), 2)
    pygame.draw.line(screen, 'black', (150, 150), (WIN_WIDTH - 150, 150), 2)
    pygame.draw.line(screen, 'black', (150, 150), (150, WIN_HEIGHT - 150), 2)
    pygame.draw.line(screen, 'black', (WIN_WIDTH, WIN_HEIGHT), (WIN_WIDTH - 150, WIN_HEIGHT - 150), 2)
    pygame.draw.line(screen, 'black', (0, WIN_HEIGHT), (150, WIN_HEIGHT - 150), 2)
    pygame.draw.line(screen, 'black', (150, WIN_HEIGHT - 150), (WIN_WIDTH - 150, WIN_HEIGHT - 150), 2)
    pygame.draw.line(screen, 'black', (WIN_WIDTH - 150, 150), (WIN_WIDTH - 150, WIN_HEIGHT - 150), 2)
    pygame.draw.line(screen, 'black', (WIN_WIDTH - 150, 150), (WIN_WIDTH, 0), 2)
    player_position = player.get_position()
    player_sprite.rect.x, player_sprite.rect.y = player_position
    all_sprites.draw(screen)
    all_sprites.update()


def get_map(name):
    with open(name, 'r', encoding='utf-8') as file:
        text = file.readlines()
        mp = list()
        for line in text:
            mp.append(list(line))
    return mp


def add_mobs():
    global ROOMCLEAR, ROOMUPDATE
    if CURENTLEVEL == 1:
        mob = Mob(20)
    elif CURENTLEVEL == 2:
        mob = Mob(30)
    elif CURENTLEVEL == 3:
        mob = Mob(40)
    if CURENTLEVEL != 4:
        all_sprites.add(mob)
        mobs.add(mob)
    ROOMCLEAR = False
    ROOMUPDATE = False


if __name__ == '__main__':
    clock = pygame.time.Clock()
    player = Player()
    oldtime = pygame.time.get_ticks()
    first_time = pygame.time.get_ticks()
    NEWROOM = False
    CAN_MOVE_UP = None
    CAN_MOVE_DOWN = None
    CAN_MOVE_LEFT = None
    CAN_MOVE_RIGHT = None

    all_sprites = pygame.sprite.Group()
    player_sprite = pygame.sprite.Sprite()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    mobs = pygame.sprite.Group()

    image = load_image("Collectible_Fanny_Pack_appearance.png")
    image2 = pygame.transform.scale(image, (100, 100))
    player_sprite.image = image2
    player_sprite.rect = player_sprite.image.get_rect()
    all_sprites.add(player_sprite)

    door1_sprite = pygame.sprite.Sprite()
    image = load_image("Planetarium_door.png")
    image2 = pygame.transform.scale(image, (200, 150))
    door1_sprite.image = image2
    door1_sprite.rect = door1_sprite.image.get_rect()
    door1_sprite.rect.x = WIN_WIDTH // 2 - 100
    all_sprites.add(door1_sprite)

    door2_sprite = pygame.sprite.Sprite()
    image = load_image("Planetarium_door2.png")
    image2 = pygame.transform.scale(image, (150, 200))
    door2_sprite.image = image2
    door2_sprite.rect = door2_sprite.image.get_rect()
    door2_sprite.rect.x = WIN_WIDTH - 150
    door2_sprite.rect.y = WIN_HEIGHT // 2 - 100
    all_sprites.add(door2_sprite)

    door3_sprite = pygame.sprite.Sprite()
    image = load_image("Planetarium_door3.png")
    image2 = pygame.transform.scale(image, (200, 150))
    door3_sprite.image = image2
    door3_sprite.rect = door3_sprite.image.get_rect()
    door3_sprite.rect.x = WIN_WIDTH // 2 - 100
    door3_sprite.rect.y = WIN_HEIGHT - 150
    all_sprites.add(door3_sprite)

    door4_sprite = pygame.sprite.Sprite()
    image = load_image("Planetarium_door4.png")
    image2 = pygame.transform.scale(image, (150, 200))
    door4_sprite.image = image2
    door4_sprite.rect = door4_sprite.image.get_rect()
    door4_sprite.rect.x = 0
    door4_sprite.rect.y = WIN_HEIGHT // 2 - 100
    all_sprites.add(door4_sprite)

    Border(150, 150, WIN_WIDTH - 150, 150)
    Border(150, 150, 150, WIN_HEIGHT - 150)
    Border(WIN_WIDTH - 150, 150, WIN_WIDTH - 150, WIN_HEIGHT - 150)
    Border(150, WIN_HEIGHT - 150, WIN_WIDTH - 150, WIN_HEIGHT - 150)

    game_map = get_map("maps/map1.txt")
    room_map = get_map("maps/room_map1.txt")
    map2 = get_map("maps/map2.txt")
    room_map2 = get_map("maps/room_map2.txt")
    map3 = get_map("maps/map3.txt")
    room_map3 = get_map("maps/room_map3.txt")

    start_screen()

    score = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                pass
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move('up')
        if keys[pygame.K_s]:
            player.move('down')
        if keys[pygame.K_a]:
            player.move('left')
        if keys[pygame.K_d]:
            player.move('right')
        if keys[pygame.K_LEFT]:
            newtime = pygame.time.get_ticks()
            if newtime - oldtime > player.rate_of_fire:
                oldtime = newtime
                bullet = Projectile(player.get_position()[0], player.get_position()[1], 10, (255, 255, 255), 10, 'left')
                all_sprites.add(bullet)
                bullets.add(bullet)
        if keys[pygame.K_RIGHT]:
            newtime = pygame.time.get_ticks()
            if newtime - oldtime > player.rate_of_fire:
                oldtime = newtime
                bullet = Projectile(player.get_position()[0], player.get_position()[1], 10, (255, 255, 255), 10, 'right')
                all_sprites.add(bullet)
                bullets.add(bullet)
        if keys[pygame.K_UP]:
            newtime = pygame.time.get_ticks()
            if newtime - oldtime > player.rate_of_fire:
                oldtime = newtime
                bullet = Projectile(player.get_position()[0], player.get_position()[1], 10, (255, 255, 255), 10, 'up')
                all_sprites.add(bullet)
                bullets.add(bullet)
        if keys[pygame.K_DOWN]:
            newtime = pygame.time.get_ticks()
            if newtime - oldtime > player.rate_of_fire:
                oldtime = newtime
                bullet = Projectile(player.get_position()[0], player.get_position()[1], 10, (255, 255, 255), 10, 'down')
                all_sprites.add(bullet)
                bullets.add(bullet)

        for x in range(10):
            for y in range(10):
                if game_map[x][y] == '#':
                    try:
                        if room_map[x][y] == '1':
                            SPAWNMOBS = True
                            room_map[x][y] = '0'
                        elif room_map[x][y] == '0':
                            SPAWNMOBS = False
                        elif room_map[x][y] == '2':
                            LEVELUPDATE = True
                            CURENTLEVEL += 1
                            SPAWNMOBS = True
                    except:
                        pass

                    try:
                        if game_map[x][y - 1] != '-':
                            door4_sprite.rect.x = 0
                            door4_sprite.rect.y = WIN_HEIGHT // 2 - 100
                            CAN_MOVE_LEFT = True
                        elif game_map[x][y - 1] == '-':
                            door4_sprite.rect.x = 2000
                            door4_sprite.rect.y = 2000
                            CAN_MOVE_LEFT = False
                    except:
                        door4_sprite.rect.x = 2000
                        door4_sprite.rect.y = 2000
                        CAN_MOVE_LEFT = False

                    try:
                        if game_map[x][y + 1] != '-':
                            door2_sprite.rect.x = WIN_WIDTH - 150
                            door2_sprite.rect.y = WIN_HEIGHT // 2 - 100
                            CAN_MOVE_RIGHT = True
                        elif game_map[x][y + 1] == '-':
                            door2_sprite.rect.x = 2000
                            door2_sprite.rect.y = 2000
                            CAN_MOVE_RIGHT = False
                    except:
                        door2_sprite.rect.x = 2000
                        door2_sprite.rect.y = 2000
                        CAN_MOVE_RIGHT = False

                    try:
                        if game_map[x - 1][y] != '-':
                            door1_sprite.rect.x = WIN_WIDTH // 2 - 100
                            door1_sprite.rect.y = 0
                            CAN_MOVE_UP = True
                        if game_map[x - 1][y] == '-':
                            door1_sprite.rect.x = 2000
                            door1_sprite.rect.y = 2000
                            CAN_MOVE_UP = False
                    except:
                        door1_sprite.rect.x = 2000
                        door2_sprite.rect.y = 2000
                        CAN_MOVE_UP = False

                    try:
                        if game_map[x + 1][y] != '-':
                            door3_sprite.rect.x = WIN_WIDTH // 2 - 100
                            door3_sprite.rect.y = WIN_HEIGHT - 150
                            CAN_MOVE_DOWN = True
                        if game_map[x + 1][y] == '-':
                            door3_sprite.rect.x = 2000
                            door3_sprite.rect.y = 2000
                            CAN_MOVE_DOWN = False
                    except:
                        door3_sprite.rect.x = 2000
                        door3_sprite.rect.y = 2000
                        CAN_MOVE_DOWN = False

                    all_sprites.remove(door1_sprite)
                    all_sprites.remove(door2_sprite)
                    all_sprites.remove(door3_sprite)
                    all_sprites.remove(door4_sprite)

                    all_sprites.add(door1_sprite)
                    all_sprites.add(door2_sprite)
                    all_sprites.add(door3_sprite)
                    all_sprites.add(door4_sprite)

        if ROOMCLEAR and ROOMUPDATE and SPAWNMOBS:
            for _ in range(random.randint(1, 4)):
                add_mobs()
                if random.randint(1, 5) == 3:
                    pass
        if bool(pygame.sprite.spritecollide(player_sprite, mobs, dokill=False)):
            second_time = pygame.time.get_ticks()
            if second_time - first_time > 1000:
                player.hp -= 1
                first_time = second_time
        if player.hp <= 0:
            running = False
            game_over = True
        if len(mobs.sprites()) == 0 and not ROOMCLEAR:
            ROOMCLEAR = True
            new_item = random.randint(1, 7)
            if new_item == 5:
                item_id = random.randint(1, 10)
                con = sqlite3.connect("items.db")
                cur = con.cursor()
                result = cur.execute("""SELECT * FROM items WHERE id = ?""", (str(item_id),)).fetchall()
                con.close()
                id, name, description, damage, hp, speed, tears, path_to_file = result[0]
                item_screen(name, description, damage, hp, speed, tears, path_to_file)

            health_up = random.randint(0, 5)
            if player.hp + health_up >= 20:
                player.hp = 20
            else:
                player.hp += health_up

        if LEVELUPDATE:
            player.hp = 20
            LEVELUPDATE = False
            if CURENTLEVEL == 2:
                game_map = map2
                room_map = room_map2
            elif CURENTLEVEL == 3:
                game_map = map3
                room_map = room_map3
            elif CURENTLEVEL == 4:
                running = False

        DrawWin(screen)
        pygame.display.flip()
        clock.tick(FPS)
    game_over_screen()
    pygame.quit()