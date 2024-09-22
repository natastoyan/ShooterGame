import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'
        self.shotgun = self.load_sound('shotgun.wav', 0.7)
        self.npc_pain = self.load_sound('npc_pain.wav', 0.2)
        self.npc_death = self.load_sound('npc_death.wav', 0.2)
        self.npc_shot =self.load_sound('npc_attack.wav', 0.1)
        self.player_pain = self.load_sound('player_pain.wav', 0.8)

    def load_sound(self, file_name, volume: float):
        sound = pg.mixer.Sound(self.path + file_name)
        sound.set_volume(volume)
        return sound
