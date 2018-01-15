import random, pygame, sys,time,math
from setting import *



class Anime(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)
        self.target_surface = target
        self.image = None
        self.master_image = None
        self.rect = None
        self.topleft = 0,0
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1     
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.x = 0
        self.y = 0
        #---------------
        self.width = 0
        self.height = 0
        self.locate = 0

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.width = int(SCREEN_WIDTH/4)
        self.height = int(SCREEN_HEIGHT/5)
        self.x = SCREEN_WIDTH/2 - SCREEN_WIDTH/8
        self.y = SCREEN_HEIGHT/2
        self.frame_width = width
        self.frame_height = height
        self.rect = 0,0,width,height
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1
    def update(self, current_time, rate=30):
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        if self.frame != self.old_frame:
            self.rect = self.x,self.y,self.frame_width,self.frame_height
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = ( frame_x, frame_y, self.frame_width, self.frame_height )
            self.image = self.master_image.subsurface(rect)
            self.image = pygame.transform.scale(self.image,(self.width,self.height))
            self.old_frame = self.frame

        w = SCREEN_WIDTH
        self.x+= int(((w/2+self.locate*w/3)-(self.x+self.width/2))/6)#左右移動動畫處理
        
    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))

    def move_right(self):
        
        if self.locate<1:
            self.locate +=1
            return True

    def move_left(self):
        if self.locate>-1:
            self.locate -=1
            return True
