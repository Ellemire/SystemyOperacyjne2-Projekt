import math
import pygame
from settings import RED, screen
from pathfinding import get_path, path_points
from assets import *

# === BASE ENEMY CLASS ===
class BaseEnemy:
    def __init__(self):
        self.path = path_points                # List of waypoints (pixel positions)
        self.path_index = 0                    # Index of current target waypoint
        self.pos = list(self.path[0])          # Current enemy position
        self.speed = 1.0
        self.health = self.max_health = 100
        self.color = RED
        self.animations = {                    # Dictionary of directional animation frames
            "right": slime_enemy_walk_right,
            "up": slime_enemy_walk_up,
            "down": slime_enemy_walk_down,
            "death": slime_enemy_death
        }
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 5                    # Animation frame change interval
        self.direction = "down"                # Current movement direction
        self.dead = False                      # Flag for death animation

    def move(self):
        """Move the enemy along the predefined path of waypoints."""

        # Make sure there are still waypoints left to follow
        if self.path_index < len(self.path) - 1:
            target = self.path[self.path_index + 1]  # Get the next waypoint (x, y)
            dx, dy = target[0] - self.pos[0], target[1] - self.pos[1]  # Vector to target
            dist = math.hypot(dx, dy)  # Euclidean distance to the target

            # === DETERMINE DIRECTION FOR ANIMATION ===
            # Horizontal movement dominates
            if abs(dx) > abs(dy):
                self.direction = "right" if dx < 0 else "left"
            # Vertical movement dominates
            else:
                self.direction = "down" if dy > 0 else "up"

            # === MOVE ENEMY TOWARD TARGET ===
            if dist < self.speed:
                # Snap to target position if very close
                self.pos = list(target)
                self.path_index += 1  # Advance to next waypoint
            else:
                # Normalize movement vector and apply speed
                self.pos[0] += dx / dist * self.speed
                self.pos[1] += dy / dist * self.speed

            # Increase animation timer to control frame change
            self.anim_timer += 1

        # === ANIMATION FRAME UPDATE ===
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0  # Reset timer

            # Use "right" animation also for "left" direction (will be flipped when drawing)
            anim_dir = self.direction if self.direction != "left" else "right"

            # Cycle through animation frames
            self.anim_index = (self.anim_index + 1) % len(self.animations[anim_dir])

    def draw(self):
        """Render the enemy's sprite and health bar on the screen."""

        # Check if the enemy is dead (health below or equal to 0)
        if self.health <= 0:
            self.dead = True  # Mark as dead to prevent further updates
            frames = self.animations["death"]  # Use death animation
            frame = frames[self.anim_index]  # Select current death frame
        else:
            # Determine animation direction (flip 'left' to reuse 'right' frames)
            anim_dir = self.direction if self.direction != "left" else "right"
            frames = self.animations[anim_dir]  # Get frames for the current direction
            frame = frames[self.anim_index]  # Select current animation frame

            # If enemy is moving left, flip the frame horizontally
            if self.direction == "left":
                frame = pygame.transform.flip(frame, True, False)

        # Calculate the frame's rectangle and center it on the enemy's current position
        rect = frame.get_rect(center=(int(self.pos[0]), int(self.pos[1])))

        # Draw the selected animation frame on the screen
        screen.blit(frame, rect)

        # === DRAWING HEALTH BAR ===
        # Calculate the ratio of remaining health (from 0.0 to 1.0)
        hp_ratio = self.health / self.max_health

        # Draw black background rectangle for the health bar (as border)
        pygame.draw.rect(screen, (0, 0, 0), (self.pos[0] - 10, self.pos[1] - 20, 20, 5))

        # Draw green foreground rectangle based on current health
        pygame.draw.rect(screen, (0, 255, 0), (self.pos[0] - 10, self.pos[1] - 20, 20 * hp_ratio, 5))

    def hit(self, damage):
        """Apply damage to enemy."""
        self.health -= damage

    def has_finished(self):
        """Check if enemy reached the end of the path."""
        return self.path_index >= len(self.path) - 1

# === FAST ENEMY (low HP, high speed) ===
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

# === NORMAL ENEMY (balanced) ===
class NormalEnemy(BaseEnemy):
    def __init__(self):
        super().__init__()
        self.speed = 1.0
        self.health = self.max_health = 100
        self.color = RED

# === TANK ENEMY (slow, high HP) ===
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
