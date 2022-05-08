#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
# init()
#классы (описание)
# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
  # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# класс главного игрока
class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys[K_RIGHT] or keys[K_d])and self.rect.x < width_win - width_player:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, width_bullet, hight_bullet, 10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > hight_win - hight_enemy:
            self.rect.y = 0
            self.rect.x = randint(0, width_win - width_enemy)
            lost += 1 # lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Boss(GameSprite):
    def fire(self):
        bullet = Bullet_Boss(img_bullet_boss, self.rect.centerx, self.rect.bottom, width_bullet, hight_bullet, 10)
        bullet.image = transform.rotate(bullet.image, 180)
        bullets_boss.add(bullet)

class Bullet_Boss(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > hight_win:
            self.kill()

#константы
width_win = 700
hight_win = 500
width_player = 60
hight_player = 110
width_enemy = 80
hight_enemy = 50
width_bullet = 20
hight_bullet = 20
width_restart = 300
hight_restart = 100

start_player_x = 300
start_player_y = hight_win - hight_player
restart_x = width_win / 2 - width_restart / 2
restart_y = hight_win * 4 / 5 - hight_restart

clock = time.Clock()
FPS = 60

lost = 0
score = 0

shoot_time = 0
interval_shoot = 3

#шрифты
font.init()
font1 = font.Font('Paper.otf', 36)
font_finish = font.Font('Paper.otf', 100)

win_text = font_finish.render("ПОБЕДА!!!", 1, (0, 255, 0))
lose_text = font_finish.render("ТЫ ПРОИГРАЛ!!!", 1, (255, 0, 0))

#музыка
#...


#картинки
img_back = "galaxy.jpg" # фон игры
img_bullet = "bullet.png" # пуля
img_player = "rocket.png" # герой
img_enemy = "ufo.png" # враг
img_restart = "Restart_Logo.png"
img_boss = "boss.png"
img_bullet_boss = "laser.png"

background = transform.scale(image.load(img_back), (width_win, hight_win))

#окно
window = display.set_mode((width_win, hight_win))
display.set_caption("Shooter")

#классы (создание объектов)
player = Player(img_player, start_player_x, start_player_y, width_player, hight_player, 12)

monsters = sprite.Group()
for i in range(5):
    rand_x = randint(0, width_win - width_enemy)
    rand_speed = randint(1, 5)
    rand_height = randint(-2*hight_enemy, -hight_enemy)
    enemy = Enemy(img_enemy, rand_x, rand_height, width_enemy, hight_enemy, rand_speed)
    monsters.add(enemy)

bullets = sprite.Group()
bullets_boss = sprite.Group()

restart = GameSprite(img_restart, restart_x, restart_y, width_restart, hight_restart, 0)
boss = Boss(img_boss, width_win / 2, 0, width_enemy*2, hight_enemy*2, 0)

#основной цикл
finish = False
run = True 
hasBoss = False

while run:
    for e in event.get():
        if e.type == QUIT:
           run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                if restart.rect.collidepoint(e.pos) and finish:
                    score = 0
                    lost = 0
                    finish = False
                else: 
                    player.fire()
                        

    if not finish:
        window.blit(background,(0,0))

        count_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(count_lose,(10, 10))

        score_text = font1.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(score_text,(10, 50))

        player.update()
        monsters.update()
        bullets.update()

        list_collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in list_collides:
            score += 1
            rand_x = randint(0, width_win - width_enemy)
            rand_speed = randint(1, 5)
            rand_height = randint(-2*hight_enemy, -hight_enemy)
            enemy = Enemy(img_enemy, rand_x, rand_height, width_enemy, hight_enemy, rand_speed)
            monsters.add(enemy)

        player.reset()
        monsters.draw(window)
        bullets.draw(window)

        if score >= 1:
            # finish = True
            # window.blit(win_text,(width_win / 2 - win_text.get_width() / 2, hight_win / 3 - win_text.get_height() / 2))
            # restart.reset()
            hasBoss = True

        if hasBoss:
            boss.reset()

            now_time = timer()

            if now_time - shoot_time >= interval_shoot:
                boss.fire()
                # print("Босс стреляет")
                shoot_time = timer()

            bullets_boss.update()
            bullets_boss.draw(window)


        if lost >= 5:
            finish = True
            window.blit(lose_text,(width_win / 2 - lose_text.get_width() / 2, hight_win / 3 - lose_text.get_height() / 2))
            restart.reset()

    display.update()
    clock.tick(FPS)


# elif e.type == MOUSEBUTTONDOWN:
        #     if e.button == 1:
        #         player.fire()



# from pygame import *
# from random import randint
# # подгружаем отдельно функции для работы со шрифтом
# font.init()
# font1 = font.Font('Paper.otf', 80)
# win = font1.render('YOU WIN!', True, (255, 255, 255))
# lose = font1.render('YOU LOSE!', True, (180, 0, 0))

# font2 = font.Font(None, 36)

# #фоновая музыка
# mixer.init()
# mixer.music.load('space.ogg')
# mixer.music.play()
# fire_sound = mixer.Sound('fire.ogg')

# # нам нужны такие картинки:
# img_back = "galaxy.jpg" # фон игры
 
# img_bullet = "bullet.png" # пуля
# img_hero = "rocket.png" # герой
# img_enemy = "ufo.png" # враг
 
# score = 0 # сбито кораблей
# goal = 10 # столько кораблей нужно сбить для победы
# lost = 0 # пропущено кораблей
# max_lost = 3 # проиграли, если пропустили столько
 
# # класс-родитель для других спрайтов
# class GameSprite(sprite.Sprite):
#   # конструктор класса
#     def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
#         # Вызываем конструктор класса (Sprite):
#         sprite.Sprite.__init__(self)

#         # каждый спрайт должен хранить свойство image - изображение
#         self.image = transform.scale(image.load(player_image), (size_x, size_y))
#         self.speed = player_speed

#         # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
#         self.rect = self.image.get_rect()
#         self.rect.x = player_x
#         self.rect.y = player_y
 
#   # метод, отрисовывающий героя на окне
#     def reset(self):
#         window.blit(self.image, (self.rect.x, self.rect.y))

# # класс главного игрока
# class Player(GameSprite):
#     # метод для управления спрайтом стрелками клавиатуры
#     def update(self):
#         keys = key.get_pressed()
#         if keys[K_LEFT] and self.rect.x > 5:
#             self.rect.x -= self.speed
#         if keys[K_RIGHT] and self.rect.x < win_width - 80:
#             self.rect.x += self.speed
#   # метод "выстрел" (используем место игрока, чтобы создать там пулю)
#     def fire(self):
#         bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
#         bullets.add(bullet)

# # класс спрайта-врага   
# class Enemy(GameSprite):
#     # движение врага
#     def update(self):
#         self.rect.y += self.speed
#         global lost
#         # исчезает, если дойдет до края экрана
#         if self.rect.y > win_height:
#             self.rect.x = randint(80, win_width - 80)
#             self.rect.y = 0
#             lost = lost + 1
 
# # класс спрайта-пули   
# class Bullet(GameSprite):
#     # движение врага
#     def update(self):
#         self.rect.y += self.speed
#         # исчезает, если дойдет до края экрана
#         if self.rect.y < 0:
#             self.kill()
 
# # Создаем окошко
# win_width = 700
# win_height = 500
# display.set_caption("Shooter")
# window = display.set_mode((win_width, win_height))
# background = transform.scale(image.load(img_back), (win_width, win_height))
 
# # создаем спрайты
# ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
# # создание группы спрайтов-врагов
# monsters = sprite.Group()
# for i in range(1, 6):
#     monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
#     monsters.add(monster)
 
# bullets = sprite.Group()
 
# # переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
# finish = False
# # Основной цикл игры:
# run = True # флаг сбрасывается кнопкой закрытия окна
# while run:
#     # событие нажатия на кнопку Закрыть
#     for e in event.get():
#         if e.type == QUIT:
#             run = False
#         # событие нажатия на пробел - спрайт стреляет
#         elif e.type == KEYDOWN:
#             if e.key == K_SPACE:
#                 fire_sound.play()
#                 ship.fire()
 
#   # сама игра: действия спрайтов, проверка правил игры, перерисовка
#     if not finish:
#         # обновляем фон
#         window.blit(background,(0,0))

#         # пишем текст на экране
#         text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
#         window.blit(text, (10, 20))

#         text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
#         window.blit(text_lose, (10, 50))

#         # производим движения спрайтов
#         ship.update()
#         monsters.update()
#         bullets.update()

#         # обновляем их в новом местоположении при каждой итерации цикла
#         ship.reset()
#         monsters.draw(window)
#         bullets.draw(window)
 
#         # проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
#         collides = sprite.groupcollide(monsters, bullets, True, True)
#         for c in collides:
#             # этот цикл повторится столько раз, сколько монстров подбито
#             score = score + 1
#             monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
#             monsters.add(monster)

#         # возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
#         if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
#             finish = True # проиграли, ставим фон и больше не управляем спрайтами.
#             window.blit(lose, (200, 200))

#         # проверка выигрыша: сколько очков набрали?
#         if score >= goal:
#             finish = True
#             window.blit(win, (200, 200))

#         display.update()
#     # цикл срабатывает каждую 0.05 секунд
#     time.delay(50)