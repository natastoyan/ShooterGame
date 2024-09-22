import math
import datetime
from sprite_object import *
from random import randint, random, choice
from pathfinding import *


class Npc(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos=(10.5, 6.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.see_player = False
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        self.attack_dist = randint(3, 6)
        self.speed = 0.01
        self.size = 20
        self.health = 100
        self.attack_damage = 10
        self.accuracy = 0.15
        self.attack_dist = randint(3, 6)

        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.frame_counter = 0
        self.player_search_trigger = False
        self.to_delete = False
        self.killed_time = None

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()
        pg.draw.circle(self.game.screen, 'blue', (self.x * 10, self.y * 10), 3)
        self.draw_ray_cast()

    def movement(self):
        # next_pos = self.game.player.map_pos
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos

        # pg.draw.rect(self.game.screen, 'blue', (100 * next_x, 100 * next_y, 100, 100))
        angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
        dx = math.cos(angle) * self.speed
        dy = math.sin(angle) * self.speed
        self.check_wall_collision(dx, dy)

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def animate_attack(self):
        self.animate(self.attack_images)

    def animate_death(self):
        if not self.alive:
            # if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
            if self.animation_trigger and self.frame_counter < len(self.death_images) - 1:
                self.image = self.death_images[0]
                self.death_images.rotate(-1)
                self.frame_counter += 1

    def attack(self):
        if self.animation_trigger:
            self.animate_attack()
            self.game.sound.npc_shot.play()
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)

    def check_if_hit(self):
        if self.see_player and self.game.player.shot:
            if self.check_if_in_center():
                self.game.sound.npc_pain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.game.sound.npc_pain.play()
            self.killed_time = datetime.datetime.now()

    def check_if_in_center(self):
        return HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width

    def run_logic(self):
        if self.alive:
            self.see_player = self.check_if_seen_by_player()
            self.check_if_hit()
            if self.pain:
                self.animate_pain()
            elif self.see_player:
                self.player_search_trigger = True
                if self.dist < self.attack_dist:
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()
            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()
            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()
            if datetime.datetime.now() - self.killed_time > datetime.timedelta(seconds=10):
                self.to_delete = True

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def check_if_seen_by_player(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0  #расстояние до ближ стены
        player_dist_v, player_dist_h = 0, 0  #расстояние до игрока

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    def draw_ray_cast(self):
        pg.draw.circle(self.game.screen, 'red', (10 * self.x, 10 * self.y), 3)
        if self.check_if_seen_by_player():
            pg.draw.line(self.game.screen, 'orange', (10 * self.game.player.x, 10 * self.game.player.y),
                         (10 * self.x, 10 * self.y), 2)
