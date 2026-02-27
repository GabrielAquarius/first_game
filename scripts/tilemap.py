import json
import pygame
# What is better is this case: composition ou inheritance?
# The rule is simple: inheritance = “is a”, composition = “has a”.
# So Tilemp has Tiles, not is a Tile


TILEMAP_PATH = 'assets/maps'
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)] # All collision possibilities that the player entity has
PHYSICS_TILES = {'grass_1a', 'dirty_1a'} # This is considered a set() in Python, this is faster than a list()

class Tile:
    def __init__(self, type:str, variant:int, pos:tuple):
        self.type = type
        self.variant = variant
        self.pos = pos
    
    def __repr__(self):
        return f"Tile(type='{self.type}', variant='{self.variant}', pos={self.pos}" # Without this, if I wanted to debug using print, I would only have access to the memory address where the object is located. This way, I can see what this object represents.

    def to_dict(self):
        return {'type': self.type, 'variant': self.variant, 'pos': list(self.pos)}

    @staticmethod
    def from_dict(data:dict):
        return Tile(data['type'], data['variant'], tuple([data['pos']]))
    
    def rect(self, tile_size):
        return pygame.Rect(self.pos[0] * tile_size, self.pos[1] * tile_size, tile_size, tile_size) # shortcut to 


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {} # Each tile is placed following the grid (only here I handle physics)
        # Map each tile based on its location, thus avoiding processing empty spaces on the screen.
        self.offgrid_tiles = [] # Tiles are positioned freely (it's possible to add physics here, but I need to learn how to optimize)
    
    def tiles_around(self, pos):
        ''' This is being used as a collision checker. If the entity occupies a space larger than 16x16, it would be necessary to check more tiles.'''
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size)) # Using integer division to convert pixel position in grid position (-1, 0, 1)
        # Handles with integer division in Python is trick → 3//2 = 1 ; int(3/2) = 1 ; -3//2 = -2 ; int(-3 / 2) = -1
        # This means that Python handles negative numbers differently depending on how it converts floats to integers.
        # It's not a consistent behavior because there is a variance between 1 and 3 pixels, so it's better checks before rounded these collisions checker to fit in a grid 

        tiles = []
        for offset in NEIGHBOR_OFFSETS:
            check_loc = (tile_loc[0] + offset[0], tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile.type in PHYSICS_TILES:
                rects.append(tile.rect(self.tile_size))
        return rects

    def add(self, pos, type, variant):
        self.tilemap[pos] = Tile(type, variant, pos)
        
    def get(self, pos):
        return self.tilemap.get(pos)
    
    def remove(self, pos):
        return self.tilemap.pop(pos, None)
    
    def save(self, path):
        data = {
            'tile_size': self.tile_size,
            'tilemap': {f'{x};{y}': tile.to_dict() for (x, y), tile in self.tilemap.items()}
        }
        with open(f'{TILEMAP_PATH}/{path}', 'w') as file:
            json.dump(data, file, indent=2)
    
    def load(self, path):
        with open(f'{TILEMAP_PATH}/{path}', 'r') as file:
            data = json.load(file)
        self.tile_size = data['tile_size']
        self.tilemap = {}
        for key, tile_data in data['tilemap'].items():
            x, y = map(int, key.split(';'))
            self.tilemap[(x, y)] = Tile.from_dict(tile_data)
    
    def render(self, surf, offset=(0, 0)):
        '''
        It's much fast and efficient to determine which tile should be on screen and then only show those tiles. If we know where the camera is we can calculate all the possible positions that could be on screen for the tilemap.
        The ideia is to figure out where the top left tile of the screen should be and then calculate all the tuples going down to the bottom right and everything in between and then we look up those locations and if there is a tile then we render it.
        '''
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            pass
        
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile.type][tile.variant], (tile.pos[0] - offset[0], tile.pos[1] - offset[1])) # The concept of a real camera doesn't exist in gaming, once the player moves right everything needs to move to the left.
        
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile.type][tile.variant], (tile.pos[0] * self.tile_size - offset[0], tile.pos[1] * self.tile_size - offset[1]))
            # Search the assets dictionary key through tile.type, e.g., ‘grass_1a’, then searches for the value from some index, e.g., 0, which would result in the first image in that folder, i.e., ‘0.png’, 
            # thus rendering the tile on the displayer, and after upscaling on the screen. In addition, the position in coordinates is converted to the pixel position on the screen, so the positions are multiplied by tile_size (=16).
            