import random, pygame, sys,time ,math
from setting import *
class class_stone(pygame.sprite.Sprite):
    def __init__(self,track):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.master_image = None
        self.rect = None
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
        self.track = track
        self.width = 0
        self.height = 0
        self.distance = 0.1
        
    def load(self, filename, width, height, columns):
        self.width = 1
        self.height = 1
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.x = SCREEN_WIDTH/2 - self.width/2 + self.track*self.width
        self.y = 30
        self.frame_width = width
        self.frame_height = height
        self.rect = 0,0,width,height
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1
    def update(self, current_time,speed=None, rate=40):
        self.distance += speed
        self.y += self.distance
        self.x = self.x + self.track*self.distance - self.distance/2
        self.width += int(self.distance)
        self.height += int(self.distance)
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
            self.old_frame = self.frame
            
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        
    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))

   
