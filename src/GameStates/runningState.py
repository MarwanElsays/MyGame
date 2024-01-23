import pygame
from GameStates.gameState import GameState
import sys
from animation import Animation
from enemy import Enemy
from projectile import Explosion, ProjectileController
from utils import Spritesheet, load_image
from player import Player
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, SCREENSCALE
from tileMap import tileMap
from weapon import Weapon

class RunningState(GameState):
    
    def __init__(self, gameStatesManager, screen) -> None:
        super().__init__(gameStatesManager,screen)
           
    def intiallize(self):
        
        self.backGC = '#000999'
        self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.BackGroundImage = load_image('background.png')
                
        #Font
        self.font = pygame.font.Font('Assets/fonts/Evil_Empire.otf',10)
    
        #offset            
        self.offset = [0,0]
            
        #Map
        self.map = tileMap("Assets/maps/map0.json")
        
        #Player
        self.player = Player(5,0.3,self.map)
        
        #Enemy
        self.enemy = {Enemy(1,0.3,(2547, 620),self.map) for i in range (300)}
      
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
                
        self.tree  =  pygame.image.load('Assets/images/tiles/Trees/Tree1.png').convert_alpha()
        
            
        self.character = Spritesheet('knight/KnightAttack.png','jsonImages/knight.json','#71664f')
        self.knightAttack = self.character.get_sprite_images("knightAttack")
        self.animation = Animation(self.knightAttack,4,'knightAttack')
               
            
    def run(self): 
        
        self.display.fill(self.backGC)
        #self.display.blit(self.BackGroundImage, (0, 0)) 
                    
        self.offset[0] += (self.player.get_rect().centerx - SCREEN_WIDTH/4 - self.offset[0])/15
        self.offset[1] += (self.player.get_rect().centery - SCREEN_HEIGHT/4 - self.offset[1])/15

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
        pygame.draw.rect(self.display, (255,0,0), pygame.Rect(295, 5, self.player.get_health(), 8))
        
        
        # self.display.blit(self.tree,( 300 - renderOffset[0],400 - renderOffset[1]))
        self.knight_update() 
        self.knight_render(self.display,renderOffset)     
        
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            if events.type == pygame.MOUSEBUTTONDOWN:
                self.gameStatesManager.getPauseState().intiallize()
                self.gameStatesManager.setGameState(self.gameStatesManager.getPauseState())
            if events.type == pygame.KEYDOWN:
                if(events.key == pygame.K_e):
                    self.player.set_equipping(not self.player.get_equipping())
                if(events.key == pygame.K_1):
                    self.player.launch_missile()
        
                
        self.screen.blit(pygame.transform.scale(self.display,(SCREENSCALE*self.screen.get_size()[0],SCREENSCALE*self.screen.get_size()[1])), (0, 0))
            
        #pygame.display.update()
        #self.clock.tick(60)
        
        
    def knight_update(self):
        self.animation.update()
        self.image = self.animation.getImage()
        self.rect = self.image.get_rect(center = (300, 200))
    
    def knight_render(self,display,renderOffset):
       display.blit(self.image,(self.rect.x-renderOffset[0],self.rect.y-renderOffset[1]))  
               
    def doAction(self,timeDelta):
        self.run()
    