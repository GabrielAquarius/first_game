
class MapSystem:
    def __init__(self, game):
        self.game = game
        self.current_area = 'area_0'
        self.current_map = 'map_start'
        
        # This dictionary defines the World Connections
        # Default Format: ('area', 'map', 'direction'): ('new_area', 'new_map')
        self.connections = {
        ('area_0', 'map_start', 'left'): ('area_0', 'map_end'),
        ('area_0', 'map_start', 'right'): ('area_1', 'map_1'),
        ('area_0', 'map_end', 'right'): ('area_0', 'map_start'),
        ('area_1', 'map_1', 'left'):  ('area_0', 'map_start'),
        ('area_1', 'map_1', 'right'): ('area_1', 'map_2'),
        }
        
    def change_map(self, new_area, new_map, direction):
        self.current_area = new_area
        self.current_map = new_map
        
        path = f'{self.current_area}/{self.current_map}.json'
        self.game.tilemap.load(path)
        
        # Position of the player (Mirror Logic)
        # When a new map is loaded essentialy reset one axis to the boundary and keep the other axis relative to where the player was.
        buffer = 16 # Without the buffer the place of the player will be exactly on the boundary of the new map, so the player could be going back and forth between the maps
        # Inside change_map
        if direction == 'right':
            self.game.player.pos[0] = self.game.tilemap.map_bounds['left'] + buffer
        if direction == 'left':
            self.game.player.pos[0] = self.game.tilemap.map_bounds['right'] - self.game.player.size[0] - buffer
        if direction == 'bottom': # Entering from the top of the new map
            self.game.player.pos[1] = self.game.tilemap.map_bounds['top'] + buffer
        if direction == 'top':    # Entering from the bottom of the new map
            self.game.player.pos[1] = self.game.tilemap.map_bounds['bottom'] - self.game.player.size[1] - buffer
        
        # TODO: Add a smother transiton
        self.game.scroll[0] = self.game.player.rect().centerx - self.game.display.get_width() / 2
        self.game.scroll[1] = self.game.player.rect().centery - self.game.display.get_height() / 2
        
    def update(self):
        direction = None
        if self.game.player.pos[0] < self.game.tilemap.map_bounds['left']:
            direction = 'left'
        if self.game.player.pos[0] + self.game.player.size[0] > self.game.tilemap.map_bounds['right']:
            direction = 'right'
        
        if direction:
            key = (self.current_area, self.current_map, direction)
            if key in self.connections:
                new_area, new_map = self.connections[key]
                self.change_map(new_area, new_map, direction)
        