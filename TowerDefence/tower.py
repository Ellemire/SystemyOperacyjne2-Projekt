import math
import pygame
from settings import screen, RED, BLUE, PINK
from game_state import enemy_lock, enemies, projectile_lock, projectiles
from assets import (
    tower_base_img, tower_fast_img, tower_sniper_img,
    blue_projectile_frames, pink_projectile_frames, red_projectile_frames
)

class BaseTower:
    cost = 30
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.range = 100
        self.fire_rate = 30
        self.timer = 0
        self.damage = 25
        self.color = BLUE
        self.image = tower_base_img
        self.projectile_frames = blue_projectile_frames

    def draw(self):
        rect = self.image.get_rect(midbottom=(self.x, self.y + 20))
        screen.blit(self.image, rect)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.range, 1)

    def update(self):
        self.timer += 1
        if self.timer >= self.fire_rate:
            with enemy_lock:
                for enemy in enemies:
                    dx = enemy.pos[0] - self.x
                    dy = enemy.pos[1] - self.y
                    if dx * dx + dy * dy <= self.range * self.range and enemy.health > 0:
                        with projectile_lock:
                            projectiles.append(Projectile(self.x, self.y, enemy, self.damage, self.projectile_frames))
                        self.timer = 0
                        break

class FastTower(BaseTower):
    cost = 40
    def __init__(self, x, y):
        super().__init__(x, y)
        self.fire_rate = 10
        self.range = 80
        self.damage = 15
        self.color = PINK
        self.image = tower_fast_img
        self.projectile_frames = pink_projectile_frames

class SniperTower(BaseTower):
    cost = 70
    def __init__(self, x, y):
        super().__init__(x, y)
        self.fire_rate = 40
        self.range = 180
        self.damage = 50
        self.color = RED
        self.image = tower_sniper_img
        self.projectile_frames = red_projectile_frames

class Projectile:
    def __init__(self, x, y, target, damage, frames = blue_projectile_frames):
        self.x, self.y = x, y
        self.target = target
        self.speed = 5
        self.damage = damage
        self.frames = frames
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 3

    def move(self):
        dx, dy = self.target.pos[0] - self.x, self.target.pos[1] - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.x += dx / dist * self.speed
            self.y += dy / dist * self.speed
        if dist < self.speed:
            self.target.hit(self.damage)
            return True
        return False

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 5)
        self.anim_timer += 1
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.anim_index = (self.anim_index + 1) % len(self.frames)

        frame = self.frames[self.anim_index]
        rect = frame.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(frame, rect)