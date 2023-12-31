from typing import Any
import pygame,sys

from pygame.sprite import AbstractGroup

class HealthSystem(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load("../Sprites/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(40,25))
        self.rect = self.image.get_rect(center = (self.x,self.y))