import pygame,sys

from pygame.sprite import AbstractGroup

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.player = pygame.image.load('../Sprites/player.png').convert_alpha()
        self.rect = self.player.get_rect(center = (self.x,self.y))

    def player_movements(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right < 596:
            self.rect.centerx += 3
        elif keys[pygame.K_LEFT] and self.rect.left > 3:
            self.rect.centerx -= 3

    def update(self,surface):
        surface.blit(self.player,self.rect)
        self.player_movements()