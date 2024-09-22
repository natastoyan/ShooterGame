from sprite_object import *
from npc import *
class ObjectFabric:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc/soldier'
        # self.static_sprite_path = 'resources/static_sprites/'
        # self.animated_sprite_path = 'resources/animated_sprites/'
        add_sprite = self.add_sprite
        self.npc_positions = {}

        #sprite map
        #self.add_sprite(StaticSprite(game))
        #add_sprite(AnimatedSprite(game))
        pos_list = [(11.5, 3.5), (11.5, 6.5), (10.5, 7.5), (5.5, 7.5), (1.5, 7.5)]

        for pos in pos_list:
            add_sprite(AnimatedSprite(game, path='resources/animated_sprites/green_light/0.png', pos=pos))

        # add_sprite(AnimatedSprite(game,  path='resources/animated_sprites/green_light/0.png',
        #          pos=(10.5, 6.5)))
        # add_sprite(AnimatedSprite(game, path='resources/animated_sprites/green_light/0.png',
        #                           pos=(10.5, 7.5)))
        # add_sprite(AnimatedSprite(game, path='resources/animated_sprites/red_light/0.png',
        #                           pos=(5.5, 7.5)))
        # add_sprite(AnimatedSprite(game, path='resources/animated_sprites/red_light/0.png',
        #                           pos=(1.5, 7.5)))

        # npc map
        self.add_npc(Npc(game))
        self.add_npc(Npc(game=game, pos=(1.5, 7.5)))

    def update(self):
        self.npc_positions = [npc.map_pos for npc in self.npc_list]
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        [self.npc_list.remove(npc) for npc in self.npc_list if npc.to_delete]

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

