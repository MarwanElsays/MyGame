import os
import pygame, math
from animation import Animation

from settings import GRAVITY
from utils import load_image, load_images


class Projectile():
    
    def __init__(self,mass,imageFilePath,scale,angle,flip,intialPos = [0 , 300]):
        
        #image
        self.image = load_image(f'wepons/{imageFilePath}',scale)
        self.rect = self.image.get_rect(topleft = (intialPos[0],intialPos[1]))
        self.rect.width = max(scale[0],scale[1]) - 7    #Adjust rect to be in middle
        self.rect.height = max(scale[0],scale[1]) - 7   #Adjust rect to be in middle
        
        self.flip = flip
        
        self.delta_t = 0.03
        self.mass = mass
        self.force = [0 , self.mass * GRAVITY]
        self.pos = intialPos
        
        self.angle = angle
        self.theta = math.radians(self.angle)

        v = 140
        self.velocity = [v * math.cos(self.theta), -v * math.sin(self.theta)]   #vx = vcos0 , vy = vsin0
        
    
    def detectCollision(self,tileMap):
        collide = False
        for rect in tileMap.getAroundTiles(self.rect.center): 
            if rect.colliderect(self.rect):
                collide = True
                break    
            
        return collide  
    
    def getExplosionPoint(self):  
        print(self.velocity)
        if self.velocity[0] > 0 and self.velocity[1] < 0 : return self.rect.topright
        if self.velocity[0] < 0 and self.velocity[1] < 0 : return self.rect.topleft
        if self.velocity[0] < 0 and self.velocity[1] > 0 : return self.rect.bottomleft
        if self.velocity[0] > 0 and self.velocity[1] > 0 : return self.rect.bottomright
    
    def updateAngle(self):  #get angle with ground ,shiftTan(vy/vx)
        self.angle = -1 * math.atan(self.velocity[1]/self.velocity[0]) * 180 / math.pi      
        self.theta = math.radians(self.angle)
        
    def update(self):
        
        self.velocity[0] = self.velocity[0] + (self.force[0] / self.mass) * self.delta_t       #v = v0 + at
        self.velocity[1] = self.velocity[1] + (self.force[1] / self.mass) * self.delta_t

        self.pos[0] = self.pos[0] + self.velocity[0] * self.delta_t
        self.pos[1] = self.pos[1] + self.velocity[1] * self.delta_t
        
        self.rect[0] = self.pos[0] + 6     #Adjust rect to be in middle
        self.rect[1] = self.pos[1] + 5     #Adjust rect to be in middle
        
        self.updateAngle()
        #print(math.atan(self.velocity[1]/self.velocity[0]) * 180 / math.pi)
        #print(self.velocity)
        
        
    def render(self,screen:pygame.Surface,offset):
        screen.blit(pygame.transform.flip(pygame.transform.rotate(self.image,self.angle),self.flip,self.flip),
                    (self.pos[0] - offset[0],self.pos[1] - offset[1]))
        
        #pygame.draw.rect(screen,(255,0,0),(self.rect[0] - offset[0], self.rect[1] - offset[1], self.rect[2], self.rect[3]))


class ProjectileController():
    
    def __init__(self,tileMap,explosions):
        
        self.tileMap = tileMap
        self.explosions:list[Explosion] = explosions
        self.missiles:list[Projectile] = []
        
    def addMissile(self,projectile:Projectile):
        self.missiles.append(projectile)
        
    def update(self):
        for missile in self.missiles:
                      
            if(missile.pos[1] > 2000):
                print('projectile removed')
                self.missiles.remove(missile)
                continue
            
            if(missile.detectCollision(self.tileMap)):
                print("explosion")                
                ex1 = Explosion("explosion",missile.getExplosionPoint())
                ex2 = Explosion("explosion",[missile.getExplosionPoint()[0] - 2,missile.getExplosionPoint()[1] - 3])
                self.explosions.append(ex1)
                self.explosions.append(ex2)
                self.missiles.remove(missile)
                continue
            
            missile.update()
            
    def render(self,screen,renderOffset):  
        for missile in self.missiles:  
            missile.render(screen,renderOffset)  
                        

class Explosion:
    
    def __init__(self,folderPath,pos):
        
        self.images = load_images(folderPath,(20,20))
        self.animation = Animation(self.images,6)
        self.pos = pos
        
    def render(self,screen,offset):
        screen.blit(self.animation.getImage(),(self.pos[0] - offset[0],self.pos[1] - offset[1]))
        
        