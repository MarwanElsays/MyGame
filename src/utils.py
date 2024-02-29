import os
import pygame
import json
from settings import SCALE, TILE_SIZE

BASE_IMG_PATH = 'Assets/images/'

def load_image(path,scale = (0,0)):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    if(scale[0] or scale[1]): img = pygame.transform.scale(img,scale)
    return img

def load_image_alpha(path,scale = (0,0)):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    if(scale[0] or scale[1]): img = pygame.transform.scale(img,scale)
    return img

def load_images(path,scale = (0,0),alpha = 0):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        if alpha:
            images.append(load_image_alpha(path + '/' + img_name,scale))
        else:
            images.append(load_image(path + '/' + img_name,scale))
    return images

class Spritesheet:
    
    def __init__(self, image_path,jsonimage_path,color_key='#000000',scale = (1,1)):
        self.image_path = BASE_IMG_PATH + image_path
        self.jsonimage_path = BASE_IMG_PATH + jsonimage_path
        self.color_key = color_key
        self.scale = scale
        self.sprite_sheet = pygame.image.load(self.image_path).convert()
        with open(self.jsonimage_path) as f:
            self.data = json.load(f)
        f.close()
        
    def __get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey(self.color_key)
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
        sprite = pygame.transform.scale(sprite,(w*self.scale[0],h*self.scale[1]))
        return sprite

    def get_sprite_images(self, animation_name):  
        
        images = []
        sprite_frames = self.data[animation_name]
        for frame in sprite_frames.values():
            x, y, w, h, off ,flip_off= frame["x"], frame["y"], frame["w"], frame["h"], frame["off"],frame["flipOff"]
            images.append((self.__get_sprite(x, y, w, h),off,flip_off))
            
        return images
    
    def get_first_image(self, animation_name):

        sprite_frames = self.data[animation_name]
        frame = sprite_frames["frame_1"]
        x, y, w, h = frame["x"], frame["y"], frame["w"], frame["h"]
                
        return self.__get_sprite(x, y, w, h)




