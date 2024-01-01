import pygame


class Animation:
    def __init__(self,images,frameDuration,status=''):
        self.images = images
        self.status = status
        self.frameDuration = frameDuration
        self.imageIdx = 0
    
    def update(self):
        self.imageIdx += 1
        self.imageIdx %= (len(self.images) * self.frameDuration)
        
        
    def getImage(self)->pygame.Surface:
        img = self.images[int(self.imageIdx / self.frameDuration)]
        return img
    