import math
import pygame
from settings import screen, RED, BLUE, PINK
from game_state import enemy_lock, enemies, projectile_lock, projectiles
from assets import (
    tower_base_img, tower_fast_img, tower_sniper_img,
    blue_projectile_frames, pink_projectile_frames, red_projectile_frames
)

# === TOWER CLASSES ===
class BaseTower:
    cost = 30  # Cost to build this tower

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.range = 100         # Attack range in pixels
        self.fire_rate = 30      # Frames between shots
        self.timer = 0           # Time since last shot
        self.damage = 25         # Damage per projectile
        self.color = BLUE        # Range circle color
        self.image = tower_base_img
        self.projectile_frames = blue_projectile_frames

    def draw(self):
        # Draw tower image and range circle
        rect = self.image.get_rect(midbottom=(self.x, self.y + 20))
        screen.blit(self.image, rect)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.range, 1)

    def update(self):
        # Increment internal timer and check for enemies in range
        self.timer += 1
        if self.timer >= self.fire_rate:
            with enemy_lock:
                for enemy in enemies:
                    dx = enemy.pos[0] - self.x
                    dy = enemy.pos[1] - self.y
                    if dx * dx + dy * dy <= self.range * self.range and enemy.health > 0:
                        # Fire at enemy and reset timer
                        with projectile_lock:
                            projectiles.append(Projectile(
                                self.x, self.y, enemy, self.damage, self.projectile_frames
                            ))
                        self.timer = 0
                        break

# === FAST TOWER CLASS ===
class FastTower(BaseTower):
    cost = 40

    def __init__(self, x, y):
        super().__init__(x, y)
        self.fire_rate = 10      # Fires faster
        self.range = 80          # Shorter range
        self.damage = 15         # Weaker damage
        self.color = PINK
        self.image = tower_fast_img
        self.projectile_frames = pink_projectile_frames

# === SNIPER TOWER CLASS ===
class SniperTower(BaseTower):
    cost = 70

    def __init__(self, x, y):
        super().__init__(x, y)
        self.fire_rate = 40      # Slower shooting
        self.range = 180         # Long range
        self.damage = 50         # High damage
        self.color = RED
        self.image = tower_sniper_img
        self.projectile_frames = red_projectile_frames

# === PROJECTILE CLASS ===
class Projectile:
    def __init__(self, x, y, target, damage, frames=blue_projectile_frames):
        self.x, self.y = x, y
        self.target = target            # Enemy to follow
        self.speed = 5                  # Speed in pixels per frame
        self.damage = damage            # Damage dealt upon hit
        self.frames = frames            # Animation frames
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 3             # Animation speed (lower = faster)

    def move(self):
        # Move toward target
        dx = self.target.pos[0] - self.x
        dy = self.target.pos[1] - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.x += dx / dist * self.speed
            self.y += dy / dist * self.speed
        # Hit if close enough
        if dist < self.speed:
            self.target.hit(self.damage)
            return True  # Mark for removal
        return False

    def draw(self):
        # Draw animated projectile frame and optional debug circle
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 5)

        # Update animation frame
        self.anim_timer += 1
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.anim_index = (self.anim_index + 1) % len(self.frames)

        # Draw current animation frame
        frame = self.frames[self.anim_index]
        rect = frame.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(frame, rect)
