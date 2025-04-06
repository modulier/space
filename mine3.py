#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer

score = 0 # сбито кораблей
goal = 10 # столько кораблей надо сбить для победы
lost = 0 # пропущено кораблей
max_lost = 10 # проигрышь если пропустили столько
life = 3

def start():

    with open("reiting.txt") as file:
        reiting = file.read()

    global goal, score, lost, max_lost, life, num_fire
# музыка
    mixer.init()
    mixer.music.load("space.ogg")
    mixer.music.play()
    fire_sound = mixer.Sound("fire.ogg") 

# надписи
    font.init()
    font1 = font.Font(None,80)
    win = font1.render('YOU WIN',True,(255,255,255))
    lose = font1.render('YOU LOSE',True,(180,0,0))

    font2 = font.Font(None,36)




    class GameSprite(sprite.Sprite):
        def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
            # вызывание конструктора класса GameSprite
            sprite.Sprite.__init__(self)
            # каждый спрайт должен хранить image
            self.image = transform.scale(image.load(player_image),(size_x,size_y))
            self.speed=player_speed
            # каждый спрайт должен иметь свойство rect - прямоугольник , в котором он описан
            self.rect = self.image.get_rect()
            self.rect.x = player_x
            self.rect.y = player_y
        # метод. отрисовывающий героя на окне
        def reset(self):
            window.blit(self.image,(self.rect.x,self.rect.y))

    class Player(GameSprite):
        def update(self):
            keys = key.get_pressed()
            if keys[K_LEFT]and self.rect.x > 5:
                self.rect.x -= self.speed
            if keys[K_RIGHT]and self.rect.x < win_width - 80:
                self.rect.x += self.speed

        def fire(self):
            bullet = Bullet("bullet.png",self.rect.centerx,self.rect.top,15,20,-15)
            bullets.add(bullet)
        
    #class Player2(GameSprite):
        #def update(self):
            #keys = key.get_pressed()
            #if keys[K_a]and self.rect.x > 5:
                #self.rect.x -= self.speed
            #if keys[K_d]and self.rect.x < win_width - 80:
                #self.rect.x += self.speed

        #def fire(self):
            #bullet = Bullet("bullet.png",self.rect.centerx,self.rect.top,15,20,-15)
            #bullets.add(bullet)


    class Enemy(GameSprite):
        def update(self):
            self.rect.y += self.speed
            global lost
            if self.rect.y > win_height:
                self.rect.y =  0
                self.rect.x = randint(80, win_width - 80)
                lost += 1

    class Bullet(GameSprite):
        # движение врага
        def update(self):
            self.rect.y += self.speed
            # исчезает если дойдет до края экрана
            if self.rect.y < 0:
                self.kill()




    # создаем окно
    win_width = 700
    win_height = 500
    window = display.set_mode((win_width,win_height))
    display.set_caption('Shooter')
    background = transform.scale(image.load('galaxy.jpg'),(win_width,win_height))

    # создаем спрайты 
    ship = Player("rocket.png" , 5, win_height - 100, 80, 100, 10)
    #ship2 = Player2("rocket.png" , 5, win_height - 100, 80, 100, 5)

    monsters = sprite.Group()
    for i in range(1,6):
        monster = Enemy("nos.png",randint(80, win_width - 80), -40, 80, 50, randint(1, 4))
        monsters.add(monster)

    asteroids = sprite.Group()
    for i in range ( 1 ,3):
        asteroid = Enemy("asteroid.png", randint(30, win_width - 30), -40, 80, 50,randint(1,5))
        asteroids.add(asteroid)

    bullets = sprite.Group()


    clock = time.Clock()
    FPS = 60
    finish=False 
#  основной цикл:
    run = True # флаг сбрасывается кнопкой закрытия окна
    rel_time = False # перезарядка
    num_fire = 0 #для подсчета выстрела



    while run:

        for e in event.get():
            if e.type == QUIT:
                run=False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if num_fire < 5 and rel_time == False:
                        num_fire = num_fire + 1
                        fire_sound.play()
                        ship.fire()

                    if num_fire >= 5 and rel_time == False: # если игрок сделал 5 выстрелов
                        last_time = timer() # заснкаем время когда это произошло
                        rel_time = True # ставим флаг перезарядки


        if not finish:


            window.blit(background,(0,0))

            text = font2.render("Счет: " + str(score),1 ,(225,255,255))
            window.blit(text, (10,20))

            text_lose = font2.render("Пропущено: " + str(lost),1 ,(225,255,255))
            window.blit(text_lose, (10,50))

            if int(reiting) < score:
                reiting = score

            text_lose = font2.render("Рейтинг: " + str(reiting),1 ,(225,255,255))
            window.blit(text, (10,100))


            ship.update()
            #ship2.update()
            monsters.update()
            asteroids.update()
            bullets.update()

            ship.reset()
            #ship2.reset()
            monsters.draw(window)
            asteroids.draw(window)
            bullets.draw(window)

            # перезарядка
            if rel_time == True:
                now_time = timer()

                if now_time - last_time < 3:
                    reload = font2.render("Wait,reload...", 1, (150,0,0))
                    window.blit(reload,(260,460))
                else:
                    num_fire = 0
                    rel_time = False

            # проверка стлокновения спрайтов
            collides = sprite.groupcollide(monsters,bullets,True,False)
            for c in collides:
                score = score + 1
  
                monster = Enemy("nos.png", randint(80,win_width - 80),40,80,50,randint(1, 5))
                monsters.add(monster)


                if sprite.spritecollide(ship,monsters ,False) or lost >= max_lost or sprite.spritecollide(ship,asteroids,False):
                    finish = True
                    window.blit(lose,(200,200))

                    if int(reiting) <= score:
                        with open("reiting.txt", "w") as file:
                            file.write(str(score))





            display.update()
            clock.tick(FPS)

        time.delay(50)