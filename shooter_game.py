from pygame import *
from random import randint


window = display.set_mode((700, 500))
display.set_caption('SpaceWars')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

score = 0
missed = 0
font.init()
font1 = font.SysFont('Arial', 35)
font_f = font.SysFont('Arial', 70)
win = font_f.render('YOU WIN!', True, (255, 255, 255))
lose = font_f.render('YOU LOSE!', True, (255, 255, 255))

game = True
finish = False
clock = time.Clock()
FPS = 60

finish = False

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y, length, width):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (length, width))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', 15, self.rect.centerx-5, self.rect.top, 15, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(5, 620)
            missed += 1

class Asteroids(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(5, 650)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Player('rocket.png', 5, 300, 420, 65, 65)
enemies = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(1,2), randint(5, 630), 0, 80, 60)
    enemies.add(enemy)
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroids('asteroid.png', 1, randint(5, 630), 0, 50, 50)
    asteroids.add(asteroid)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type ==  KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                fire.play()

    display.update()
    clock.tick(FPS)

    if not finish:
        window.blit(background, (0, 0))
        player.reset()
        player.update()
        enemies.draw(window)
        enemies.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        score_label = font1.render('Score: '+str(score), True, (255, 255, 255))
        missed_label = font1.render('Missed: '+str(missed), True, (255, 255, 255))
        window.blit(score_label, (5, 10))
        window.blit(missed_label, (5, 40))
        collides = sprite.groupcollide(bullets, enemies, True, True)
        for c in collides:
            score += 1
            enemy = Enemy('ufo.png', randint(1,2), randint(5, 630), 0, 80, 60)
            enemies.add(enemy)
        if score >= 10:
            finish = True
            window.blit(win, (250, 250))
        if missed >= 3 or sprite.spritecollide(player, enemies, False) or sprite.spritecollide(player, asteroids, False):
            finish = True
            window.blit(lose, (220, 250))