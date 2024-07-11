import pygame as pg
import sys
from map import *
from player import *
from log import *
from raycasting import *
from object_renderer import *
from object_fabric import *
from weapon import *
from sound import *
from pathfinding import *

class Game:
    def __init__(self):
        pg.init()
        #pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()  #an object to help track time
        self.delta_time = 1  #just to initialize
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.log = Log(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        # self.static_sprite = StaticSprite(self)
        # self.animated_sprite = AnimatedSprite(self)
        self.object_fabric = ObjectFabric(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        # self.static_sprite.update()
        # self.animated_sprite.update()
        self.object_fabric.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(
            FPS)  #wtf? tick(framerate=0) -> milliseconds. time in miliseconds since the past frame
        pg.display.set_caption(f'{self.clock.get_fps() : .1f}')

    def draw(self):
        self.screen.fill('black')
        self.map.draw()
        self.player.draw()

        # self.object_renderer.draw()
        # self.weapon.draw()
        # self.log.draw()
        # self.map.draw_mini()
        # self.player.draw_mini()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
