import os

import pygame

BASE_IMG_PATH = 'assets/images/'

def load_image(path):
    img = pygame.image.load(f'{BASE_IMG_PATH}{path}').convert() # This converts the internal representation of this image in pygame and makes more efficient for rendering
    img.set_colorkey((0, 0, 0)) # Everything on the screen that is black will be considered transparent.
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(f'{BASE_IMG_PATH}{path}')):
        images.append(load_image(f'{path}/{img_name}'))
    return images

class Animation:
    def __init__(self, images, img_dur=5, loop=True): # TODO: Maybe it's better to create a system where eachframe has an assigned duration (search for the others DaFluffyPotato's codes)
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
    def copy(self): # In Python, if you have a object and you assigned something else to that same object it will be a reference to it instead of actually copying it
        '''This isn't actually making a copy of the images, it's just getting the same reference, so if you change on of them it will affect both.'''    
        return Animation(self.images, self.img_duration, self.loop) # This is beneficial because it does not consume extra memory since all “copies” are looking at the same element.

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images)) # Rest of division in Python is REALLY good to create loops
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1) 
            # Since there's no loop, i.e., the animation only happens when a certain event occurs, it's important to remember that the animation cannot exceed the boundaries of the index, hence the -1.
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
            
    def img(self): # Instead of actually rendering it to a surface it's better to get the current image of the animation because that's a little bit more flexible
        return self.images[int(self.frame / self.img_duration)] # It's dividing the frame by how long each image is supposed to show for
        # To be clear I'll increment frame animation value every single frame of the game and then every single time it crosses this threshold (self.img_duration) the role value, 
        # once it's truncated to an integer, will go up by one and that will be used to select which image needs to be displayed