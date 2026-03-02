import sys

import pygame

from scripts.utils import load_images
from scripts.tilemap import Tile, Tilemap
from scripts.assets import Assets

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
RENDER_SCALE = 3.0

class Editor:
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
        
        try:        
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass
        
        self.scroll = [0.0, 0.0]
        
        self.tile_list = list(self.assets.tile)
        self.tile_group = 0
        self.tile_variant = 0
        
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True
        
    def run(self):
        while True:
            self.display.fill((0, 0, 0))
            
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            
            render_scroll = (int(self.scroll[0]), int(self.scroll[1])) # Truncated version of scroll to respect the grid
            
            self.tilemap.render(self.display, offset=render_scroll)
            
            current_tile_img = self.assets.tile[self.tile_list[self.tile_group]][self.tile_variant].copy() # Each image of each folder of my assets.tile atribute
            current_tile_img.set_alpha(100) # Image partially transparent to see what is behind before place it
            
            mouse_pos = pygame.mouse.get_pos() # Mouse position coordinates
            mouse_pos = (mouse_pos[0] / RENDER_SCALE, mouse_pos[1] / RENDER_SCALE)
            tile_pos = (int((mouse_pos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mouse_pos[1] + self.scroll[1]) // self.tilemap.tile_size))
            # That will give the coordinates of the mouse in terms of the tile system (Grid Based)
            
            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
                # Allows to preview the tile that will be placed according to the grid.
            else:
                self.display.blit(current_tile_img, mouse_pos) # Allows to preview the tile that will be placed off of the grid
            
            if self.clicking and self.ongrid: # Add tiles to the screen
                self.tilemap.add(pos=tile_pos, type=self.tile_list[self.tile_group], variant=self.tile_variant)
            if self.right_clicking: # Remove tiles to the screen
                tile_loc = (tile_pos[0], tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    self.tilemap.remove(tile_loc)
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets.tile[tile.type][tile.variant]
                    tile_rect = pygame.Rect(tile.pos[0] - self.scroll[0], tile.pos[1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_rect.collidepoint(mouse_pos):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile_img, (5, 5))
            
            for event in pygame.event.get(): # Gets the input and interacts with Windows
                if event.type == pygame.QUIT: # Each 'event' has a type attribute that can specifies what type of event it is
                    pygame.quit() # Close pygame window
                    sys.exit() # Exit the application as a whole
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # The left button of mouse
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append(Tile(type=self.tile_list[self.tile_group], variant=self.tile_variant, pos=(mouse_pos[0] + self.scroll[0], mouse_pos[1] + self.scroll[1])))
                            # Why add scroll to 'pos' attribute? From the camera's perspective the top left is (0, 0) but in the world's perspective could be other value, because the world is larger than the camera position
                    if event.button == 3: # The right button of mouse
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4: # Up scrolling with mouse
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets.tile[self.tile_list[self.tile_group]]) # When you reach the end of that list it'll just loop around to zero
                        if event.button == 5: # Down scrolling with mouse
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets.tile[self.tile_list[self.tile_group]]) # With this is possible to scroll between variants    
                    else:
                        if event.button == 4: # Up scrolling with mouse
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list) # When you reach the end of that list it'll just loop around to zero
                            self.tile_variant = 0
                        if event.button == 5: # Down scrolling with mouse
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list) # With this is possible to scroll between groups but it's also necessary scroll between variants    
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                
                if event.type == pygame.KEYDOWN: # This conditions checks if ANY key in keyboard Windows is pressed down 
                    if event.key == pygame.K_a: # Checks if 'a' is pressed
                        self.movement[0] = True
                    if event.key == pygame.K_d: # Checks if 'd' is pressed
                        self.movement[1] = True
                    if event.key == pygame.K_w: # Checks if 'w' is pressed 
                        self.movement[2] = True
                    if event.key == pygame.K_s: # Checks if 's' is pressed
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid # Why do not use just False? Because not self.ongrid just flip the boolean value, if just put False how can I go back to true with the same key?
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_o:
                        self.tilemap.save('map.json')
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                if event.type == pygame.KEYUP: # This conditions checks if ANY key in keyboard Windows is unpressed 
                    if event.key == pygame.K_a: # Checks if 'a' is unpressed
                        self.movement[0] = False
                    if event.key == pygame.K_d: # Checks if 'd' is unpressed
                        self.movement[1] = False
                    if event.key == pygame.K_w: # Checks if 'w' is unpressed
                        self.movement[2] = False
                    if event.key == pygame.K_s: # Checks if 's' is unpressed
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size())) # Scale the size of the display to the size of the screen 
            pygame.display.update() # If I don't call this function, I won't see anything changing on the screen

            self.clock.tick(60) # Force the loop to run at 60 FPS



if __name__ == '__main__':
    Editor().run()
    
    
    

