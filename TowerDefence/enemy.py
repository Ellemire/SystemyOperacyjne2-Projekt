import math
import pygame
from settings import RED
from settings import screen
from pathfinding import get_path, path_points
from assets import *

class BaseEnemy:
    def __init__(self):
        self.path = path_points
        self.path_index = 0
        self.pos = list(self.path[0])
        self.speed = 1.0
        self.health = self.max_health = 100
        self.color = RED
        self.animations = {
            "right": slime_enemy_walk_right,
            "up": slime_enemy_walk_up,
            "down": slime_enemy_walk_down,
            "death": slime_enemy_death
        }
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 5
        self.direction = "down"
        self.dead = False

    def move(self):
        if self.path_index < len(self.path) - 1:
            target = self.path[self.path_index + 1]
            dx, dy = target[0] - self.pos[0], target[1] - self.pos[1]
            dist = math.hypot(dx, dy)

            if abs(dx) > abs(dy):
                self.direction = "right" if dx < 0 else "left"
            else:
                self.direction = "down" if dy > 0 else "up"

            if dist < self.speed:
                self.pos = list(target)
                self.path_index += 1
            else:
                self.pos[0] += dx / dist * self.speed
                self.pos[1] += dy / dist * self.speed

            self.anim_timer += 1

        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            anim_dir = self.direction if self.direction != "left" else "right"
            self.anim_index = (self.anim_index + 1) % len(self.animations[anim_dir])

    def draw(self):
        if self.health <= 0:
            self.dead = True
            frames = self.animations["death"]
            frame = frames[self.anim_index]
        else:
            anim_dir = self.direction if self.direction != "left" else "right"
            frames = self.animations[anim_dir]
            frame = frames[self.anim_index]
            if self.direction == "left":
                frame = pygame.transform.flip(frame, True, False)

        rect = frame.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
        screen.blit(frame, rect)

        # Health bar
        hp_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (0, 0, 0), (self.pos[0]-10, self.pos[1]-20, 20, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.pos[0]-10, self.pos[1]-20, 20 * hp_ratio, 5))

    def hit(self, damage):
        self.health -= damage

    def has_finished(self):
        return self.path_index >= len(self.path) - 1

class FastEnemy(BaseEnemy):
    def __init__(self):
        super().__init__()
        self.speed = 2.0
        self.health = self.max_health = 60
        self.color = (255, 100, 100)
        self.animations = {
            "right": fast_enemy_walk_right,
            "up": fast_enemy_walk_up,
            "down": fast_enemy_walk_down,
            "death": fast_enemy_death
        }

class NormalEnemy(BaseEnemy):
    def __init__(self):
        super().__init__()
        self.speed = 1.0
        self.health = self.max_health = 100
        self.color = RED

class TankEnemy(BaseEnemy):
    def __init__(self):
        super().__init__()
        self.speed = 0.5
        self.health = self.max_health = 250
        self.color = (100, 0, 0)
        self.animations = {
            "right": tank_enemy_walk_right,
            "up": tank_enemy_walk_up,
            "down": tank_enemy_walk_down,
            "death": tank_enemy_death
        }
