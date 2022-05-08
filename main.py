from pygame import *
from random import randint
from gameSprite import *

# класс-родитель для других спрайтов
# class GameSprite(sprite.Sprite):
#     def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
#         sprite.Sprite.__init__(self)
    
#         self.image = transform.scale(image.load(player_image), (size_x, size_y))
#         self.speed = player_speed
    
#         self.rect = self.image.get_rect()
#         self.rect.x = player_x
#         self.rect.y = player_y
    
#     def reset(self, win):
#         win.blit(self.image, (self.rect.x, self.rect.y))

# класс главного игрока
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.x < win_width - 80:
            self.rect.x += self.speed
  # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -30)
        bullets.add(bullet)

# класс спрайта-врага   
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1
 
# класс спрайта-пули   
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
 

# подгружаем отдельно функции для работы со шрифтом
font.init()
font = font.Font('Paper.otf', 36)

# https://www.youtube.com/watch?v=jgqPcx45iiw&ab_channel=selfedu
mixer.pre_init(44100, -16, 1, 512)
mixer.init()
 
img_win = "win.png"
img_los = "gameover.jpg"
img_back = "galaxy.jpg" 
img_h = transform.scale(image.load("helth.png"), (20, 20))
img_ex = "exit.png"
img_pause = 'helth.png' #"pause.png"
img_restart = 'helth.png' #"restart.png"
 
img_bullet = "bullet.png" 
img_hero = "rocket.png"
img_enemy = "ufo.png" 

snd_back = "space.ogg"
snd_shoot = mixer.Sound("zvuk-kogda-metnuli-ognennyiy-shar.ogg")
 
score = 0 
goal = 10 
lost = 0 
max_lost = 3 

display.set_caption("Шутер")
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
# window = display.set_mode((0, 0), FULLSCREEN)
win_width, win_height = display.get_surface().get_size()
background = transform.scale(image.load(img_back), (win_width, win_height))

mixer.music.load(snd_back)
mixer.music.play()

ship = Player(img_hero, 5, win_height - 100, 80, 100, 20)

ex = GameSprite(img_ex, win_width - 50, 5, 30, 30, 0)
pause = GameSprite(img_pause, win_width / 2 - 150, win_height / 2 - 150, 300, 300, 0)
restart = GameSprite(img_restart, win_width / 2 - 150, win_height - 160, 300, 130, 0)

monsters = sprite.Group()
for i in range(1, 10):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(2, 10))
    monsters.add(monster)
    
bullets = sprite.Group()

game_pause = False
sprite_run = True
# Основной цикл игры:
run = True 
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and sprite_run:
                snd_shoot.play()
                ship.fire()
            elif e.key == K_ESCAPE:
                sprite_run = False
                game_pause = True
                pause.reset(window)
                mixer.music.pause()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                # mouse_pos = mouse.get_pos()
                if ex.rect.collidepoint(e.pos):
                    run = False
                elif pause.rect.collidepoint(e.pos) and game_pause:
                    game_pause = False
                    sprite_run = True
                    mixer.music.unpause()
                elif restart.rect.collidepoint(e.pos) and not sprite_run:
                    sprite_run = True
                    mixer.music.play()
                    for m in monsters:
                        m.rect.y = 0
                elif sprite_run:
                    snd_shoot.play()
                    ship.fire()


  # сама игра: действия спрайтов, проверка правил игры, перерисовка
    if sprite_run:
        # обновляем фон
        window.blit(background,(0,0))
    
        # пишем текст на экране
        text = font.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
    
        text_lose = font.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        show_h = 0
        x_h = 5
        while show_h != max_lost - lost:
            window.blit(img_h, (x_h, 100))
            x_h += 30
            show_h += 1
    
        # производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
    
        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset(window)
        monsters.draw(window)
        bullets.draw(window)
            
        # проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # этот цикл повторится столько раз, сколько монстров подбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
    
        # возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            mixer.music.stop()
            sprite_run = False # проиграли, ставим фон и больше не управляем спрайтами.
            # вычисляем отношение
            # img = transform.scale(image.load(img_los), (win_height, win_height))
            # d = img.get_width() // img.get_height()
            # window.fill((255, 255, 255))
            # window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))
            img = image.load(img_los)
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
            restart.reset(window)
            score = 0
            lost = 0
            for b in bullets:
                b.kill()
    
        # проверка выигрыша: сколько очков набрали?
        if score >= goal:
            mixer.music.stop()
            sprite_run = False
            img = image.load(img_win)
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
            restart.reset(window)
            score = 0
            lost = 0
            for b in bullets:
                b.kill()

        ex.reset(window)

    display.update()
    # цикл срабатывает каждую 0.05 секунд
    time.delay(50)

