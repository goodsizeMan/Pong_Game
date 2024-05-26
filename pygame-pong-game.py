
from typing import Any
import pygame
import subprocess as sub
from gpiozero import MCP3008,Button

#初始化pygame
pygame.init()

#設定視窗大小
FPS = 60
WIDTH = 800
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("PONG")
clock = pygame.time.Clock()

#GPIO 設定
r_pot = MCP3008(0)
l_pot = MCP3008(1)
up_pot = MCP3008(2)

r_button = Button(26)
l_button = Button(2)
home_button = Button(3)

#Game Menu 路徑
game_menu_path = r'D:\Projects\python_project\game_menu\pygame_game_menu.py'

#顏色設定
BLACK = (0,0,0)
WHITE = (255,255,255)

#發球設定
isThrow = False

# Class
class L_Player(pygame.sprite.Sprite):
    

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,80))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 240
        self.speed = 6
        self.l_player_rect = self.rect

    def update(self):
        global isThrow      
        #按鍵控制
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w]:
            self.rect.y -= self.speed
        if key_pressed[pygame.K_s]:
            self.rect.y += self.speed
        if key_pressed[pygame.K_j] and ball.rect.x <= 400:
            isThrow = True

        if l_pot.value>0.25:
            self.rect.y -= self.speed
        if l_pot.value<0.25:
            self.rect.y += self.speed

        if l_button.is_pressed and ball.rect.x <= 400:
            isThrow = True


        #脫屏判斷
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        
class R_Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,80))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 700
        self.rect.y = 240
        self.speed = 6

    def update(self):
        global isThrow
        #按鍵控制
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
        if key_pressed[pygame.K_LEFT] and ball.rect.x >= 400:
            isThrow = True

        if r_pot.value>0.25:
            self.rect.y -= self.speed
        if r_pot.value<0.25:
            self.rect.y += self.speed

        if r_button.is_pressed and ball.rect.x >= 400:
            isThrow = True

        #脫屏判斷
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Ball(pygame.sprite.Sprite):
     
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 240
        self.ball_vel_x,self.ball_vel_y = 3, 3

    def update(self):
        global isThrow
        if(isThrow):
            self.rect.x += self.ball_vel_x
            self.rect.y += self.ball_vel_y
        elif(isThrow==False and self.rect.x <= 400):
            self.rect.x = l_player.rect.x + l_player.rect.width
            self.rect.y = l_player.rect.centery
        elif(isThrow==False and self.rect.x >= 400):
            self.rect.x = r_player.rect.x 
            self.rect.y = r_player.rect.centery

        # ball第一次觸地
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.ball_vel_y *= -1
        
        #ball碰到底 重置

        ## ball碰到右底
        if self.rect.right >= WIDTH:
            isThrow=False
            self.rect.x = l_player.rect.x + l_player.rect.width
            self.rect.y = l_player.rect.centery
            self.ball_vel_x *= -1

        ## ball 碰到左底   
        if self.rect.left <= 0:
            isThrow=False
            self.rect.x = r_player.rect.x 
            self.rect.y = r_player.rect.centery
            self.ball_vel_x *= -1

        #ball 碰撞 player
        if pygame.sprite.collide_rect(self,l_player):
            self.rect.x = l_player.rect.right
            self.ball_vel_x *= -1

        if pygame.sprite.collide_rect(self,r_player):
            self.rect.x = r_player.rect.left - self.rect.width
            self.ball_vel_x *= -1     

#遊戲字體
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size,x,y):
    
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text, True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
         
#遊戲標題畫面
def draw_init():
    draw_text(screen,"PONG",64,400,100)  
    draw_text(screen,"Pressed any button to START",36,400,200)
    
    pygame.display.update()  
    waiting = True

    while waiting:
        clock.tick(FPS)
    #取得輸入
        for event in pygame.event.get(): 
            
            if event.type == pygame.QUIT:
                pygame.quit()

        key_pressed = pygame.key.get_pressed() 
        if key_pressed[pygame.K_q]:
            sub.Popen(["python",game_menu_path])
            pygame.quit()
        if key_pressed[pygame.K_j]:
            waiting = False

        #如果按Home鍵返回Menu 按r、l_button則開始遊戲
        if home_button.is_pressed:
            sub.Popen(["python",game_menu_path])
            pygame.quit()
        if r_button.is_pressed:
            waiting = False
        if l_button.is_pressed:
            waiting = False



#創建Sprite群組
all_sprites = pygame.sprite.Group()
l_player = L_Player()
r_player = R_Player()
ball = Ball()
all_sprites.add(l_player,r_player,ball)

#鼠標鎖定 和 隱藏
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)



#遊戲迴圈
running = True
show_init = True

while running:
    #判斷先進入遊戲標題
    if(show_init):
        draw_init()
        show_init = False

    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
       
        if event.type == pygame.QUIT:
            running = False

    ##按下Home鍵關閉遊戲回到MENU
    key_pressed = pygame.key.get_pressed() 
    if key_pressed[pygame.K_q]:
        sub.Popen(["python",game_menu_path])
        pygame.quit()

    if home_button.is_pressed:
        sub.Popen(["python",game_menu_path])
        pygame.quit()

    #更新遊戲
    all_sprites.update()

    #畫面更新
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.update()

#遊戲結束
pygame.quit()