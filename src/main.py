import math
import sys
import pygame
from enemy import Enemy
from projectile import ProjectileController
from utils import load_image
from player import Player
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from tileMap import tileMap
from weapon import Weapon

class Game:
    
    def __init__(self):
        pygame.init()
        self.backGC = '#C4FAF8'
        self.screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
        self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.BackGroundImage = load_image('background.png')
        
        pygame.display.set_caption("Maro Game")
        self.clock = pygame.time.Clock()
        
        #Font
        self.font = pygame.font.Font('Assets/fonts/regular_font.otf',10)
        self.font.bold = True
        
        self.offset = [0,0]
            
        #Map
        self.map = tileMap("Assets/maps/map0.json")
        
        #Player
        self.player = Player(3,0.3,self.map)
        
        #Enemy
        self.enemy = [Enemy(1,0.3,self.map),Enemy(1,0.3,self.map),Enemy(1,0.3,self.map),Enemy(1,0.3,self.map)]
        
        self.controlProjectile = ProjectileController(self.map)
        
        # Load sounds into a single channel
        self.channel = pygame.mixer.Channel(1)
                      
        #wepon
        rpg = Weapon("rpg.png",(30,10),self.player,45,self.controlProjectile,self.channel,[300,134])
        rpg2 = Weapon("rpg2.png",(30,17),self.player,0,self.controlProjectile,self.channel,[250,134])
        
        self.weapons = [rpg,rpg2]
        
        
    def run(self): 
        
        while True:

            self.display.fill(self.backGC)
            #self.display.blit(self.BackGroundImage, (0, 0)) 
                        
            self.offset[0] += (self.player.rect.centerx - SCREEN_WIDTH/6 - self.offset[0])/15
            self.offset[1] += (self.player.rect.centery - SCREEN_HEIGHT/6 - self.offset[1])/15

            renderOffset = (int(self.offset[0]),int(self.offset[1]))
                        
            #Map
            self.map.update()
            self.map.render(self.display,renderOffset)
            
            #Player
            self.player.update()
            self.player.render(self.display,renderOffset)
            
            #enemies
            for enem in self.enemy:
                enem.update()
                enem.render(self.display,renderOffset)
                
            #wepon
            for weapon in self.weapons:
                weapon.update()
                weapon.render(self.display,renderOffset)  
                   
            
            self.controlProjectile.update()
            self.controlProjectile.render(self.display,renderOffset)
            
            # #health Text
            # healthTextSurface = self.font.render("Health", True, (255,0,0))
            # self.display.blit(healthTextSurface, healthTextSurface.get_rect(center = (220,10)))    
                   
            
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
                if events.type == pygame.MOUSEBUTTONDOWN:
                    pass
                if events.type == pygame.KEYDOWN:
                    if(events.key == pygame.K_e):
                        self.player.equipping = not self.player.equipping
                    if(events.key == pygame.K_1):
                        self.player.launchMissile()
            
                    
            self.screen.blit(pygame.transform.scale(self.display, (3*self.screen.get_size()[0],3*self.screen.get_size()[1])), (0, 0))
              
            pygame.display.update()
            self.clock.tick(60)
            

if __name__ == "__main__":
    Game().run()
