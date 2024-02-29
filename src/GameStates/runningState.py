import pygame
from Characters.knight import Knight
from GameStates.gameState import GameState
import sys
from animation import Animation
from enemy import Enemy
from projectile import Explosion, ProjectileController
from utils import Spritesheet, load_image
from Characters.player import Player
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, SCREENSCALE
from tileMap import tileMap
from weapon import Weapon

class RunningState(GameState):
    
    def __init__(self, gameStatesManager, screen) -> None:
        super().__init__(gameStatesManager,screen)
           
    def intiallize(self,character = "player"):
        
        self.backGC = '#00FFBB'
        self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.BackGroundImage = load_image('background.png')
                
        #Font
        self.font = pygame.font.Font('Assets/fonts/Evil_Empire.otf',10)
    
        #offset            
        self.offset = [0,0]
            
        #Map
        self.map = tileMap("Assets/maps/map0.json")
        
        #Player
        if character == "player":
            self.player = Player(6,self.map)
        elif character == "Knight":
            self.player = Knight(6,self.map)
            
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
                      
            
    def run(self,timeDelta): 

        self.display.fill(self.backGC)
        #self.display.blit(self.BackGroundImage, (0, 0)) 
        # print(abs(self.player.get_rect().centery - SCREEN_HEIGHT/4 - self.offset[1]))         
        self.offset[0] += (self.player.get_rect().centerx - SCREEN_WIDTH/4 - self.offset[0])/15
        if(abs(self.player.get_rect().centery - SCREEN_HEIGHT/4 - self.offset[1]) > 4):
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
        
    def doAction(self,timeDelta):
        self.run(timeDelta)
    