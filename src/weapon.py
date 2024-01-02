import math

from pygame import Surface
import pygame
from projectile import Projectile, ProjectileController
from utils import load_image


class Weapon:
    
    def __init__(self,imageFilePath,scale,player,equippedAngle,projectileController,soundChannel,intialPos = [300,100]):
        
        self.projectileController:ProjectileController = projectileController
        
        self._pos:[float,float] = intialPos
        self._vY = 0   
        self._scale = scale
        
        from player import Player
        self._player:Player = player
        
        self._image = load_image(f'wepons/{imageFilePath}',scale)
        self._rect = self._image.get_rect(center = (self._pos[0]+scale[0]/2,self._pos[1]+scale[1]/2))
        self._rect.width = 30
        self._rect.height = 30
        
        # Load a sound file
        self.soundfile = "Assets/Sounds/RpgBrust.mp3" 
        self.soundeffect = pygame.mixer.Sound(self.soundfile) 
        self.soundChannel = soundChannel 
        
        self._equiped = False  
        self._floatAngle = 0        #When it is not equipped just hovering
        self._angle = 0             #When Equipped by player  
        self._equipedAngle = equippedAngle  
        self._flip = False          #Flip with the Player
        
    
    def isCollidingWithPlayer(self):
        return self._player.rect.colliderect(self._rect)
                    
    def checkEquipped(self):
      
        if(self._player.getWepon() == self and not self._player.equipping):
            self._player.setWepon(None)
            self._equiped = False
            self._angle = 0
            self._pos = [self._player.rect.center[0],self._player.rect.center[1]-30]
            
            print("unEquipped")
            
        if(self._player.getWepon() == None and self.isCollidingWithPlayer() and self._player.equipping):
            self._player.setWepon(self)
            self._equiped = True
            self._angle = self._equipedAngle
                        
            print("Equipped")
                    
        
    def update(self):
        
        self.checkEquipped()

        
        if self._equiped:
            self._floatAngle = 0
            if self._player.flip:
                self._flip = True
                self._pos = [self._player.rect.center[0]-10,self._player.rect.center[1]-10]
            else:
                self._flip = False
                self._pos = [self._player.rect.center[0]-10,self._player.rect.center[1]-10]
        else:
            self._floatAngle+=1
            self._floatAngle%=360
            self._pos[1] += 0.3 * math.sin(self._floatAngle*math.pi/180)
            self._rect.center = (self._pos[0]+self._scale[0]/2,self._pos[1]+self._scale[1]/2)
            
            
    def launch(self):
        missileAngle = 180 - self._equipedAngle  if self._flip else self._equipedAngle
        missile = Projectile(1,"missile.png",(20,14),missileAngle,self._flip,self._pos)
        missile.setForceY(0)
        #self.soundChannel.play(self.soundeffect)
        self.soundeffect.play()
        self.projectileController.addMissile(missile)
    
    def render(self,screen:Surface,offset):
        
        #pygame.draw.rect(screen,(255,0,0),(self._rect[0] - offset[0], self._rect[1] - offset[1], self._rect[2], self._rect[3]))
        
        screen.blit(pygame.transform.flip(pygame.transform.rotate(self._image,self._angle),self._flip,False),
                    (self._pos[0] - offset[0],self._pos[1] - offset[1]))
    