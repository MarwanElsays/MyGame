import sys
import pygame
from GameStates.gameState import GameState
from animation import Animation
from utils import Spritesheet, load_image, load_image_alpha

class PauseState(GameState):
    
    def __init__(self, gameStatesManager , screen) -> None:
        super().__init__(gameStatesManager,screen)
       
    def intiallize(self):
        # self.character = Spritesheet('knight/KnightAttack.png','jsonImages/knight.json','#71664f')
        # self.knightAttack = self.character.get_sprite_images("knightAttack")
        # self.animation = Animation(self.knightAttack,4,'knightAttack')
        self.bk_image = load_image_alpha('menu/pinkBorder1.png',(400,500))
        
                    
        self.character = Spritesheet('knight/KnightAttack.png','jsonImages/knight.json','#71664f')
        self.knightAttack = self.character.get_sprite_images("knightAttack")
        self.animation = Animation(self.knightAttack,6,'knightAttack')
        
    def doAction(self,timeDelta):
        self.screen.fill("#FFFFFF")
        
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                sys.exit()    
            if events.type == pygame.MOUSEBUTTONDOWN:
                self.gameStatesManager.setGameState(self.gameStatesManager.getRunningState())
                     
        self.update()
        self.render()
                
        # print("Pausing")
        
    def update(self):
        self.animation.update()
        self.image = self.animation.getImage()
        self.rect = self.image.get_rect(center = (610, 330))
        
    
    def render(self):
       self.screen.blit(self.bk_image,(400,100))    
       self.screen.blit(self.image,(self.rect.x,self.rect.y))  
       