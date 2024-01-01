import os
import pygame, sys, math
from animation import Animation

from settings import GRAVITY
from utils import load_image


class Projectile():
    
    def __init__(self,mass,imageFilePath,scale,angle,flip,intialPos = [0 , 300]):
        
        #image
        self.image = load_image(f'wepons/{imageFilePath}',scale)
        self.rect = self.image.get_rect(center = (intialPos[0],intialPos[1]))
        self.rect.width = max(scale[0],scale[1]) - 2
        self.rect.height = max(scale[0],scale[1]) - 2
        
        self.flip = flip
        
        self.delta_t = 0.03
        self.mass = mass
        self.force = [0 , self.mass * GRAVITY]
        self.pos = intialPos
        
        self.angle = angle
        self.theta = math.radians(self.angle)

        v = 100
        self.velocity = [v * math.cos(self.theta), -v * math.sin(self.theta)]   #vx = vcos0 , vy = vsin0
        
    
    def detectCollision(self,tileMap):
        collide = False
        for rect in tileMap.getAroundTiles(self.rect.center): 
            if rect.colliderect(self.rect):
                collide = True
                break    
            
        return collide       
    
    def updateAngle(self):  #get angle with ground ,shiftTan(vy/vx)
        self.angle = -1 * math.atan(self.velocity[1]/self.velocity[0]) * 180 / math.pi      
        self.theta = math.radians(self.angle)
        
    def update(self):
        
        self.velocity[0] = self.velocity[0] + (self.force[0] / self.mass) * self.delta_t       #v = v0 + at
        self.velocity[1] = self.velocity[1] + (self.force[1] / self.mass) * self.delta_t

        self.pos[0] = self.pos[0] + self.velocity[0] * self.delta_t
        self.pos[1] = self.pos[1] + self.velocity[1] * self.delta_t
        
        self.rect[0] = self.pos[0]
        self.rect[1] = self.pos[1]
        
        self.updateAngle()
        #print(math.atan(self.velocity[1]/self.velocity[0]) * 180 / math.pi)
        #print(self.velocity)
        
        
    def render(self,screen:pygame.Surface,offset):
        screen.blit(pygame.transform.flip(pygame.transform.rotate(self.image,self.angle),self.flip,self.flip),
                    (self.pos[0] - offset[0],self.pos[1] - offset[1]))
        
        #pygame.draw.rect(screen,(255,0,0),(self.rect[0] - offset[0], self.rect[1] - offset[1], self.rect[2], self.rect[3]))


class ProjectileController():
    
    def __init__(self,tileMap):
        
        self.tileMap = tileMap
        self.missiles:list[Projectile] = []
        
    def addMissile(self,projectile:Projectile):
        self.missiles.append(projectile)
        
    def update(self):
        for missile in self.missiles:
            if(missile.pos[1] > 2000) or missile.detectCollision(self.tileMap):
                print('projectile removed')
                self.missiles.remove(missile)
            
            missile.update()
            
    def render(self,screen,renderOffset):  
        for missile in self.missiles:  
            missile.render(screen,renderOffset)  
                        


class Explosion:
    
    def __init__(self,folderPath):
        
        self.images = self.loadImages(folderPath)
        self.animation = Animation(self.images,12)
    
    def loadImages(self,folderPath):
        return [load_image(f) for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, f))]
        
        