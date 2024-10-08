import pygame as pg
from settings import *
from collections import *
import os

class StaticSprite:
    def __init__(self, game, path='resources/static_sprites/candlebra.png',
                 pos=(10.5, 3.5), scale=0.7, shift=0.27):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.path = path
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift

        self.game.raycasting.object_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()
        pg.draw.circle(self.game.screen, 'blue', (self.x * 10, self.y * 10), 3)


class AnimatedSprite(StaticSprite):
    def __init__(self, game, path='resources/animated_sprites/green_light/0.png',
                 pos=(11.5, 3.5), scale=0.7, shift=0.27, animation_time=120):
        StaticSprite.__init__(self, game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.image_number = 0
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        StaticSprite.update(self)
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]
            # if self.image_number < 3:
            #     self.image_number += 1
            # else:
            #     self.image_number = 0
            # self.image = images[self.image_number]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            # print(f"{time_now} - {self.animation_time_prev} = {time_now - self.animation_time_prev}")
            self.animation_time_prev = time_now
            self.animation_trigger = True
            
    def get_images(self, path):
        # images = []
        images = deque()
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                image = pg.image.load(f'{path}/{filename}').convert_alpha()
                images.append(image)
        return images
