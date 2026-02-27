import sys

import pygame

from scripts.utils import load_images
from scripts.tilemap import Tilemap
from scripts.assets import Assets

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
RENDER_SCALE = 2.0

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Editor')

        editor_icon = pygame.image.load('assets/editor_icon.png')

        pygame.display.set_icon(editor_icon)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH*3, SCREEN_HEIGHT*3)) # Window resolution -- here I will draw everything

        self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)) # screen = window surface / display = window that render things
        # The reason for using a separate internal surface is to render the game at a lower native resolution (320 x 240), which ensures consistent pixel art scaling 
        # and reduces processing overhead. The main screen surface then acts as a container, upscaling the final image to fill the window (960 x 720) without losing the 'chunky' retro aesthetic.
        
        self.clock = pygame.time.Clock()

        self.assets = Assets()
        
        self.movement = [False, False, False, False]
        
        self.tilemap = Tilemap(self, tile_size=16)
        
        self.scroll = [0.0, 0.0]
        
        self.tile_list = list(self.assets.tile)
        
    def run(self):
        while True:
            self.display.fill((0, 0, 0))
            
            for event in pygame.event.get(): # Gets the input and interacts with Windows
                if event.type == pygame.QUIT: # Each 'event' has a type attribute that can specifies what type of event it is
                    pygame.quit() # Close pygame window
                    sys.exit() # Exit the application as a whole
                if event.type == pygame.KEYDOWN: # This conditions checks if ANY key in keyboard Windows is pressed down 
                    if event.key == pygame.K_a: # Checks if 'a' is pressed
                        self.movement[0] = True
                    if event.key == pygame.K_d: # Checks if 'd' is pressed
                        self.movement[1] = True
                    if event.key == pygame.K_w: # Checks if 'w' is pressed 
                        self.movement[2] = True
                    if event.key == pygame.K_s: # Checks if 's' is pressed
                        self.movement[3] = True
                if event.type == pygame.KEYUP: # This conditions checks if ANY key in keyboard Windows is unpressed 
                    if event.key == pygame.K_a: # Checks if 'a' is unpressed
                        self.movement[0] = False
                    if event.key == pygame.K_d: # Checks if 'd' is unpressed
                        self.movement[1] = False
                    if event.key == pygame.K_w: # Checks if 'w' is unpressed
                        self.movement[2] = False
                    if event.key == pygame.K_s: # Checks if 's' is unpressed
                        self.movement[3] = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size())) # Scale the size of the display to the size of the screen 
            pygame.display.update() # If I don't call this function, I won't see anything changing on the screen

            self.clock.tick(60) # Force the loop to run at 60 FPS



if __name__ == '__main__':
    Game().run()
    
    
    

