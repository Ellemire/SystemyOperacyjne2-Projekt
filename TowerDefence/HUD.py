import pygame
from settings import *
from tower import *
from map import *

def draw_hud(screen, font, money, lives, wave, waves, selected_tower_class):
    # Informacje o stanie gry
    screen.blit(font.render(f"Money: {money}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Lives: {lives}", True, WHITE), (10, 30))
    screen.blit(font.render(f"Wave: {min(wave, len(waves))}/{len(waves)}", True, WHITE), (WIDTH - 200, 10))

    # Dostępne wieże i ich koszt
    screen.blit(font.render(f"1: Base ({BaseTower.cost})  3: Fast ({FastTower.cost})  3: Sniper ({SniperTower.cost})", True, WHITE), (10, 50))

    # Wybrana wieża
    selected_name = selected_tower_class.__name__.replace("Tower", "")
    screen.blit(font.render(f"Selected: {selected_name}", True, (255, 255, 0)), (10, 70))

def draw_ghost_tower(screen):
    # Pobranie pozycji kursora
    mx, my = pygame.mouse.get_pos()
    tile_x, tile_y = mx // TILE_SIZE, my // TILE_SIZE
    
    # Sprawdzamy, czy miejsce jest wolne
    if MAP[tile_y][tile_x] == 0:
        ghost_color = (255, 255, 255, 100)
        ghost_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        
        # Zaznaczony punkt
        pygame.draw.circle(ghost_surface, ghost_color, (TILE_SIZE // 2, TILE_SIZE // 2), 5)
        screen.blit(ghost_surface, (tile_x * TILE_SIZE, tile_y * TILE_SIZE))
