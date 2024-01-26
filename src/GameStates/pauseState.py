import sys
import pygame
from GameStates.gameState import GameState
from animation import Animation
from utils import Spritesheet, load_image, load_image_alpha

class PauseState(GameState):
    
    def __init__(self, gameStatesManager , screen) -> None:
        super().__init__(gameStatesManager,screen)
       
    def intiallize(self):
       
        self.bk_image = load_image_alpha('menu/pinkBorder1.png',(400,500))
        
        self.x ,self.y = 20,0  
        self.scale = (3,3)  
        self.knight_idle_sheet = Spritesheet('knight/knightIdle.png','jsonImages/knight.json','#71664f',self.scale) 
        self.knight_attack_sheet = Spritesheet('knight/knightAttack.png','jsonImages/knight.json','#71664f',self.scale) 
        self.animations = {
            "idle" : Animation(self.knight_idle_sheet.get_sprite_images("knightIdle"),6,'idle'),
            "attack" : Animation(self.knight_attack_sheet.get_sprite_images("knightAttack"),6,'attack')
        }
        
        # self.pos = [(self.x,self.y+i*100) for i in range (len(self.knightAttack))]
        self.curr_animation =  self.animations['idle']
        self.image = self.curr_animation.getImage()
        self.rect = self.image[0].get_rect(bottomleft = (610, 330))

        self.offset = 0
        self.offsetx = 0
        self.flip = True
        
    def doAction(self,timeDelta):
        self.screen.fill("#FFFFFF")

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                sys.exit()    
            if events.type == pygame.MOUSEBUTTONDOWN: 
                self.flip = not self.flip
                    
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
        self.curr_animation.update()
        
        new_img = self.curr_animation.getImage()
        new_rect = new_img[0].get_rect()
        
        # if(self.animation.get_anim_index() in [14,15,16]):
        #     self.rect.x += 1
            
        if(self.image != new_img):
            self.image = new_img
            self.rect.y = self.rect.y - (new_rect.h - self.rect.h)
            self.rect.h = new_rect.h
                   
    def render(self):
        #self.screen.blit(self.bk_image,(400,100))
        
        img_offset = 0
        if self.flip:
            img_offset = -(self.image[0].get_rect().w - 35) + self.image[1] * self.scale[0]
        else:   
            img_offset = -self.image[1] * self.scale[0]
            
        self.screen.blit(pygame.transform.flip(self.image[0],self.flip,False)
                    ,(self.rect.x -  self.offsetx + img_offset,self.rect.y )) 

        pygame.draw.line(self.screen,"#FF0000",(0,self.rect.y + self.rect.h),(1200,self.rect.y + self.rect.h))
        pygame.draw.line(self.screen,"#FF0000",(self.rect.x,0),(self.rect.x,1000))
        
        # for i,img in enumerate(self.knightAttack):   
        #     self.screen.blit(img[0],(self.pos[i][0],self.pos[i][1]-self.offset))  
        
        