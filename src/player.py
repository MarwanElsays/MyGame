import math
import pygame
from animation import Animation
from utils import load_images
from settings import SCALE
from weapon import Weapon

class Player():
    def __init__(self,speedx,gravity,tileMap):
        self.speedX = speedx
        self.speedY = 0
        self.tileMap = tileMap
        self.gravity = gravity
        self.dir = [0,0]
        self.collision = [0,0,0,0]  #down,top,left,right
        
        #health
        MAXHEALTH = 100
        self.health = MAXHEALTH/2
        
        #Jumps
        self.jumps = 2
        self.canJump = True
        
        #animation
        self.flip = False    
        self.scale = (SCALE*16,SCALE*20)  
        self.Animations = {"idle" : Animation(load_images('Player/idle',self.scale),10,'idle'),
                           "jump" : Animation(load_images('Player/jump',self.scale),10,'jump'),
                           "run" : Animation(load_images('Player/run',self.scale),5,'run'),
                           "slide" : Animation(load_images('Player/slide',self.scale),10,'slide'),
                           "wall_slide" : Animation(load_images('Player/wall_slide',self.scale),10,'wall_slide')}
        
        self.currAnimation =  self.Animations['idle']
        self.image = self.currAnimation.getImage()
        self.rect = self.image.get_rect(center = (300, 200))
        
        #Slide
        self.slide = 0
        self.slideTime = 30
        self.slideoffset = 0
        self.canSlide = False
        self.slideCnt = 0
        
        #climb
        self.canClimb = False
        
        #Wepon
        self.__wepon:Weapon= None
        self.equipping = False
        
        
    def setWepon(self,wepon):
        self.__wepon = wepon
        
    def getWepon(self)->Weapon:
        return self.__wepon
            
    def getInput(self):
        
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_RIGHT]): 
            self.dir[0] = 1
            self.flip = False
        elif(keys[pygame.K_LEFT]): 
            self.dir[0] = -1
            self.flip = True
            
        else:
            self.dir[0] = 0
            
        if(keys[pygame.K_UP]): 
            self.canClimb = True
        else:
            self.canClimb = False
            
        if(keys[pygame.K_x] and self.dir[0] != 0 and self.canSlide):
            self.slide = 1
            self.slideCnt = 0
            self.canSlide = False
        
        if(keys[pygame.K_SPACE] and self.jumps > 0 and self.canJump): 
            self.speedY = -6*SCALE
            self.collision[0] = 0
            self.jumps-=1
            self.canJump = False
            
        if(not keys[pygame.K_SPACE]):
            self.canJump = True
            
        if(not keys[pygame.K_x]):
            self.canSlide = True
                               
    def launchMissile(self):
        if (self.__wepon is not None):
            self.__wepon.launch()    
                                
    def getAnimation(self):
        newAnim = ''
        
        if(not self.collision[0]):
            if((self.collision[2] or self.collision[3])):
                if(self.canClimb):
                    newAnim = 'idle'   # need to add climb animation
                else:
                    if(self.speedY > 0):
                        newAnim = 'wall_slide'
                        self.slideoffset = 3 * self.dir[0]
                    else:
                        newAnim = 'jump'
                        self.slideoffset = 0
            else:
                newAnim = 'jump'
                self.slideoffset = 0
                
        elif(self.slide):
            newAnim = 'slide'
        elif(self.dir[0] == 0):
            newAnim = 'idle'
        else:
            newAnim = 'run'
            
        if(newAnim == self.currAnimation.status):
            self.currAnimation.update()
        else:
            self.currAnimation.imageIdx = 0
            self.currAnimation = self.Animations[newAnim]
            
        self.image = self.currAnimation.getImage()
        
    def Controlslide(self):
        self.slideCnt+=1
        if(self.slideCnt >= self.slideTime):
            self.slide = 0
            self.slideCnt = self.slideTime 
                 
    def update(self):
        self.collision = [0,0,0,0]
        
        self.getInput()
    
        self.Controlslide()
        if(self.slide):
            self.rect.x += self.dir[0] * self.speedX * 2 
        else:
            self.rect.x += self.dir[0] * self.speedX 
             
        for rect in self.tileMap.getAroundTiles(self.rect.center):
            if(self.rect.colliderect(rect)):
                if(self.dir[0] == 1):
                    self.collision[3] = 1
                    self.rect.right = rect.left
                if(self.dir[0] == -1):
                    self.collision[2] = 1
                    self.rect.left = rect.right
                self.slide = 0
                                      
        self.rect.y += self.speedY         
        colRect = pygame.rect.Rect(self.rect)
        if(self.speedY < 0.5 and self.speedY >= 0): colRect.y+=1
    
        for rect in self.tileMap.getAroundTiles(self.rect.center):
            if(colRect.colliderect(rect)):
                if(self.speedY >= 0):
                    self.collision[0] = 1
                    colRect.bottom = rect.top
                if(self.speedY < 0):
                    self.collision[1] = 1
                    colRect.top = rect.bottom
                self.rect = colRect
                self.speedY = 0                     
                          
                          
        if(self.collision[1]):  #upWall bounce
            self.speedY+=2
        
        if((self.collision[2] or self.collision[3]) and self.speedY > 0): #wallSlide
            if(self.canClimb):
                self.speedY = -3
            else:
                self.speedY = 1

        #if player is not on left or right Wall then he cant climb
        if(not(self.collision[2] or self.collision[3])): 
            self.canClimb = False
                    
        if(self.collision[0]): 
            self.jumps = 2   
            self.canClimb = False     #prevent player from climbing when on ground
        else:
            if(not self.canClimb):
                self.speedY += self.gravity
                self.speedY = min(9*SCALE,self.speedY)  
               
        self.getAnimation() 

    def render(self,screen,offset):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),(self.rect.x - offset[0]+self.slideoffset,self.rect.y - offset[1]))

    
    
    