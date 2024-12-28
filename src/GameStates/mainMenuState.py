import sys
import pygame
import pygame_gui
from GameStates.gameState import GameState
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from utils import SpriteSheet, load_images

class MainMenuState(GameState):
    
    def __init__(self, game_statesManager, screen) -> None:
        super().__init__(game_statesManager,screen)
        
        # Load a sound file
        self.sound_file = "Assets/Sounds/buttonSelection.mp3" 
        self.sound_effect = pygame.mixer.Sound(self.sound_file) 
        
        #fonts
        self.font = pygame.font.Font('Assets/fonts/Evil_Empire.otf',9)
        
        self.curr_screen = 1
        self.scale = (3,3)
        
        # Create a UIManager
        self.ui_manager = pygame_gui.UIManager((SCREEN_WIDTH,SCREEN_HEIGHT),
                                               "C:/Users/MARWAN/Desktop/Programing/Python/srengaGame/Assets/uiThemes/theme.json")
        
        self.characters = {
            'Knight': SpriteSheet('knight/knightIdle.png','jsonImages/knight.json','#71664f',self.scale).get_first_image('knightIdle'),
            'player': load_images('Player/idle',(self.scale[0]*16,self.scale[1]*20))[0]
        }
        
        self.curr_character = 0
        self.characters_list = list(self.characters)      
         
        self.init_screen1()
        
    
    def init_screen1(self):
        
        self.curr_screen = 1
        self.ui_manager.clear_and_reset()
                                    
        # Create a button with the custom theme
        button_rect = pygame.Rect(((SCREEN_WIDTH-100)/2, (SCREEN_HEIGHT-120)/2), (100, 50))
        self.button = pygame_gui.elements.UIButton(relative_rect=button_rect,text='New Game',
                                                   manager=self.ui_manager,visible=1)

        button1_rect = pygame.Rect(((SCREEN_WIDTH-100)/2, (SCREEN_HEIGHT-120)/2 + 70), (100, 50))
        self.button1 = pygame_gui.elements.UIButton(relative_rect=button1_rect,text='Exit',
                                                    manager=self.ui_manager)
        
        
    def init_screen2(self):
        
        self.curr_screen = 2
        self.ui_manager.clear_and_reset()
                    
        # Create a button with the custom theme
        button_rect2 = pygame.Rect(((SCREEN_WIDTH-140), (SCREEN_HEIGHT-100)), (120, 50))
        self.button2 = pygame_gui.elements.UIButton(relative_rect=button_rect2,text='Start Game',
                                                   manager=self.ui_manager,visible=1)
        

        button1_rect2 = pygame.Rect(((20), (SCREEN_HEIGHT-100)), (160, 50))
        self.button3 = pygame_gui.elements.UIButton(relative_rect=button1_rect2,text='Back to MainMenu',
                                                    manager=self.ui_manager)
    
    
    def screen1(self,timeDelta):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()    
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.button:
                    self.sound_effect.play()
                    self.init_screen2()
                    print("moving from screen 1 to screen 2")
                if event.ui_element == self.button1:
                    #self.button.hide()
                    self.sound_effect.play()
                    pygame.quit()
                    sys.exit()
                          
            # Pass events to the UIManager
            self.ui_manager.process_events(event)
            
                
        # Update the UIManager
        self.ui_manager.update(timeDelta)
        
        # Draw everything
        self.screen.fill((0, 200, 200))
        self.ui_manager.draw_ui(self.screen)
     
         
    def screen2(self,timeDelta):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_RIGHT):
                    self.curr_character = (self.curr_character+1)%len(self.characters_list)
                        
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.button2:
                    self.sound_effect.play()
                    self.game_statesManager.getRunningState().intiallize(self.characters_list[self.curr_character])
                    self.game_statesManager.setGameState(self.game_statesManager.getRunningState())
                    break                   
                if event.ui_element == self.button3:
                    self.sound_effect.play()
                    self.init_screen1()
                    print("moving from screen 2 to screen 1")
                    
                          
            # Pass events to the UIManager
            self.ui_manager.process_events(event)
             
        # Update the UIManager
        self.ui_manager.update(timeDelta)
        
        # Draw everything
        self.screen.fill((0, 200, 200))
        self.ui_manager.draw_ui(self.screen)
        
        img_pos = ((SCREEN_WIDTH)/2,(SCREEN_HEIGHT)/2)
        character_type = self.characters_list[self.curr_character]
        self.screen.blit(self.characters[character_type],img_pos)
        
        char_text_surface = self.font.render("Select a Character", False,  (0, 0, 0))
        self.screen.blit(pygame.transform.scale(char_text_surface,(300,20)), char_text_surface.get_rect(topleft = ((SCREEN_WIDTH)/2 - 100,100))) 
          
           
    def doAction(self,timeDelta):
        
        if self.curr_screen == 1:
            self.screen1(timeDelta)
        else:
            self.screen2(timeDelta)
        
    
        
        
    