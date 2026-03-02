import sys

import pygame

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player
from scripts.tilemap import Tilemap
from scripts.assets import Assets

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Metroid Rogue')

        game_icon = pygame.image.load('assets/game_icon.png')

        pygame.display.set_icon(game_icon)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH*3, SCREEN_HEIGHT*3)) # Window resolution -- here I will draw everything

        self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)) # screen = window surface / display = window that render things
        # The reason for using a separate internal surface is to render the game at a lower native resolution (320 x 240), which ensures consistent pixel art scaling 
        # and reduces processing overhead. The main screen surface then acts as a container, upscaling the final image to fill the window (960 x 720) without losing the 'chunky' retro aesthetic.
        
        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]
        
        self.assets = Assets()
        
        self.scaled_background = pygame.transform.scale(self.assets.ground['background'], (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.player = Player(self, (155, -165), (10, 12)) # (10, 16) are the dimensions of the player, that is the collision space that PhysicsEntity is considering
        
        self.tilemap = Tilemap(self, tile_size=16)
        
        self.scroll = [0.0, 0.0]
        
        self.tilemap.load('map.json')
        
    def run(self):
        while True:
            self.display.blit(self.scaled_background, (0, 0))
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30 # Creates a smoother movement of the camera
            # If the camera is placed directly onto the player's location, the player would end up in the top left of the screen. The player needs to be in the center of the screen,
            # so it's necessary to subtract part of the screen size so that the camera os positioned in a way where the center of what you can see is on the player.
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            
            render_scroll = (int(self.scroll[0]), int(self.scroll[1])) # Without this, when the player jumps, they will flicker because the camera will result in a float.
            
            self.tilemap.render(self.display, offset=render_scroll) # The movement of the camera could seems a little bit choppy, to solve this it'll be necessary work with subpixels (I do'nt know)
            
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)
            
            for event in pygame.event.get(): # Gets the input and interacts with Windows
                if event.type == pygame.QUIT: # Each 'event' has a type attribute that can specifies what type of event it is
                    pygame.quit() # Close pygame window
                    sys.exit() # Exit the application as a whole
                if event.type == pygame.KEYDOWN: # This conditions checks if ANY key in keyboard Windows is pressed down 
                    if event.key == pygame.K_LEFT: # Checks if '←' is pressed
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT: # Checks if '→' is pressed
                        self.movement[1] = True
                    if event.key == pygame.K_UP: # Checks if '↑' is pressed 
                        self.player.jump_up()
                    if event.key == pygame.K_DOWN: # Checks if '↓' is pressed
                        pass
                if event.type == pygame.KEYUP: # This conditions checks if ANY key in keyboard Windows is unpressed 
                    if event.key == pygame.K_LEFT: # Checks if '←' is unpressed
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT: # Checks if '→' is unpressed
                        self.movement[1] = False
                    if event.key == pygame.K_UP: # Checks if '↑' is unpressed
                        pass
                    if event.key == pygame.K_DOWN: # Checks if '↓' is unpressed
                        pass
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size())) # Scale the size of the display to the size of the screen 
            pygame.display.update() # If I don't call this function, I won't see anything changing on the screen

            self.clock.tick(60) # Force the loop to run at 60 FPS



if __name__ == '__main__':
    Game().run()
    
    
    

