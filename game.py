import sys

import pygame

pygame.init()

pygame.display.set_caption('Metroid Rogue')

game_icon = pygame.image.load('assets/game_icon.png')

pygame.display.set_icon(game_icon)

screen = pygame.display.set_mode((640, 480)) # Window resolution -- here I will draw everything

clock = pygame.time.Clock()


while True:
    for event in pygame.event.get(): # Gets the input and interacts with Windows
        if event.type == pygame.QUIT: # Each 'event' has a type attribute that can specifies what type of event it is
            pygame.quit() # Close pygame window
            sys.exit() # Exit the application as a whole
    
    pygame.display.update() # If I don't call this function, I won't see anything changing on the screen
    
    clock.tick(60) # Force the loop to run at 60 FPS
    
    
    
    
    
    

