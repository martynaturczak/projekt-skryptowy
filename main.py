import pygame,sys,random
from pygame.locals import *
from pygame import mixer
import os
import operator
pygame.init() 
w = 1280
h = 720
screen = pygame.display.set_mode((w,h)) 
clock = pygame.time.Clock()
pygame.time.set_timer(USEREVENT+1, 2000)

pygame.display.set_caption("Flappy Bird")
icon = pygame.image.load('bird.png')
pygame.display.set_icon(icon)

game_background = pygame.image.load("game_background.png")
game_background = pygame.transform.scale(game_background, (1280, 720))

menu_background = pygame.image.load("go_background.png")
menu_background = pygame.transform.scale(menu_background, (1280, 720))

pipe_img = pygame.image.load('pipe.png')
coin_img =  pygame.image.load('coin.png')
diamond_img =  pygame.image.load('diamond.png')
player_img = pygame.image.load('bird.png')
ranking_img = pygame.image.load('ranking.png')
previous_img = pygame.image.load('previous.png')
player_x = 100
player_y = 300 
dy = 0
up_key = False

mixer.music.load('music.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

font = pygame.font.Font('freesansbold.ttf',32)
menu_font = pygame.font.Font('freesansbold.ttf',64)
over_font = pygame.font.Font('Linford.ttf',128)
character_font = pygame.font.Font('Linford.ttf',90)
score_font = pygame.font.Font('Linford.ttf',64)
name_input_font = pygame.font.Font('Linford.ttf',50)
text_x = 10
text_y = 10

def show_points(x,y):
    score = font.render("Score: " + str(points), True, (255,255,255))
    screen.blit(score,(x,y))

def show_coins(x,y):
    score = font.render("        : " + str(points2), True, (255,255,255))
    screen.blit(coin_img,(x,y - 10))
    screen.blit(score,(x,y + 5))

def show_superpower(x,y):
    screen.blit(diamond_img,(x,y + 10))

def player(x,y):
    screen.blit(player_img,(x,y))

class impediments():
    def __init__(self,x,y,width,height,screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height 
        self.screen = screen
    def draw(self,screen):
        pipe_image = pygame.transform.scale(pipe_img, (self.width, self.height))
        if self.y == 0:
            pipe_image = pygame.transform.flip(pygame.transform.scale(pipe_img, (self.width, self.height)), 0, 1)
        screen.blit(pipe_image,(self.x, self.y))
    def avoid_impediment(self,player,impediment):
        if pygame.Rect.colliderect(player,impediment):
            return True
        else:
            return False

class money():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def draw(self,screen):
        screen.blit(coin_img,(self.x,self.y))
    def collect_coin(self,player,coin):
        if pygame.Rect.colliderect(player,coin):
            return True
        else:
            return False

class get_diamond():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def draw(self,screen):
        screen.blit(diamond_img,(self.x,self.y))

counter = 0
tab = []
coins = []
diamonds = []
collision = 0
points = 0
points2 = 0
running = True
collecting = False
game_state = "menu"
superpower = False
power2 = False
super_points = 0
display_text = False
nick = ""
if not os.path.isfile('zapis.txt'):
    file = open('zapis.txt','x')


while running:
    if game_state == "menu":
        screen.blit(menu_background,(0,0))
        title_img = pygame.image.load("flappybird.png")
        title_rect = title_img.get_rect(center=((w/2,150)))
        screen.blit(title_img,title_rect)
        mouse_position = pygame.mouse.get_pos()
        play_image = pygame.image.load("play_button.png")
        play_image = pygame.transform.scale(play_image, (300, 100))
        play_rect = play_image.get_rect(center=((w/2,400)))
        screen.blit(play_image,play_rect)
        exit_image = pygame.image.load("exit_button.png")
        exit_image = pygame.transform.scale(exit_image, (300, 100))
        exit_rect = exit_image.get_rect(center=((w/2,540)))
        screen.blit(exit_image,exit_rect)
        ranking_img = pygame.image.load("ranking.png")
        ranking_rect = ranking_img.get_rect(center=((w - 64,64)))
        screen.blit(ranking_img,ranking_rect)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_position[0] in range (play_rect.left, play_rect.right) and mouse_position[1] in range (play_rect.top, play_rect.bottom):
                    game_state = "character"
                if mouse_position[0] in range (exit_rect.left, exit_rect.right) and mouse_position[1] in range (exit_rect.top, exit_rect.bottom):
                    running = False
                if mouse_position[0] in range (ranking_rect.left, ranking_rect.right) and mouse_position[1] in range (ranking_rect.top,ranking_rect.bottom):
                    game_state = "ranking"
            if event.type == pygame.QUIT:
                running = False
        clock.tick(30)
        pygame.display.update()
    elif game_state == "ranking":
        screen.blit(menu_background,(0,0))
        file = open("zapis.txt",'r')
        lines = file.readlines()
        file.close()
        keys = lines[0::2]
        values2 = lines[1::2]
        values = lines[1::2]
        for x in values:
            values[values.index(x)] = int(x)
        for x in values2:
            values2[values2.index(x)] = int(x)
        values.sort()
        values.sort(reverse = True)
        for value in values2:
            if values[0] == value:
                top1 = keys[values2.index(value)]
                top1_value = str(values[0])
            if values[1] == value:
                top2 = keys[values2.index(value)]
                top2_value = str(values[1])
            if values[2] == value:
                top3 = keys[values2.index(value)]
                top3_value = str(values[2]) 
        ranking_text = over_font.render("RANKING", True, (255,255,0))
        ranking_rect = ranking_text.get_rect(center=((w/2,150)))
        screen.blit(ranking_text, ranking_rect)
        top1_text = character_font.render('1. ' + top1[:-1] + ' ' +  top1_value, True, (255,255,0))
        top1_rect = top1_text.get_rect(center=((w/2,280)))
        screen.blit(top1_text, top1_rect)
        top2_text = character_font.render('2. ' + top2[:-1] + ' ' +  top2_value, True, (255,255,0))
        top2_rect = top2_text.get_rect(center=((w/2,400)))
        screen.blit(top2_text, top2_rect)
        top3_text = character_font.render('3. ' + top3[:-1] + ' ' +  top3_value, True, (255,255,0))
        top3_rect = top3_text.get_rect(center=((w/2,520)))
        screen.blit(top3_text, top3_rect)
        mouse_position = pygame.mouse.get_pos()
        previous_rect = previous_img.get_rect(center=((100,100)))
        screen.blit(previous_img,previous_rect)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_position[0] in range (previous_rect.left, previous_rect.right) and mouse_position[1] in range (previous_rect.top,previous_rect.bottom):
                    game_state = "menu"
            if event.type == pygame.QUIT:
                running = False
        clock.tick(30)
        pygame.display.update()
    elif game_state == "character":
        screen.fill((0,0,0))
        screen.blit(menu_background,(0,0))
        mouse_position = pygame.mouse.get_pos()
        character_text = character_font.render("Choose your player", True, (255,255,0))
        character_rect = character_text.get_rect(center=((w/2,140)))
        screen.blit(character_text, character_rect)
        name_input = name_input_font.render("Enter your nickname:", True, (255,255,0))
        name_input_rect = name_input.get_rect(center=((w/2,250)))
        screen.blit(name_input, name_input_rect)
        show_nickname = name_input_font.render(nick, True, (255,255,255))
        show_nickname_rect = show_nickname.get_rect(center=((w/2,320)))
        screen.blit(show_nickname, show_nickname_rect)
        player1_image = pygame.image.load("player11.png")
        player1_image = pygame.transform.scale(player1_image, (128, 128))
        player1_rect = player1_image.get_rect(center=((420, 480)))
        screen.blit(player1_image,player1_rect)
        player2_image = pygame.image.load("player22.png")
        player2_image = pygame.transform.scale(player2_image, (128, 128))
        player2_rect = player2_image.get_rect(center=((640, 480)))
        screen.blit(player2_image,player2_rect)
        player3_image = pygame.image.load("player33.png")
        player3_image = pygame.transform.scale(player3_image, (128, 128))
        player3_rect = player3_image.get_rect(center=((860, 480)))
        screen.blit(player3_image,player3_rect)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_position[0] in range (player1_rect.left, player1_rect.right) and mouse_position[1] in range (player1_rect.top, player1_rect.bottom) and nick!="":
                    game_state = "game"
                    player_img = pygame.transform.scale(player1_image, (64, 64))
                if mouse_position[0] in range (player2_rect.left, player2_rect.right) and mouse_position[1] in range (player2_rect.top, player2_rect.bottom) and nick!="":
                    game_state = "game"
                    player_img = pygame.transform.scale(player2_image, (64, 64))
                if mouse_position[0] in range (player3_rect.left, player3_rect.right) and mouse_position[1] in range (player3_rect.top, player3_rect.bottom) and nick!="":
                    game_state = "game"
                    player_img = pygame.transform.scale(player3_image, (64, 64))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and nick != "":
                    nick = nick[:-1]
                else:
                    nick += event.unicode
            if event.type == pygame.QUIT:
                running = False
        clock.tick(30)
        pygame.display.update()      
    elif game_state =="game":
        file = open("zapis.txt",'r')
        content = file.read()
        file.close()
        if nick not in content:
            file = open("zapis.txt",'a')
            file.write(nick + '\n')
            file.write('0' + '\n')
            file.close()
        if up_key:
            dy = dy - 0.5
        else:
            dy = dy + 0.5 
        if dy > 7:
            dy = 7
        if dy < -7:
            dy = -7
        player_y = player_y + dy
        if player_y > h - 64:
            player_y = h - 64
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
            if event.type == USEREVENT+1:
                width = 100
                height = random.randrange(100,400)
                x = w - width 
                y1 = 0
                y2 = height + 150 
                color = (255,248,220)
                tab.append(impediments(x,y1,width,height,screen))
                tab.append(impediments(x,y2,width,h - y2,screen))
                counter = 0
                if collecting == True:
                    coin = money(w - width + 18, height + 43)
                    coins.append(coin)
                    collecting = False
                if points > 0 and points % 7  == 0:
                    diamond = get_diamond(w - width + 200, height + 43)
                    diamonds.append(diamond)
        screen.fill((0,0,0))
        screen.blit(game_background,(0,0))
        for x in diamonds:
            x.x -= 8
            x.draw(screen)
            player_rect = Rect(player_x,player_y,64,64)
            diamond_rect = Rect(x.x,x.y,64,64)
            obiekt3 = pygame.Rect.colliderect(player_rect,diamond_rect)
            if obiekt3: 
                diamonds.pop(0)
                mixer.music.stop()
                mixer.music.load('superpower.mp3')
                mixer.music.set_volume(2.5)
                mixer.music.play()
                superpower = True
                super_points = points
                power2 = True
                display_text = True
        if super_points + 5 == points and power2 == True:
            superpower = False
            power2 = False
            display_text = False
        if  display_text == True:
            show_superpower(600,text_y)
        if super_points + 4 == points and display_text == True:
            display_text = False
            mixer.music.stop()
            mixer.music.set_volume(0.2)
            mixer.music.load('music.mp3')
            mixer.music.play()
        for x in coins:
            x.x -= 8
            x.draw(screen)
            player_rect = Rect(player_x,player_y,64,64)
            coin_rect = Rect(x.x,x.y,64,64)
            obiekt2 = pygame.Rect.colliderect(player_rect,coin_rect)
            if obiekt2: 
                coins.pop(0)
                obiekt2 = False
                points2 += 1
        for x in tab:
            if x.x < -108:
                tab.pop(0)
                tab.pop(0)
            x.x -= 8
            x.draw(screen)
            player_rect = Rect(player_x,player_y,64,64)
            impediment_rect = Rect(x.x,x.y,x.width,x.height)
            obiekt = pygame.Rect.colliderect(player_rect,impediment_rect)
            if obiekt == True and superpower == False: 
                collision += 1
                display_text = False
            if (collision/16) > 0:
                game_state = "game_over"  
                del tab[:]
                del coins[:]
            if x.x == player_rect.x and x.y == 0:
                points += 1
                if points % 2 == 0:
                    collecting = True
        player(player_x, player_y) 
        show_points(text_x,text_y)
        show_coins(text_x,52)
        clock.tick(30)
        pygame.display.update()
    elif game_state == "game_over":
        file = open("zapis.txt",'r')
        lines = file.readlines()
        file.close()
        for line in lines:
            if nick in line:
                nick_index = lines.index(line)
                if points > int(lines[nick_index + 1]):
                    del lines[nick_index]
                    del lines[nick_index]
                    lines.append(nick + '\n')
                    lines.append(str(points) + '\n')
                    file = open("zapis.txt",'w')
                    for x in lines:
                        file.write(x)
                    file.close()
        screen.fill((0,0,0))
        screen.blit(menu_background,(0,0))
        mouse_position = pygame.mouse.get_pos()
        game_over_text = over_font.render("GAME OVER", True, (255,255,0))
        game_over_rect = game_over_text.get_rect(center=((w/2,150)))
        screen.blit(game_over_text, game_over_rect)
        score_text = score_font.render("Score: " + str(points),  True, (255,255,0))
        score_rect = score_text.get_rect(center=((w/2,300)))
        screen.blit(score_text, score_rect)
        playagain_text = score_font.render("Play again?", True, (255,255,0))
        playagain_rect = playagain_text.get_rect(center=((w/2,400)))
        screen.blit(playagain_text, playagain_rect)
        yes_image = pygame.image.load("yes_button.png")
        yes_image = pygame.transform.scale(yes_image, (300, 107))
        yes_rect = yes_image.get_rect(center=((w/2 - 150,510)))
        screen.blit(yes_image,yes_rect)
        no_image = pygame.image.load("no_button.png")
        no_image = pygame.transform.scale(no_image, (300, 150))
        no_rect = no_image.get_rect(center=((w/2 + 150,520)))
        screen.blit(no_image,no_rect)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_position[0] in range (yes_rect.left, yes_rect.right) and mouse_position[1] in range (yes_rect.top, yes_rect.bottom):
                    game_state = "game"
                    points = 0
                    points2 = 0
                    collision = 0
                    counter = 0
                    running = True
                    collecting = False
                if mouse_position[0] in range (no_rect.left, no_rect.right) and mouse_position[1] in range (no_rect.top, no_rect.bottom):
                    running = False
            if event.type == pygame.QUIT:
                running = False
        clock.tick(30)
        pygame.display.update()      
pygame.quit() 

