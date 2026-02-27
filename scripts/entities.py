import pygame

class PhysicsEntity:
    """
    Attributes:
    game (): allows everything in the Game class to be accessible by this class.
    e_type ():
    pos (List[]): position of each entity 
    size (): size of each entity
    """
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) # This will convert any iterable in to a list
        # There's two reasons for this:
        # 1° If you change the position of an entity that uses this list to move, you will change the position of all other entities that also use this list.
        # 2° If you use a tuple you can't change individual values, so it's better to use a list
        # TODO: Consider using the pygame.math.Vector2 function.
        self.size = size
        self.velocity = [0.0, 0.0] # The derivative of position is velocity and the derivative of velocity is acceleration so the relationships are similiar.
        # To explain, velocity is just used to represent the rate of change in the position and the acceleration will be the rate o change in velocity.
        self.collisions = {'up':False, 'down':False, 'right':False, 'left':False}
        
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up':False, 'down':False, 'right':False, 'left':False}
        
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1]) 
        # This' a Vector that represents how much the entity should be moved in this frame based on who much we want to force it to move in this particular frame plus however much there are in velocity
        
        # Bellow is the AABB (Axis-Aligned Bounding Box)
        # Without separating the axes when checking for collisions, there would be a “corner bug”: the player would get stuck on the edge of blocks because the code would not know whether to push them out to the side or up/down. 
        # This would cause strange behavior where the character appears to “stick” to the wall or shake.
        self.pos[0] += frame_movement[0] # Update the X position based on frame movement of X
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
                
        self.pos[1] += frame_movement[1] # Update the Y position based on frame movement of Y
        # Boolenas can be converted to integers (True = 1, False = 0). Since the update function receives the self.movement attribute, which is Boolean, as a parameter, this means that 
        # if both keys (of opposite directions) are pressed at the same time, the result value will be 0 and the character will not move; if only one is pressed, the counter increases by 1 + velocity for one of the directions.
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        
        self.velocity[1] = min(5, self.velocity[1] + 0.1) # Add gravity (Changing the Y axis)
        # I'm applying the idea of terminal velocity, an object will have a maximum achievable velocity while it's falling when acceleration stops, this happens when the resistance of the medium equals the force of gravity, maintaining the same velocity until the end of the journey.

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        
    def render(self, surf, offset=(0, 0)):
        surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        # self.screen.blit(self.img, self.img_pos) → blit means (Bit Block Transfer). Essentially, is an operation that copies pixels (a section of memory) from a source surface (such as an image of a character) to a destination surface (such as your game window).
        # In pygame a surface is basically just an image so the window itself has a surface which is the main one render onto that's the screen (the screen itself is a special type of surface)
        # but most surfaces are an image loaded in memory, it's not necessarily represent the screen or something like that. This means that it's possible to blit the screen onto the image.
        # self.img.blit(self.screen, self.img_pos), because they're both surfaces. It's possible to blit any surface onto another surface and then at a given location (it's just merge different images)
        # ⤷ Besides that, when this' executed and the image moves on the screen, there'll be an image being rendered on top of another image that has already been rendered causing a trail effect
        #   To solve this is important to clear the screen every frame (self.screen.fill()). Note: This means that the entire screen is rendered and everything is redrawn from scratch every frame.