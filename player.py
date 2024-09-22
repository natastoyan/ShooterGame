from settings import *
import pygame as pg
import math

FORWARD, BACKWARD, LEFT, RIGHT = 'forward', 'backward', 'left', 'right'

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.moves = FORWARD
        self.sin_a = math.sin(self.angle)
        self.cos_a = math.cos(self.angle)
        self.dx, self.dy = 0, 0
        
        self.health = 100

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True

    def get_damage(self, damage):
        self.health -= damage
        self.game.sound.player_pain.play()

    def movement(self):
        self.sin_a = math.sin(self.angle)
        self.cos_a = math.cos(self.angle)
        self.dx, self.dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time

        shift_for_x = speed * self.cos_a
        shift_for_y = speed * self.sin_a
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.moves = FORWARD
            self.dx += shift_for_x
            self.dy += shift_for_y
        if keys[pg.K_s]:
            self.moves = BACKWARD
            self.dx -= shift_for_x
            self.dy -= shift_for_y
        if keys[pg.K_a]:
            self.moves = LEFT
            self.dx += shift_for_y
            self.dy -= shift_for_x
        if keys[pg.K_d]:
            self.moves = RIGHT
            self.dx -= shift_for_y
            self.dy += shift_for_x

        #self.x += self.dx
        #self.y += self.dy
        self.check_wall_collision(self.dx, self.dy)

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw_mini(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 10, self.y * 10),
                     (self.x * 10 + 16 * math.cos(self.angle),
                      self.y * 10 + 16 * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 10, self.y * 10), 3)

    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                     (self.x * 100 * WIDTH * math.cos(self.angle),
                      self.y * 100 * WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 6)
    
    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def calculate_shift(self):
        speed = PLAYER_SPEED * self.game.delta_time

        shift_for_x = speed * self.sin_a
        shift_for_y = speed * self.cos_a
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.dx += shift_for_x
            self.dy += shift_for_y
        if keys[pg.K_s]:
            self.dx -= shift_for_x
            self.dy -= shift_for_y
        if keys[pg.K_a]:
            self.dx += shift_for_x
            self.dy -= shift_for_y
        if keys[pg.K_a]:
            self.dx -= shift_for_x
            self.dy += shift_for_y
        return self.dx, self.dy

    def update(self):
        self.movement()
        self.mouse_control()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return  int(self.x), int(self.y)