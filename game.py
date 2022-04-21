import pygame,sys,random
from pygame.locals import *
pygame.init() 
w = 800
h = 600
screen = pygame.display.set_mode((w,h)) 
clock = pygame.time.Clock()

pygame.display.set_caption("Flappy Bird")
icon = pygame.image.load('bird.png')
pygame.display.set_icon(icon)

player_img = pygame.image.load('bird.png')
player_x = 100
player_y = 300 
dy = 0
up_key = False

def player(x,y):
    screen.blit(player_img,(x,y))

class impediments():
    def __init__(self,x,y,width,height,screen,color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height 
        self.screen = screen
        self.color = color
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height))
    def avoid_impediment(self,player,impediment):
        if pygame.Rect.colliderect(player,impediment):
            return True
        else:
            return False

counter = 0
tab = []
collision = 0

running = True
while running:
    counter += (clock.tick())/25
    if counter > 4.5:
        width = 100
        height = random.randrange(100,400)
        x = w - width 
        y1 = 0
        y2 = height + 150 
        color = (255,248,220)
        tab.append(impediments(x,y1,width,height,screen,color))
        tab.append(impediments(x,y2,width,h - y2,screen,color))
        counter = 0
    if up_key:
        dy = dy - 0.5
    else:
        dy = dy + 0.5 
    if dy > 7:
        dy = 7
    if dy < -7:
        dy = -7
    player_y = player_y + dy
    if player_y > 600 - 64:
        player_y = 600 - 64
    if player_y < 0:
        player_y = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            up_key = True
            dy = dy - 3
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            up_key = False
            dy = 0
    screen.fill((0,0,0))
    for x in tab:
        x.x -= 8
        x.draw(screen)
        player_rect = Rect(player_x,player_y,64,64)
        impediment_rect = Rect(x.x,x.y,x.width,x.height)
        obiekt = pygame.Rect.colliderect(player_rect,impediment_rect)
        if obiekt: 
           collision += 1
        if (collision/16) > 0:
            running = False                  
    player(player_x, player_y) 
    clock.tick(30)
    pygame.display.update()
pygame.quit()     





