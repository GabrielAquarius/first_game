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