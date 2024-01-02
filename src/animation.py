import pygame


class Animation:
    def __init__(self,images,frameDuration,status=''):
        self.images = images
        self.status = status
        self.frameDuration = frameDuration
        self.imageIdx = 0
        self.done = False
        self.animationDuration = len(self.images) * self.frameDuration
    
    def update(self):
        self.imageIdx += 1
        if(self.imageIdx == self.animationDuration):self.done = True
        self.imageIdx %= self.animationDuration
        
    def getImage(self)->pygame.Surface:
        img = self.images[int(self.imageIdx / self.frameDuration)]
        return img
    