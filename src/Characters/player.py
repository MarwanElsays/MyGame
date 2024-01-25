import pygame
from animation import Animation
from utils import load_images
from settings import PSCALE, SCALE,GRAVITY
from weapon import Weapon

class Player():
    def __init__(self,speedx,tile_map):
        self.__speedX ,self.__speedY = speedx, 0
        self.__tile_map = tile_map
        self.__gravity = GRAVITY
        self.__dir = [0,0]
        self.__collision = [0,0,0,0]  #down,top,left,right
        
        #health
        self.__MAXHEALTH = 100
        self.__health = self.__MAXHEALTH/2
        
        #Jumps
        self.__MAXJUMPS = 2
        self.__jumps = self.__MAXJUMPS
        self.__can_jump = True
        
        #animation
        self.__flip = False    
        self.__scale = (SCALE*16,SCALE*20)  
        self.__animations = {"idle" : Animation(load_images('Player/idle',self.__scale),10,'idle'),
                           "jump" : Animation(load_images('Player/jump',self.__scale),10,'jump'),
                           "run" : Animation(load_images('Player/run',self.__scale),5,'run'),
                           "slide" : Animation(load_images('Player/slide',self.__scale),10,'slide'),
                           "wall_slide" : Animation(load_images('Player/wall_slide',self.__scale),10,'wall_slide')}
        
        self.__curr_animation =  self.__animations['idle']
        self.__image = self.__curr_animation.getImage()
        self.__rect = self.__image.get_rect(topleft = (300, 200))
                    
        #Wall sldie
        self.__WALLSLIDESPEED = 2
        
        #Ground Slide
        self.__slide = 0
        self.__slide_time = 30
        self.__slide_offset = 0
        self.__can_slide = False
        self.__slide_cnt = 0
        
        #climb
        self.__CLIMBSPEED = -4
        self.__can_climb = False
        
        #Wepon
        self.__wepon:Weapon= None
        self.__equipping = False
    
    
    def get_wepon(self)->Weapon:
        return self.__wepon
    
    def get_health(self):
        return self.__health
    
    def get_flip(self):
        return self.__flip
    
    def get_rect(self):
        return self.__rect
    
    def get_equipping(self):
        return self.__equipping
    
    def set_equipping(self,equipping):
        self.__equipping = equipping

    def set_wepon(self,wepon):
        self.__wepon = wepon
        
            
    def get_input(self):
        
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_RIGHT]): 
            self.__dir[0] = 1
            self.__flip = False
        elif(keys[pygame.K_LEFT]): 
            self.__dir[0] = -1
            self.__flip = True 
        else:
            self.__dir[0] = 0
            
        if(keys[pygame.K_UP]): 
            self.__can_climb = True
        else:
            self.__can_climb = False
            
        if(keys[pygame.K_x] and self.__dir[0] != 0 and self.__can_slide):
            self.__slide = 1
            self.__slide_cnt = 0
            self.__can_slide = False
        
        if(keys[pygame.K_SPACE] and self.__jumps > 0 and self.__can_jump): 
            self.__speedY = -6*PSCALE
            self.__collision[0] = 0
            self.__jumps-=1
            self.__can_jump = False
            
        if(not keys[pygame.K_SPACE]):
            self.__can_jump = True
            
        if(not keys[pygame.K_x]):
            self.__can_slide = True
                               
    def launch_missile(self):
        if (self.__wepon is not None):
            self.__wepon.launch()    
                                
    def get_animation(self):
        new_anim = ''
        
        if(not self.__collision[0]):
            if(any([self.__collision[2],self.__collision[3]])):
                if(self.__can_climb):
                    new_anim = 'idle'   # need to add climb animation
                else:
                    if(self.__speedY > 0):
                        new_anim = 'wall_slide'
                        self.__slide_offset = 3 * self.__dir[0]
                    else:
                        new_anim = 'jump'
                        self.__slide_offset = 0
            else:
                new_anim = 'jump'
                self.__slide_offset = 0
                
        elif(self.__slide):
            new_anim = 'slide'
        elif(self.__dir[0] == 0):
            new_anim = 'idle'
        else:
            new_anim = 'run'
            
        if(new_anim == self.__curr_animation.status):
            self.__curr_animation.update()
        else:
            self.__curr_animation.imageIdx = 0
            self.__curr_animation = self.__animations[new_anim]
            
        self.__image = self.__curr_animation.getImage()
        
    def control_slide(self):
        self.__slide_cnt+=1
        if(self.__slide_cnt >= self.__slide_time):
            self.__slide = 0
            self.__slide_cnt = self.__slide_time 
            
    def check_collisions(self, direction):
        if direction == "horizontal":
            for rect in self.__tile_map.getAroundTiles(self.__rect.center):
                if(self.__rect.colliderect(rect)):
                    if(self.__dir[0] == 1):
                        self.__collision[3] = 1
                        self.__rect.right = rect.left
                    if(self.__dir[0] == -1):
                        self.__collision[2] = 1
                        self.__rect.left = rect.right
                    self.__slide = 0
        elif direction == "vertical":
            for rect in self.__tile_map.getAroundTiles(self.__rect.center):
                if(self.__rect.colliderect(rect)):
                    if(self.__speedY >= 0):
                        self.__collision[0] = 1
                        self.__rect.bottom = rect.top
                    if(self.__speedY < 0):
                        self.__collision[1] = 1
                        self.__rect.top = rect.bottom
                    self.__speedY = 1
       
                    
    def handle_collision(self):
        if(self.__collision[1]):  #upWall bounce
            self.__speedY+=2
        
        if(self.__collision[2] or self.__collision[3]):
            if(self.__speedY > 0):                           #handle wall slide      
                self.__speedY = self.__WALLSLIDESPEED        #he can jump of wall when sliding
        
            if self.__can_climb : 
                self.__speedY = self.__CLIMBSPEED        
                self.__jumps = 0         #prevent player from jumping when climbing 
        else:
            self.__can_climb = False     #if player is not on left or right Wall then he cant climb
                   
        if(self.__collision[0]): 
            self.__jumps = self.__MAXJUMPS  
            self.__speedY,self.__can_climb = 1,False     #prevent player from climbing when on ground
        elif(not self.__can_climb):
            self.__speedY += self.__gravity
            self.__speedY = min(9*PSCALE,self.__speedY)   
                 
                                     
    def update(self):
        prev_col = self.__collision
        self.__collision = [0,0,0,0]
        
        self.get_input()
    
        self.control_slide()
        
        self.__rect.x += self.__dir[0] * self.__speedX * (2 if self.__slide else 1)
        self.check_collisions("horizontal")
                                      
        self.__rect.y += self.__speedY         
        self.check_collisions("vertical")
                                                           
        self.handle_collision()  
                
        self.get_animation() 
               

    def render(self,screen,offset):
        screen.blit(pygame.transform.flip(self.__image,self.__flip,False),(self.__rect.x - offset[0]+self.__slide_offset,self.__rect.y - offset[1]))