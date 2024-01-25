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
        
        self.x ,self.y = 20,0    
        self.character = Spritesheet('knight/knightIdle.png','jsonImages/knight.json','#71664f')
        self.knightAttack = self.character.get_sprite_images("knightIdle")
        #self.knightIdle = self.character.get_sprite_images("knightIdle")
        
        self.animation = Animation(self.knightAttack,6,'knightAttack')
        self.pos = [(self.x,self.y+i*100) for i in range (len(self.knightAttack))]
        self.rect = self.knightAttack[0][0].get_rect(bottomleft = (610, 330))

        self.image = self.knightAttack[0][0]
        print(self.rect)
        self.offset = 0
        self.offsetx = 0
    def doAction(self,timeDelta):
        self.screen.fill("#FFFFFF")

       
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                sys.exit()    
            if events.type == pygame.MOUSEBUTTONDOWN:
                 
                if events.button == 4:  # Scroll Up
                    self.offset -=20
                elif events.button == 5:  # Scroll Down
                    self.offset +=20
                    
            if events.type == pygame.KEYDOWN:
                 
                if(events.key == pygame.K_d):
                    print(self.rect.x)
                    self.rect.x +=3
                if(events.key == pygame.K_a):  
                    self.rect.x -=3
                #self.gameStatesManager.setGameState(self.gameStatesManager.getRunningState())                
        #self.offsetx+=1            
        self.update()
        self.render()
                
        # print("Pausing")
        
        
    def update(self):
        self.animation.update()
        
        new_img = self.animation.getImage()
        new_rect = new_img[0].get_rect()
        
        # if(self.animation.get_anim_index() in [14,15,16]):
        #     self.rect.x += 1
            
        if(self.image != new_img):
            self.image = new_img
            self.rect.y = self.rect.y - (new_rect.h - self.rect.h)
            self.rect.h = new_rect.h
                   
    def render(self):
        #self.screen.blit(self.bk_image,(400,100))
        print(self.image[1])
        self.screen.blit(self.image[0],(self.rect.x+self.offsetx-self.image[1]*3,self.rect.y))  

        pygame.draw.line(self.screen,"#FF0000",(0,self.rect.y + self.rect.h),(1200,self.rect.y + self.rect.h))
        #pygame.draw.line(self.screen,"#FF0000",(self.rect.x,0),(self.rect.x,1000))
        for i,img in enumerate(self.knightAttack):   
            self.screen.blit(img[0],(self.pos[i][0],self.pos[i][1]-self.offset))  
        
        