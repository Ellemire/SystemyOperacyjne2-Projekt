import pygame
import os

def load_image(name):
    path = os.path.join("assets", name)
    return pygame.image.load(path).convert_alpha()

def slice_tileset(image, frame_width, frame_height, num_frames):
    return [image.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)) for i in range(num_frames)]

# Textures
# grass_img = load_image("Grass 001.png")
grass_img = pygame.transform.scale(load_image("Grass 001.png"), (64, 64))
# path_img = load_image("path.png")

# === Towers (3 wieże: 64x128 każda) ===
tower_image = load_image("Tower 05.png")
tower_base_img = pygame.transform.scale(tower_image.subsurface((0, 0, 64, 128)), (32, 64))
tower_fast_img = pygame.transform.scale(tower_image.subsurface((64, 0, 64, 128)), (32, 64))
tower_sniper_img = pygame.transform.scale(tower_image.subsurface((128, 0, 64, 128)), (32, 64))


# # Enemies

# === FastEnemy ===
slime_enemy_walk_right = slice_tileset(load_image("slime_enemy/walk_right.png"), 48, 48, 6)
slime_enemy_walk_up  = slice_tileset(load_image("slime_enemy/walk_up.png"), 48, 48, 6)
slime_enemy_walk_down  = slice_tileset(load_image("slime_enemy/walk_down.png"), 48, 48, 6)
slime_enemy_death_right = slice_tileset(load_image("slime_enemy/death_right.png"), 48, 48, 6)
slime_enemy_death_up  = slice_tileset(load_image("slime_enemy/death_up.png"), 48, 48, 6)
slime_enemy_death_down  = slice_tileset(load_image("slime_enemy/death_down.png"), 48, 48, 6)
slime_enemy_death = slice_tileset(load_image("slime_enemy/death_down.png"), 48, 48, 6)

# === FastEnemy ===
fast_enemy_walk_right = slice_tileset(load_image("fast_enemy/walk_right.png"), 48, 48, 6)
fast_enemy_walk_up  = slice_tileset(load_image("fast_enemy/walk_up.png"), 48, 48, 6)
fast_enemy_walk_down  = slice_tileset(load_image("fast_enemy/walk_down.png"), 48, 48, 6)
fast_enemy_death      = slice_tileset(load_image("fast_enemy/death_down.png"), 48, 48, 6)

# === TankEnemy ===
tank_enemy_walk_right = slice_tileset(load_image("tank_enemy/walk_right.png"), 48, 48, 6)
tank_enemy_walk_up  = slice_tileset(load_image("tank_enemy/walk_up.png"), 48, 48, 6)
tank_enemy_walk_down  = slice_tileset(load_image("tank_enemy/walk_down.png"), 48, 48, 6)
tank_enemy_death      = slice_tileset(load_image("tank_enemy/death_down.png"), 48, 48, 6)

# === Projectile animation: 12 klatek, 32x32 każda ===
blue_projectile_frames = slice_tileset(load_image("BlueProjectile.png"), 32, 32, 12)
pink_projectile_frames = slice_tileset(load_image("PinkProjectile.png"), 64, 64, 12)
red_projectile_frames = slice_tileset(load_image("RedProjectile.png"), 96, 96, 12)
