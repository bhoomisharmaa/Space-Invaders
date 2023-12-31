import pygame
from pygame.locals import *
 
class Aliens(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        self.color = color
        self.x = x
        self.y = y

        self.file_path = '../Sprites/' + color + '.png'
        self.image = pygame.image.load(self.file_path).convert_alpha()
        self.rect = self.image.get_rect(center = (self.x,self.y))

        if self.color == 'red': self.val = 200
        elif self.color == 'green' : self.val = 100
        else: self.val = 50

    def update(self,direction):
        self.rect.x += direction

