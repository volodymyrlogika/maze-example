#створи гру "Лабіринт"!
from pygame import *
mixer.init()
FPS = 60
WIDTH, HEIGHT = 700, 525
window = display.set_mode((WIDTH, HEIGHT))
mixer.music.load('jungles.ogg')
mixer.music.play()
mixer.music.set_volume(0.01)
kick = mixer.Sound('kick.ogg')
kick.play()
count = 0
display.set_caption('Лабіринт')


class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, x, y, width, height):
        self.image = transform.scale(image.load(sprite_img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self):
        window.blit(self.image, self.rect)


class Player(GameSprite):
    def update(self):
        pressed = key.get_pressed()
        old_pos = self.rect.x, self.rect.y
        if pressed[K_w] and self.rect.y > 0:
            self.rect.y -= 3

        if pressed[K_s] and self.rect.y < HEIGHT - 70:
            self.rect.y += 3

        if pressed[K_a] and self.rect.x > 0:
            self.rect.x -= 3

        if pressed[K_d] and self.rect.x < WIDTH - 70:
            self.rect.x += 3
    
        for w in walls:
            if sprite.collide_rect(player, w):
                self.rect.x, self.rect.y = old_pos


class Enemy(GameSprite):
    def __init__(self, x , y , sprite_img = 'cyborg.png', speed = 2):
        super().__init__(sprite_img, x, y, 30, 30)
        self.speed = speed
    def update(self, walls):
        for w in walls:
            if sprite.collide_rect(self, w):
                self.speed = self.speed * -1

        self.rect.x += self.speed 


class Wall(GameSprite):
    def __init__(self, x , y, ):
        super().__init__('wall.png', x, y, 35, 35)


class Coin(GameSprite):
    def __init__(self, x , y, ):
        super().__init__('pngegg.png', x, y, 20, 20)


bg = transform.scale(image.load("background.jpg"), (WIDTH, HEIGHT))
player = Player('hero.png', 40 , 350, 30, 30)
gold = GameSprite('treasure.png', WIDTH - 100 , 420, 30, 30)

walls = []
enemys = []
coins = []

with open('map.txt', 'r') as file:
    x, y = 0, 0
    map = file.readlines()
    for line in map:
        for symbol in line:
            if symbol == 'W':
                walls.append(Wall(x, y))
            elif symbol == 'S':
                player.rect.x = x
                player.rect.y = y
            elif symbol == 'F':
                gold.rect.x = x
                gold.rect.y = y
            elif symbol == 'E':
                enemys.append(Enemy(x, y))
            elif symbol == 'C':
                coins.append(Coin(x + 7.5, y + 7.5))
                
            x += 35
        y += 35
        x = 0

run = True
finish = False
clock = time.Clock()

font.init()
font1 = font.SysFont('Impact', 70)
result = font1.render('YOU LOSE' , True, (140, 100, 30))

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        player.update()
        window.blit(bg, (0, 0))
        player.draw()
        
        gold.draw()
        for w in walls:
            w.draw()

        for e in enemys:
            e.update(walls)
            e.draw()
            if sprite.collide_rect(player, e):
                finish = True  

        for c in coins:
            c.draw() 
            if sprite.collide_rect(player, c):
                count += 1
                coins.remove(c)
                
        if sprite.collide_rect(player, gold):
            if count == 16:
                finish = True
                result = font1.render('YOU WIN'  , True, (210, 150, 100))
            
    else:
        window.blit(result, (250, 200))
    display.update()
    clock.tick(FPS)