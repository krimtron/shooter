import pygame
from time import time
import random
from random import randint
import os



pygame.init()


wind_width, wind_height = 700, 500


window = pygame.display.set_mode((wind_width, wind_height))

pygame.mixer_music.load("space.ogg")
pygame.mixer_music.set_volume(0.1)
pygame.mixer_music.play(-1)

FPS = 40


clock = pygame.time.Clock()
bots = []            

back = pygame.image.load("galaxy.jpg")
back = pygame.transform.scale(back, (wind_width, wind_height))

miss = 0

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image,speed):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image
        self.speed = speed
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def collide(self, obj):
        if self.rect.colliderect(obj.rect):
            return True
        else:
            return False


class Player(GameSprite):

    def move(self, left, right):
        k = pygame.key.get_pressed()
        if k[right]:
            if self.rect.x <= wind_width - self.rect.width:
                self.rect.x += self.speed
        if k[left]:
            if self.rect.x >= 0:
                self.rect.x -= self.speed

    def shoot(self):
        k = pygame.key.get_pressed()
        if k[pygame.K_q]:
            bulet = Bullet(self.rect.x + 35, self.rect.y, 10, 20, Pla_img,13)


    def collide(self, obj):
        if self.rect.colliderect(obj.rect):
            return True
        else:
            return False

class Bot (GameSprite):
    def __init__(self,x,y,w,h,image,speed):
        super().__init__(x,y,w,h,image,speed)
        bots.append(self)

    def move(self):
        global miss
        self.rect.y += self.speed
        if self.rect.y >= 520:
            bots.remove(self)
            miss += 1

meteors = []

class Meteor (GameSprite):
    def __init__(self,x,y,w,h,image,speed):
        super().__init__(x,y,w,h,image,speed)
        meteors.append(self)

    def move(self):
        global miss
        self.rect.y += self.speed
        if self.rect.y >= 550:
            meteors.remove(self)
            

bullets = []

bullet_group = pygame.sprite.Group()

class Bullet(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image, speed)
        bullet_group.add(self)
        bullets.append(self)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom <= 0 :
            bullet_group.remove(self)




font1 = pygame.font.SysFont("Arial",30)
font = pygame.font.SysFont("Arial",40)
font2 = pygame.font.SysFont("Arial",20)

Player_img = pygame.image.load("rocket.png")
player = Player(350,400,80,85,Player_img,6)

lox_img = pygame.image.load("ufo.png")
lox_img2 = pygame.image.load("asteroid.png")

Pla_img = pygame.image.load("bullet.png")
#bullet = Player(350,400,80,85,Pla_img,4)


ok = 0
reloa = 20
vistrelov = 10
sbitoo = 10
bot_wait  = 50
metiors_wait  = 250
sbito = 0
finish = False
game = True
heal = 3
level = 0
while game:
    window.blit(back, (0, 0))
    
    if not finish:

        player.draw()
        player.move(pygame.K_a, pygame.K_d)

        if bot_wait == 0:
            x = randint(50,650)
            speeed = randint(1,4)
            bot = Bot(x,0,50,40,lox_img,speeed)
            bot_wait = randint(100,200)
        else:
            bot_wait -= 1

        if metiors_wait == 0:
            x = randint(50,650) 
            speeed = randint(3,8)
            meteor = Meteor(x,0,100,90,lox_img2,speeed)
            metiors_wait = randint(300,1000)
        else:
            metiors_wait -= 1

        for meteor in meteors:
            meteor.draw()
            meteor.move()


        bullet_group.update()
        bullet_group.draw(window)



        time_lb = font1.render("Пропуски: ",True,(250,250,250))
        tim_lb = font1.render(str(miss),True,(250,250,250))
        sbit = font1.render("Сбито: "+ str(sbito),True,(250,250,250))
        hp = font1.render("Жизни: " + str(heal),True,(250,250,250))
        patronov = font1.render("Потроны: " + str(vistrelov),True,(250,250,250))
        window.blit(time_lb, (0, 0))
        window.blit(tim_lb, (150, 0))
        window.blit(hp, (250, 0))
        window.blit(sbit, (500, 0))
        window.blit(patronov, (0, 50))
        r = font2.render("Нажмите R ",True,(250,250,250))
        r1 = font2.render("для перезарядки ",True,(250,250,250))

    

    for bot in bots:
        if player.collide(bot):
            heal = heal - 1
            bots.remove(bot)

        else:
            bot.draw()
            bot.move()

        for bulet in bullets:
            if bulet.collide(bot):
                bots.remove(bot)
                bullets.remove(bulet)
                sbito += 1


    for meteor in meteors:
        if player.collide(meteor):
            heal = heal - 1
            meteors.remove(meteor)


        else:
            meteor.draw()
            meteor.move()
    
    #if player.collide(Bot):
        #window.fill((255,0,0))
        #game_over = font.render("Game Over!", True, (20,20,20))
        #window.blit(game_over,(300,250))
        #finish = True
            

    if miss == 3:
        window.fill((255,0,0))
        game_over = font.render("Game Over!", True, (20,20,20))
        window.blit(game_over,(300,250))
        finish = True

    if heal == 0:
        window.fill((255,0,0))
        game_over = font.render("Game Over!", True, (20,20,20))
        window.blit(game_over,(300,250))
        finish = True

    if sbito == sbitoo:
        heal += 1
        sbitoo += 10





    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and finish:
            finish = False
            miss = 0
            bot_wait  = 50
            metiors_wait  = 250
            meteors = []
            bots = []
            heal = 3
            vistrelov = 10
            sbito = 0
            sbitoo = 10

        if vistrelov == 0:
            pass
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                player.shoot()
                vistrelov -= 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            vistrelov = 10


    pygame.display.update()
    clock.tick(FPS)