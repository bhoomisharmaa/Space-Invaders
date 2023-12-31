import pygame,sys

from pygame.sprite import AbstractGroup

class Laser(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load('../Sprites/laser.png').convert_alpha()
        self.rect = self.image.get_rect(center = (x,y))

    def update(self,direction):
        self.rect.y += direction
