import json
import pygame
# What is better is this case: composition or inheritance?
# The rule is simple: inheritance = “is a”, composition = “has a”.
# So Tilemp has Tiles, not is a Tile

AUTOTILE_MAP = { # It's not possible to use a list as key, so it's necessary to use a tuple
    tuple(sorted([(1, 0), (0, 1)])): 0, # The top left should be placed if there's a tile to your right and a tile below 
    tuple(sorted([(1, 0), (-1, 0), (0, 1)])): 1, # The top middle should be placed if there's a tile to your right, a tile below and a tile on the left
    tuple(sorted([(-1, 0), (0, 1)])): 2, # The top right should be placed if there's a tile to your left and a tile below
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 3, # The mid left should be placed if there's a tile to your right, a tile below and a tile above
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 4, # The mid middle should be placed if there's tiles in any direction
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 5, # The mid right should be placed if there's a tile to your left, a tile below and a tile above
    tuple(sorted([(1, 0), (0, -1)])): 6, # The bottom left should be placed if there's a tile to your right and a tile above
    tuple(sorted([(1, 0), (-1, 0), (0, -1)])): 7, # The bottom middle should be placed if there's a tile to your right, a tile to the left and a tile above
    tuple(sorted([(-1, 0), (0, -1)])): 8, # The bottom right should be placed if there's a tile to your left and a tile above
}

TILEMAP_PATH = 'assets/maps'
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)] # All collision possibilities that the player entity has
PHYSICS_TILES = {'grass_1a', 'grass_1b', 'grass_plataform', 'dirty_1a', 'dirty_1b', 'dirty_plataform', 'rock_1a', 'rock_1b', 'stone', 'wood'} # This is considered a set() in Python, this is faster than a list()
AUTOTILE_TYPES = {'grass_1a', 'grass_1b', 'dirty_1a', 'dirty_1b', 'rock_1a', 'rock_1b'}

class Tile:
    def __init__(self, type:str, variant:int, pos:tuple):
        self.type = type
        self.variant = variant
        self.pos = pos

    def __repr__(self):
        return f"Tile(type='{self.type}', variant='{self.variant}', pos={self.pos})" # Without this, if I wanted to debug using print, I would only have access to the memory address where the object is located. This way, I can see what this object represents.

    def to_dict(self):
        return {'type': self.type, 'variant': self.variant, 'pos': list(self.pos)}

    @staticmethod
    def from_dict(data:dict):
        return Tile(data['type'], data['variant'], tuple(data['pos']))
    
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

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = (tile.pos[0] + shift[0], tile.pos[1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc].type == tile.type: # Check if the neighboring tile the same type as the tile itself (I don't want to autocomplete 'grass' with 'dirty')
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile.type in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile.variant = AUTOTILE_MAP[neighbors]

                
    def add(self, pos, type, variant):
        self.tilemap[pos] = Tile(type, variant, pos)
        
    def get(self, pos):
        return self.tilemap.get(pos)
    
    def remove(self, pos):
        return self.tilemap.pop(pos, None)
    
    def save(self, path):
        data = {
            'tile_size': self.tile_size,
            'tilemap': {f'{x};{y}': tile.to_dict() for (x, y), tile in self.tilemap.items()},
            'offgrid_tiles': [tile.to_dict() for tile in self.offgrid_tiles]
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
        self.offgrid_tiles = [Tile.from_dict(tile_data) for tile_data in data.get('offgrid_tiles', [])]

        self.update_boundaries()
        
    def update_boundaries(self):
        self.min_x = min(self.tilemap.keys(), key=lambda x: x[0])[0] # Returns a tuple like this (1, 4) but I only want min or max between 
        self.max_x = max(self.tilemap.keys(), key=lambda x: x[0])[0]
        self.min_y = min(self.tilemap.keys(), key=lambda x: x[1])[1]
        self.max_y = max(self.tilemap.keys(), key=lambda x: x[1])[1]
        
        self.map_bounds = {
            'left': self.min_x * self.tile_size,
            'right': (self.max_x + 1) * self.tile_size, # Add +1 to max values so the boundary is at the FAR edge of the tile
            'top': self.min_y * self.tile_size,
            'bottom': (self.max_y + 1) * self.tile_size
        }
    
    def render(self, surf, offset=(0, 0)):
        '''
        It's much fast and efficient to determine which tile should be on screen and then only show those tiles. If we know where the camera is we can calculate all the possible positions that could be on screen for the tilemap.
        The ideia is to figure out where the top left tile of the screen should be and then calculate all the tuples going down to the bottom right and everything in between and then we look up those locations and if there is a tile then we render it.
        '''
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets.tile[tile.type][tile.variant], (tile.pos[0] - offset[0], tile.pos[1] - offset[1])) # The concept of a real camera doesn't exist in gaming, once the player moves right everything needs to move to the left.
        
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1): # Start on the top left edge of the screen and goes to the right edge of the screen (there is an off by one)
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1): # It's the same for y axis but now vertically, with this the assets will be rendered based on where the camera is
                loc = (x, y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets.tile[tile.type][tile.variant], (tile.pos[0] * self.tile_size - offset[0], tile.pos[1] * self.tile_size - offset[1]))
                    # Search the assets dictionary key through tile.type, e.g., ‘grass_1a’, then searches for the value from some index, e.g., 0, which would result in the first image in that folder, i.e., ‘0.png’, 
                    # thus rendering the tile on the displayer, and after upscaling on the screen. In addition, the position in coordinates is converted to the pixel position on the screen, so the positions are multiplied by tile_size (=16).
