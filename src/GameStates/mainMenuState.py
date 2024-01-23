import sys
import pygame
import pygame_gui
from GameStates.gameState import GameState
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class MainMenuState(GameState):
    
    def __init__(self, gameStatesManager, screen) -> None:
        super().__init__(gameStatesManager,screen)
        
        # Create a UIManager
        self.ui_manager = pygame_gui.UIManager((SCREEN_WIDTH,SCREEN_HEIGHT),
                                               "C:/Users/MARWAN/Desktop/Programing/Python/srengaGame/Assets/uiThemes/theme.json")

        # Create a button with the custom theme
        button_rect = pygame.Rect((350, 275), (100, 50))
        self.button = pygame_gui.elements.UIButton(relative_rect=button_rect,text='New Game',
                                                   manager=self.ui_manager,visible=1)
        

        button1_rect = pygame.Rect((150, 275), (100, 50))
        self.button1 = pygame_gui.elements.UIButton(relative_rect=button1_rect,text='clear window!',
                                                    manager=self.ui_manager)

        UIDropDownMenu1_rect = pygame.Rect((450, 275), (100, 50))
        self.uIDropDownMenu = pygame_gui.elements.UIDropDownMenu(['maro','youma'],'maro',UIDropDownMenu1_rect,manager=self.ui_manager)
           
           
    def doAction(self,timeDelta):
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()    
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.button:
                    self.gameStatesManager.getRunningState().intiallize()
                    self.gameStatesManager.setGameState(self.gameStatesManager.getRunningState())
                    break                   
                if event.ui_element == self.button1:
                    self.button.hide()
                    #self.ui_manager.clear_and_reset()
                    print("Window Cleared")
                          
            # Pass events to the UIManager
            self.ui_manager.process_events(event)
            
                
        # Update the UIManager
        self.ui_manager.update(timeDelta)
        
        # Draw everything
        self.screen.fill((255, 255, 255))
        self.ui_manager.draw_ui(self.screen)
        
    
        
        
    