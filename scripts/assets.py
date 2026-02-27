# This class is basically to load assets out of game.py
import pygame

from .utils import load_image, load_images, Animation

class Assets:
    def __init__(self):
        self.ground = {
            'background': load_image('/grounds/background/background.png'),
            'foreground': load_image('/grounds/foreground/foreground.png'),
        }
        
        self.tile = {
            'grass_1a': load_images('tiles/grass/grass_1a'),
            'grass_1b': load_images('tiles/grass/grass_1b'),
            'grass_plataform': load_images('tiles/grass/grass_platform'), 
            'dirty_1a': load_images('tiles/dirty/dirty_1a'),
            'dirty_1b': load_images('tiles/dirty/dirty_1b'),
            'dirty_plataform': load_images('tiles/dirty/dirty_platform'), 
            'rock_1a': load_images('tiles/rock/rock_1a'),
            'rock_1b': load_images('tiles/rock/rock_1b'),
            'stone': load_images('tiles/stone'),
            'wood': load_images('tiles/wood'),
            'decor': load_images('tiles/decor'),
        }
        
        self.font_assets = {
            'alphabet': load_images('font/alphabet'),
            'numbers': load_images('font/numbers'),
            'specials': load_images('font/specials'),
        }
        
        self.items_assets = {
            'antidote_potion': load_image('items/items/antidote_potion.png'),
            'health_potion': load_image('items/items/health_potion.png'),
            'apple': load_image('items/items/apple.png'),
            'meat': load_image('items/items/meat.png'),
        }
        
        self.hud_assets = {
            'health_menu': load_image('hud/health_menu.png'),
            'coin': load_image('hud/coin.png'),
            'orb': load_image('hud/orb.png'),
            'select': load_images('hud/select'),
        }

        # Dicionário unificado para todas as animações
        self.animations = {
            'player': {
                'idle': Animation(load_images('entities/player/idle'), img_dur=6),
                'run': Animation(load_images('entities/player/run'), img_dur=4),
                'before_or_after_jump': Animation(load_images('entities/player/before_or_after_jump'), img_dur=4),
                'jump_up': Animation(load_images('entities/player/jump_up'), img_dur=4),
                'jump_up_sparkle': Animation(load_images('entities/player/jump_up_sparkle'), img_dur=4),
                'jump_down': Animation(load_images('entities/player/jump_down'), img_dur=4),
                'jump_down_sparkle': Animation(load_images('entities/player/jump_down_sparkle'), img_dur=4),
                'double_jump': Animation(load_images('entities/player/double_jump'), img_dur=4),
                'push': Animation(load_images('entities/player/push'), img_dur=6),
                'death': Animation(load_images('entities/player/death'), img_dur=4),
                'damage': Animation(load_images('entities/player/damage'), img_dur=4),
                'attack': Animation(load_images('entities/player/attack'), img_dur=6),
                'attack_sword': Animation(load_images('entities/player/attack_sword'), img_dur=6),
                'attack_sparkle': Animation(load_images('entities/player/attack_sparkle'), img_dur=6),
            },
            'blue_bat': {
                'idle': Animation(load_images('entities/enemies/bat/blue/idle'), img_dur=6),
                'attack': Animation(load_images('entities/enemies/bat/blue/attack'), img_dur=6),
                'hit': Animation(load_images('entities/enemies/bat/blue/hit'), img_dur=6),
                'death': Animation(load_images('entities/enemies/bat/blue/death'), img_dur=6),
            },
            'orange_bat': {
                'idle': Animation(load_images('entities/enemies/bat/orange/idle'), img_dur=6),
                'attack': Animation(load_images('entities/enemies/bat/orange/attack'), img_dur=6),
                'hit': Animation(load_images('entities/enemies/bat/orange/hit'), img_dur=6),
                'death': Animation(load_images('entities/enemies/bat/orange/death'), img_dur=6),
            },
            'bomber_goblin': {
                'idle': Animation(load_images('entities/enemies/bomber_goblin/idle'), img_dur=6),
                'attack': Animation(load_images('entities/enemies/bomber_goblin/attack'), img_dur=6),
                'hit': Animation(load_images('entities/enemies/bomber_goblin/hit'), img_dur=6),
                'death': Animation(load_images('entities/enemies/bomber_goblin/death'), img_dur=6),
            },
            'goblin': {
                'idle': Animation(load_images('entities/enemies/goblin/idle'), img_dur=6),
                'run': Animation(load_images('entities/enemies/goblin/run'), img_dur=6),
                'attack': Animation(load_images('entities/enemies/goblin/attack'), img_dur=6),
                'hit': Animation(load_images('entities/enemies/goblin/hit'), img_dur=6),
                'death': Animation(load_images('entities/enemies/goblin/death'), img_dur=6),
            },
            'mushroom': {
                'walk': Animation(load_images('entities/enemies/mushroom/walk'), img_dur=6),
                'crush': Animation(load_images('entities/enemies/mushroom/crush'), img_dur=6),
                'hit': Animation(load_images('entities/enemies/mushroom/hit'), img_dur=6),
                'death': Animation(load_images('entities/enemies/mushroom/death'), img_dur=6),
            },
            'slime': {
                'idle': Animation(load_images('entities/enemies/slime/idle'), img_dur=6),
                'walk': Animation(load_images('entities/enemies/slime/walk'), img_dur=6),
                'hit': Animation(load_images('entities/enemies/slime/hit'), img_dur=6),
                'death': Animation(load_images('entities/enemies/slime/death'), img_dur=6),
            },
            'worm': {
                'walk': Animation(load_images('entities/enemies/worm/walk'), img_dur=6),
                'hit': Animation(load_images('entities/enemies/worm/hit'), img_dur=6),
                'death': Animation(load_images('entities/enemies/worm/death'), img_dur=6),
            },
            'bird': {
                'idle': Animation(load_images('entities/fauna/bird/idle'), img_dur=6),
                'walk': Animation(load_images('entities/fauna/bird/walk'), img_dur=6),
                'fly': Animation(load_images('entities/fauna/bird/fly'), img_dur=6),
            },
            'rabbit': {
                'idle': Animation(load_images('entities/fauna/rabbit/idle'), img_dur=6),
                'walk': Animation(load_images('entities/fauna/rabbit/walk'), img_dur=6),
            },
            'bomb': {
                'explosion': Animation(load_images('items/bomb/explosion'), img_dur=6),
                'on_ground': Animation(load_images('items/bomb/on_ground'), img_dur=6),
                'throw': Animation(load_images('items/bomb/throw'), img_dur=6),
            },
            'coin' : {
                'idle': Animation(load_images('items/coin/idle'), img_dur=6),
                'pickup': Animation(load_images('items/coin/pickup'), img_dur=6),
            },
            'orb': {
                 'idle': Animation(load_images('items/orb/idle'), img_dur=6),
                'pickup': Animation(load_images('items/orb/pickup'), img_dur=6),
            }
        }