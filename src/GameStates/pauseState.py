import sys
import pygame
from GameStates.gameState import GameState

class PauseState(GameState):
    
    def __init__(self, gameStatesManager , screen) -> None:
        super().__init__(gameStatesManager,screen)
        
    def doAction(self,timeDelta):
        self.screen.fill("#FF0000")
        
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                sys.exit()    
            if events.type == pygame.MOUSEBUTTONDOWN:
                self.gameStatesManager.setGameState(self.gameStatesManager.getRunningState())
                
        print("Pausing")