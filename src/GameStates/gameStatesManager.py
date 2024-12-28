from GameStates.mainMenuState import MainMenuState
from GameStates.gameState import GameState
from GameStates.pauseState import PauseState
from GameStates.runningState import RunningState

class GameStatesManager:
    
    def __init__(self,screen) :
        self.__main_menu_state = MainMenuState(self,screen)
        self.__running_state = RunningState(self,screen)
        self.__PauseState = PauseState(self,screen)
        #self.__PauseState.intiallize()
        #self.__game_state:GameState = self.__PauseState
        self.__game_state:GameState = self.__main_menu_state
        
    def setGameState(self,game_state):
        self.__game_state = game_state
    
    def getGameState(self):
        return self.__game_state
    
    def getMainMenuState(self):
        return self.__main_menu_state
    
    def getRunningState(self):
        return self.__running_state
    
    def getPauseState(self):
        return self.__PauseState 
   
    def doAction(self,timeDelta):
        self.__game_state.doAction(timeDelta)