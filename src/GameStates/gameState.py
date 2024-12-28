
from abc import ABC, abstractmethod

class GameState(ABC):

    def __init__(self,game_statesManager,screen) -> None:
        self.game_statesManager = game_statesManager
        self.screen = screen
    
    @abstractmethod
    def doAction(self,timeDelta):
        pass