import pygame
import pygame_gui

pygame.init()

# Set up Pygame window
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption('pygame_gui Button Example')

# Create a UIManager
ui_manager = pygame_gui.UIManager(window_size,"C:/Users/MARWAN/Desktop/Programing/Python/srengaGame/src/theme.json")

# Create a button with the custom theme
button_rect = pygame.Rect((350, 275), (100, 50))
button = pygame_gui.elements.UIButton(relative_rect=button_rect,
                                      text='Click me!',
                                      manager=ui_manager)

button1_rect = pygame.Rect((150, 275), (100, 50))
button1 = pygame_gui.elements.UIButton(relative_rect=button1_rect,
                                      text='hey me!',
                                      manager=ui_manager)


UIDropDownMenu1_rect = pygame.Rect((450, 275), (100, 50))
uIDropDownMenu = pygame_gui.elements.UIDropDownMenu(['maro','youma'],'maro',UIDropDownMenu1_rect,manager=ui_manager)

clock = pygame.time.Clock()
is_running = True
x=1
while is_running:
    time_delta = clock.tick(60) / 1000.0

    if(x == 1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button:
                    x = 2
                    print("x = 2")
                if event.ui_element == button1:
                    print("in first state")
                        
            # Pass events to the UIManager
            ui_manager.process_events(event)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button:
                    x = 1
                    print("x = 1")
                if event.ui_element == button1:
                    print("in Second State")
                        
            # Pass events to the UIManager
            ui_manager.process_events(event)

    # Update the UIManager
    ui_manager.update(time_delta)

        

    # Draw everything
    window.fill((255, 255, 255))
    ui_manager.draw_ui(window)

    pygame.display.update()

pygame.quit()
