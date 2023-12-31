import pygame,sys
from pygame.locals import *
import random
from Aliens import*
from player import Player
from laser import Laser
from healthSystem import HealthSystem

pygame.init()
screen_height = 600
screen_width = 600
pygame.display.set_caption("Space Invader")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_height,screen_width))
gameActive = False

class MainGame():
    def __init__(self):
        #aliens
        self.aliens = pygame.sprite.Group()
        self.direction = 1
        self.x = 20
        self.y = 100
        self.alien_setup(rows = 6, cols = 8)
        self.direction = 1
        self.alienCount = 47

        #player
        self.player = Player(300,584)

        #game over screen
        self.victory = False #returns true if player won
        self.lose = False #returns true if player lost

        #collision rect
        self.rect = pygame.sprite.Group()
        self.rect1 = Sprite(x = 0,y = 30)
        self.rect2 = Sprite(x = 595,y = 30)
        self.rect.add(self.rect1)
        self.rect.add(self.rect2)

        #laser
        self.player_laser = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.laser()

        #score
        self.score = 0

        #font
        self.game_font = pygame.font.Font("../Sprites/Pixeled.TTF",18)
        self.score_surface = self.game_font.render("Score: " + str(self.score),True,(255,255,255))
        self.score_rect = self.score_surface.get_rect(midleft = (8,15))
        self.victory_msg = self.game_font.render("YOU WON!",True,(255,255,255))
        self.victory_rect = self.victory_msg.get_rect(center = (300,300))
        self.gameOver = self.game_font.render("GAME OVER!",True,(255,255,255))
        self.gameOver_rect = self.gameOver.get_rect(center = (300,300))

        self.liveCount = 3
        self.heathSprites = pygame.sprite.Group()
        self.healthSystem()

        #sound 
        self.music = pygame.mixer.Sound('../sound/music.wav')
        self.music.set_volume(0.2)
        self.music.play(loops = -1)
        self.explosionSound = pygame.mixer.Sound('../sound/explosion.wav')
        self.laserSound = pygame.mixer.Sound('../sound/laser.wav')
        
    def alien_setup(self,rows,cols,dist_x = 60,dist_y = 50):
        for row_no, row in enumerate(range(0,rows)):
            for col_no, col in enumerate(range(0,cols)):
                self.x += dist_x  

                if row_no < 1: color = 'yellow'
                elif 1 <= row_no <= 2: color = 'green'
                else: color = 'red'

                alien_sp =  Aliens(color, self.x, self.y)
                self.aliens.add(alien_sp)

            self.y += dist_y  
            self.x = 20

    def laser(self):  
        playerlaser = Laser(self.player.rect.x + 29,self.player.rect.y)
        self.player_laser.add(playerlaser)
        
        if not self.victory and not self.lose:
            alien_index = random.randint(0,self.alienCount)
            alienlaser = Laser(self.aliens.sprites()[alien_index].rect.x + 29,self.aliens.sprites()[alien_index].rect.y + 35)
            self.alien_lasers.add(alienlaser)

    def scroll_x(self):
        if pygame.sprite.groupcollide(self.aliens,self.rect,False,False):
            self.direction *= -1

    def check_collision(self):
        #to check collision between aliens and player lasers
        collisionAlien = pygame.sprite.groupcollide(self.aliens.sprites(),self.player_laser.sprites(),False,False)
        if collisionAlien:
            for sprite,laser in collisionAlien.items():
                self.score += 10
                self.player_laser.remove(laser)
                self.aliens.remove(sprite)
                self.alienCount -= 1
                self.laserSound.play()

        if self.alienCount < 0: self.victory = True

        #to check collision between player and alien lasers
        for laser in self.alien_lasers.sprites():
            if pygame.sprite.spritecollide(self.player,self.alien_lasers.sprites(),False):
                self.alien_lasers.remove(laser)
                self.liveCount -= 1
                if self.liveCount >= 0: self.heathSprites.remove(self.heathSprites.sprites()[0])
                else: self.lose = True
                self.explosionSound.play()

    def healthSystem(self):
        x = 450
        y = 15
        for i in range(1,4):
            sprite = HealthSystem(x,y)
            self.heathSprites.add(sprite)
            x += 60
                
    def update(self):
        #update all the sprites

        #player
        self.player.update(screen)

        #aliens
        self.aliens.draw(screen)
        self.scroll_x()
        self.aliens.update(self.direction)
        
        #laser
        if not self.victory and not self.lose:
            self.player_laser.draw(screen)
            self.player_laser.update(-5)
            self.alien_lasers.draw(screen)
            self.alien_lasers.update(5)
        #to remove laser sprite if it is out of game screen
        for sprite in self.alien_lasers.sprites():
            if sprite.rect.y >= 600: self.alien_lasers.remove(sprite)
        for sprite in self.player_laser.sprites():
            if sprite.rect.y <= 0: self.player_laser.remove(sprite)

        self.check_collision()

        #font
        self.score_surface = self.game_font.render("Score: " + str(self.score),True,(255,255,255))
        screen.blit(self.score_surface,self.score_rect)
        if self.victory: screen.blit(self.victory_msg,self.victory_rect)
        if self.lose: screen.blit(self.gameOver,self.gameOver_rect)


        #healthSystem
        self.heathSprites.draw(screen)

class Sprite(pygame.sprite.Sprite):
    def __init__(self,x,y,height = 500, width = 5):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect(center = (x,y))
        
game = MainGame()
SPAWNBULLET = pygame.USEREVENT
pygame.time.set_timer(SPAWNBULLET,1500)

while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWNBULLET:
            game.laser()

    screen.fill('black')
    game.update()

    pygame.display.update()
    clock.tick(60)