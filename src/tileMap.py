import pygame
import json

from settings import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE
from utils import load_images

aroundDir = [(-1,-1),(-1,0),(-1,1),(1,-1),(1,0),(1,1),(0,-1),(0,1)]

class tile:
    def __init__(self,pos,image):
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)    

class tileMap:
    def __init__(self,path):
        self.map = {}
        self.Tiles = []
        
        self.TilesImages = {
            "rockyGround" : load_images('tiles/rockyGround',scale=(TILE_SIZE,TILE_SIZE)),
            "Grass" : load_images('tiles/Grass',scale=(TILE_SIZE,TILE_SIZE)),
            "Chests" : load_images('chests',scale=(TILE_SIZE,TILE_SIZE)),
            "Alien" : load_images('tiles/Alien',(TILE_SIZE,TILE_SIZE)),
            "Lava": load_images('tiles/Lava',(TILE_SIZE,TILE_SIZE)),
        }
        
        self.LoadMap(path)
        
        print(len(self.map))
    
    def LoadMap(self,path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
    
        self.map = map_data['tilemap']
        for tilesInfo in self.map.values():
            type,var,pos = tilesInfo.values()
            newPos = (pos[0]*TILE_SIZE , pos[1]*TILE_SIZE)
            self.Tiles.append(tile(newPos,self.TilesImages[type][var]))
            
    def getAroundTiles(self,pos) -> list:
        rects = []
        cord = (int(pos[0]/TILE_SIZE),int(pos[1]/TILE_SIZE))       
        for DirAr in aroundDir:
            locAr = str(cord[0]+ DirAr[0]) + ';' + str(cord[1] + DirAr[1])
            if locAr in self.map:
                p = self.map[locAr]['pos']
                rects.append(pygame.rect.Rect(p[0]*TILE_SIZE,p[1]*TILE_SIZE,TILE_SIZE,TILE_SIZE))  
                 
        return rects     
                                                  
    def update(self):
        pass
    
    def render(self,screen,offset):
            
        for x in range(offset[0] // TILE_SIZE, (offset[0] + SCREEN_WIDTH) // TILE_SIZE + 1):
            for y in range(offset[1] // TILE_SIZE, (offset[1] + SCREEN_HEIGHT) // TILE_SIZE + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.map:
                    type,var,pos = self.map[loc].values()
                    screen.blit(self.TilesImages[type][var], (pos[0] * TILE_SIZE - offset[0],pos[1] * TILE_SIZE - offset[1]))