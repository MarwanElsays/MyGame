import pygame
from GameStates.gameStatesManager import GameStatesManager
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Game:
    
    def __init__(self):
        pygame.init()
    
        self.screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
        pygame.display.set_caption("Seringa Game")
        self.clock = pygame.time.Clock()
        
        self.gameStatesManager = GameStatesManager(self.screen)            
            
    def run(self): 
        
        while True:
            time_delta = self.clock.tick(60) / 1000.0
            self.gameStatesManager.doAction(time_delta)
            pygame.display.update() 
            
            
if __name__ == "__main__":
    game = Game()
    game.run()
