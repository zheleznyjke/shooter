from pygame import *
from random import randint

#mixer.init()
#mixer.music.load("space.ogg")
#mixer.music.play()
#fire_sound = mixer.Sound("fire.ogg")

font.init()
font2 = font.SysFont("Arial", 36)
font1 = font.SysFont("Arial", 80)

my_win = font1.render("Ты победил!",True, (0,180,0))
my_lose = font1.render("Ты проиграл",True, (180,0,0))

img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"

score = 0
lost = 0
MAX_LOST = 3
goal = 10

win_w = 700
win_h = 500
display.set_caption("Shooter")
window = display.set_mode((win_w, win_h))
background = transform.scale(image.load(img_back),(win_w, win_h))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(
            image.load(player_image),
            (size_x, size_y)
        )
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_w - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_h:
            self.rect.x = randint(80, win_h - 80)
            self.rect.y = -40
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, randint(80, win_h - 80),
                    -40, 80, 50, randint(1, 5))
    monsters.add(monster)

ship = Player(img_hero, 5, win_h - 100, 80, 100, 10)
finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #fire_sound.play()
                ship.fire()
    if not finish:
        window.blit(background, (0,0))

        text = font2.render("Рахунок: "+str(score), 1, (255,255,255))
        window.blit(text, (10,20))

        text_lose = font2.render("Пропущено: "+str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))

        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_w - 80), -40, 80,50, randint(1, 5))
            monsters.add(monster)

        if score >= goal:
            finish = True
            window.blit(my_win, (200,200))

        if  sprite.spritecollide(ship, monsters, False) or lost >= MAX_LOST:
            finish = True
            window.blit(my_lose, (200,200))


        display.update()
    time.delay(50)