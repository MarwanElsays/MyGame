import sys
import pygame
import json
from utils import load_images
from settings import TILE_SIZE

class Game:
    
    def __init__(self):
        pygame.init()
        self.width = 600
        self.height = 600
        self.backGC = '#C4FAF8'
        self.screen = pygame.display.set_mode((self.width , self.height))
        
        pygame.display.set_caption("Maro Game")
        self.clock = pygame.time.Clock()
        
        self.offset = [0,0]
        
        self.background = False
        self.Tiles = {
            "rockyGround" : load_images('tiles/rockyGround'),
            "Grass" : load_images('tiles/Grass'),
            "Grass2" : load_images('tiles/Grass2'),
            "Alien" : load_images('tiles/Alien',(TILE_SIZE,TILE_SIZE)),
            "Chests": load_images('/chests',(TILE_SIZE,TILE_SIZE)),
            "Lava": load_images('tiles/Lava',(TILE_SIZE,TILE_SIZE)),
        }
         
        self.TilesAsList = list(self.Tiles)
        print(self.TilesAsList)
        print(len(self.Tiles))
        self.tileType = 0 
        self.variant = 0       
        self.speed = [0,0]
        self.pos = [self.width/2,self.height/2]
        self.TilesDrawn , self.backgroundTiles = self.LoadMap('Assets/maps/map0.json')
        print(self.backgroundTiles)
            
    def getpos(self,pos):
        newPos = (int(pos[0]/TILE_SIZE),int(pos[1]/TILE_SIZE))
        return newPos
    
    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.TilesDrawn,'backgroundTiles':self.backgroundTiles}, f)
        f.close()
        
    def LoadMap(self,path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        return map_data['tilemap'], map_data['backgroundTiles'] if 'backgroundTiles' in map_data else {}
    
    def render(self,offset):
        # for tilesInfo in self.TilesDrawn.values():
        #     type,var,pos = tilesInfo.values()
        #     self.screen.blit(self.Tiles[type][var],(pos[0]*TILE_SIZE - self.offset[0],pos[1]*TILE_SIZE - self.offset[1]))
            
        for x in range(offset[0] // TILE_SIZE, (offset[0] + self.width) // TILE_SIZE + 1):
            for y in range(offset[1] // TILE_SIZE, (offset[1] + self.height) // TILE_SIZE + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.TilesDrawn:
                    type,var,pos = self.TilesDrawn[loc].values()
                    self.screen.blit(self.Tiles[type][var], (pos[0] * TILE_SIZE - offset[0],pos[1] * TILE_SIZE - offset[1]))
                if loc in self.backgroundTiles:
                    type,var,pos = self.backgroundTiles[loc].values()
                    self.screen.blit(self.Tiles[type][var], (pos[0] * TILE_SIZE - offset[0],pos[1] * TILE_SIZE - offset[1]))        
      
    def getInput(self,renderOffset):
        mousePos = pygame.mouse.get_pos()
        Mouse = pygame.mouse.get_pressed()
        newpos = self.getpos((mousePos[0] + renderOffset[0],mousePos[1] + renderOffset[1]))
        tilekey = str(newpos[0]) + ';' + str(newpos[1])
        
        if(Mouse[0]):
            if(not self.background):
                self.TilesDrawn[tilekey] = {'type':self.TilesAsList[self.tileType],'variant':self.variant,'pos':newpos}
            else:
                self.backgroundTiles[tilekey] = {'type':self.TilesAsList[self.tileType],'variant':self.variant,'pos':newpos}
            
            print(tilekey)   
            print((mousePos[0] + renderOffset[0],mousePos[1] + renderOffset[1]))
            
        elif(Mouse[2]):
            if(not self.background):
                if(tilekey in self.TilesDrawn):
                    self.TilesDrawn.pop(tilekey)
            else:
                if(tilekey in self.backgroundTiles):
                    self.backgroundTiles.pop(tilekey)
            
        
    def run(self): 
        
        while True:

            self.screen.fill(self.backGC) 

            mousePos = pygame.mouse.get_pos()
            self.pos[0]+=self.speed[0]
            self.pos[1]+=self.speed[1]
            self.offset[0] += (self.pos[0] - self.width/2 - self.offset[0])/10
            self.offset[1] += (self.pos[1]- self.height/2 - self.offset[1])/10
            
            renderOffset = (int(self.offset[0]),int(self.offset[1]))
            
            self.screen.blit(self.Tiles[self.TilesAsList[self.tileType]][self.variant],mousePos)
            
            self.render(renderOffset)
            self.getInput(renderOffset)
            
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
                if events.type == pygame.MOUSEBUTTONDOWN:
                    pass 
                         
                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_RIGHT:
                        self.speed[0] = 10
                    if events.key == pygame.K_LEFT:
                        self.speed[0] = -10
                    if events.key == pygame.K_UP:
                        self.speed[1] = -10
                    if events.key == pygame.K_DOWN:
                        self.speed[1] = 10
                    if events.key == pygame.K_b:
                        self.background = not self.background
                    if events.key == pygame.K_v:
                        self.variant+=1
                        self.variant%=len(self.Tiles[self.TilesAsList[self.tileType]])
                    if events.key == pygame.K_t:
                        self.tileType+=1
                        self.variant = 0
                        self.tileType%=len(self.TilesAsList)
                    if events.key == pygame.K_s:
                        print("DATA SAVED")
                        self.save('Assets/maps/map0.json')
                        
                if events.type == pygame.KEYUP:
                    if events.key == pygame.K_RIGHT or events.key == pygame.K_LEFT:
                        self.speed[0] = 0
                    if events.key == pygame.K_UP or events.key == pygame.K_DOWN:
                        self.speed[1] = 0
                        
            pygame.display.update()
            self.clock.tick(60)
            
Game().run()