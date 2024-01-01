import os
import pygame

from settings import TILE_SIZE

BASE_IMG_PATH = 'Assets/images/'

def load_image(path,scale = (0,0)):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    if(scale[0] or scale[1]): img = pygame.transform.scale(img,scale)
    return img

def load_images(path,scale = (0,0)):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name,scale))
    return images


# def HelpRect():
#     sur = pygame.surface.Surface(self.rect.size)
#     sur.fill("green")
#     screen.blit(sur,(self.rect.x - offset[0],self.rect.y - offset[1]))

