from GameStates.mainMenuState import MainMenuState
from GameStates.gameState import GameState
from GameStates.pauseState import PauseState
from GameStates.runningState import RunningState

class GameStatesManager:
    
    def __init__(self,screen) :
        self.__mainMenuState = MainMenuState(self,screen)
        self.__runningState = RunningState(self,screen)
        self.__PauseState = PauseState(self,screen)
        #self.__PauseState.intiallize()
        #self.__gameState:GameState = self.__PauseState
        self.__gameState:GameState = self.__mainMenuState
        
    def setGameState(self,gameState):
        self.__gameState = gameState
    
    def getGameState(self):
        return self.__gameState
    
    def getMainMenuState(self):
        return self.__mainMenuState
    
    def getRunningState(self):
        return self.__runningState
    
    def getPauseState(self):
        return self.__PauseState 
   
    def doAction(self,timeDelta):
        self.__gameState.doAction(timeDelta)