import random, pygame, sys,time,math
from pygame.locals import *
from UFO import *
from Stone import *
from explosion import *
from shield import *
from setting import *
from gravel import *
Game = 0
Score = 0


screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)
pygame.display.set_caption("1104105330 UFO閃躲隕石 Ver1.1")
pygame.mixer.pre_init(22050, 16, 2, 512)

pygame.init()


font = pygame.font.Font("Fonts/msjh.ttf", 48)
framerate = pygame.time.Clock()

ufo = Anime(screen)
ufo.load("image/ufo.png", 56, 40, 6)

shield = Shield(screen)
shield.load("image/shield.png",400,400,4)
bg = pygame.image.load('image/background.png').convert()
bg = pygame.transform.scale(bg,(SCREEN_WIDTH+40,SCREEN_HEIGHT+40))
bg.set_alpha(127)


################################
def setting_init():
    global stones,Game,SPEED,Score
    stones=[]
    Game = 1
    SPEED = 0.05
    ufo.locate = 0
    ufo.x = SCREEN_WIDTH/2-ufo.width/2
    Score = 0
################################
def show_text(text,x,y):
    x = x
    y = y
    text = font.render(text,True,(255,255,255))
    screen.blit(text,(x,y))

################################
explosions = []
def explosion_code():
    for i in explosions:
        i.update(ticks)
        i.draw(screen)
        if i.frame==15:explosions.remove(i)
################################
def shield_code():
    if shield.visable:
        if shield.x != ufo.x - 100 or shield.y != ufo.y - 100:
            shield.x = ufo.x-100
            shield.y = ufo.y-150
        shield.update(ticks)
        shield.draw(screen)
################################
gravels = []
def gravel_code():#畫面上碎石平均數量約在10~15顆左右
    n = random.randint(0,5)
    if n==0:
        g = class_gravel()
        g.load("image/stone2.png",300,300,4)
        gravels.append(g)

        
    for i in range(len(gravels)-1,-1,-1):
        gravels[i].update(ticks,SPEED)
        gravels[i].draw(screen)
        if gravels[i].x+gravels[i].width<0 or gravels[i].x>SCREEN_WIDTH or gravels[i].y > SCREEN_HEIGHT:
            del gravels[i]
        
        
################################
stones = []
def stone_code():
    global Game,Score
    if Game and len(stones)==0:
        n = random.randint(-1,1)
        for i in range(-1,2):
            if i==n:
                continue
            stone = class_stone(i)
            stone.load("image/stone2.png",300,300,4)
            stones.append(stone)
    elif Game:
        if stones[0].y>SCREEN_HEIGHT/3 and len(stones)<=2:
            n = random.randint(-1,1)
            for i in range(-1,2):
                if i==n:
                    continue
                stone = class_stone(i)
                stone.load("image/stone2.png",300,300,4)
                stones.append(stone)
                
    for i in range(len(stones)-1,-1,-1):
        stones[i].update(ticks,SPEED)
        stones[i].draw(screen)
        if Game and stones[i].y>= SCREEN_HEIGHT/20*7 and stones[i].y <= SCREEN_HEIGHT/20*11 and ufo.locate==stones[i].track and abs(ufo.x-stones[i].x)<200:
            del stones[i]
            if shield.visable:
                stone_break.play()
                Score -= 100
                continue
            print("GameOver 遊戲結束")
            print("獲得分數:",int(Score))
            explosion_sound.play()
            Game = 0
            explosions.append(explosion(screen))
            explosions[0].load("image/exp2.png",62,62,4,ufo.x,ufo.y)
            continue
        
        if stones[i].y>SCREEN_HEIGHT:
            del stones[i]
################################
            
pygame.mixer.music.load("sound/BGM.mp3")
pygame.mixer.music.play(-1)
explosion_sound = pygame.mixer.Sound("sound/explosion.wav")           
ufo_sound = pygame.mixer.Sound("sound/pass2.wav")
stone_break = pygame.mixer.Sound("sound/stone_break.wav")
now_time = time.time()
screen.blit(bg,(-20,-20))
show_text("分數:"+str(int(Score)),0,0)
pygame.display.update()

while True:
    framerate.tick(60)
    ticks = pygame.time.get_ticks()
    key = pygame.key.get_pressed()
    #鍵盤滑鼠事件處理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button==1:#左鍵
                if Game:
                    if ufo.move_left():ufo_sound.play(0)
                    
            elif event.button==3:#右鍵
                if Game:
                    if ufo.move_right():ufo_sound.play(0)

        elif event.type == KEYDOWN:
            if event.key == K_s:
                shield.visable = True
            elif event.key == K_RIGHT or event.key == K_d:
                if ufo.move_right():ufo_sound.play(0)
            elif event.key == K_LEFT or event.key == K_a:
                if ufo.move_left():ufo_sound.play(0)
            elif event.key == K_ESCAPE:
                exit()
            elif event.key == K_SPACE:
                if Game==0:
                    print("GameStart 開始遊戲")
                    setting_init()
                    bg.set_alpha(255)
        elif event.type == KEYUP:
            if event.key == K_s:
                shield.visable = False
           
    
    

    
    
    
    
    gravel_code()
    stone_code()#隕石處理
    explosion_code()#爆炸處理
    show_text("分數:"+str(int(Score)),0,0)
    
    if Game:
        Score += SPEED#分數計算
        if time.time()-now_time >=1 and SPEED <3:
            now_time = time.time()
            SPEED *=1.1
        ufo.update(ticks)
        ufo.draw(screen)
        shield_code()
        
            
        
    if Game==False:show_text("按空白鍵開始遊戲",SCREEN_WIDTH/3,SCREEN_HEIGHT/2)
    pygame.display.update()
    screen.fill((0,0,0))
    screen.blit(bg,(-20,-20))
    

        
    

    
    
