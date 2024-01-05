import math
import sys
import time
import pygame
from enemy import Enemy
from projectile import Explosion, ProjectileController
from utils import load_image
from player import Player
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, SCREENSCALE
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
        self.font = pygame.font.Font('Assets/fonts/Evil_Empire.otf',10)
    
        #offset            
        self.offset = [0,0]
            
        #Map
        self.map = tileMap("Assets/maps/map0.json")
        
        
        #Player
        self.player = Player(5,0.3,self.map)
        
        #Enemy
        self.enemy = {Enemy(1,0.3,(300,540),self.map) for i in range (300)}
      
        #Explosions
        self.explosions:set[Explosion] = set()
        
        self.controlProjectile = ProjectileController(self.map,self.enemy,self.explosions)
        
        # Load sounds into a single channel
        self.channel = pygame.mixer.Channel(1)
                      
        #wepon
        rpg = Weapon("rpg.png",(40,15),self.player,45,self.controlProjectile,self.channel,[300,134])
        rpg2 = Weapon("rpg2.png",(40,22),self.player,0,self.controlProjectile,self.channel,[250,134])
        
        #weapons
        self.weapons = [rpg,rpg2]
               
        
    def run(self): 
        
        while True:

            self.display.fill(self.backGC)
            #self.display.blit(self.BackGroundImage, (0, 0)) 
                        
            self.offset[0] += (self.player.rect.centerx - SCREEN_WIDTH/4 - self.offset[0])/15
            self.offset[1] += (self.player.rect.centery - SCREEN_HEIGHT/4 - self.offset[1])/15

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
            
            #Projectiles
            self.controlProjectile.update()
            self.controlProjectile.render(self.display,renderOffset)
            
            #explosions
            for exp in self.explosions.copy():
                exp.animation.update()
                if(exp.animation.done):
                    self.explosions.remove(exp)
                else:
                    exp.render(self.display,renderOffset)  
                    
            
            #health Text
            healthTextSurface = self.font.render("Health", False,  (0, 0, 0))
            self.display.blit(healthTextSurface, healthTextSurface.get_rect(topleft = (265,3))) 
            pygame.draw.rect(self.display, (255,255,200), pygame.Rect(295, 5, 100, 8)) 
            pygame.draw.rect(self.display, (255,0,0), pygame.Rect(295, 5, self.player.health, 8))
                   
            
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
            
                    
            self.screen.blit(pygame.transform.scale(self.display,(SCREENSCALE*self.screen.get_size()[0],SCREENSCALE*self.screen.get_size()[1])), (0, 0))
              
            pygame.display.update()
            self.clock.tick(60)
            

if __name__ == "__main__":
    Game().run()
