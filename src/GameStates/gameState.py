
from abc import ABC, abstractmethod

class GameState(ABC):

    def __init__(self,gameStatesManager,screen) -> None:
        self.gameStatesManager = gameStatesManager
        self.screen = screen
    
    @abstractmethod
    def doAction(self,timeDelta):
        pass