import pygame

# === CONSTANTS ===
WIDTH, HEIGHT = 800, 600
FPS = 60
TILE_SIZE = 40

# === COLORS ===
WHITE = (255, 255, 255)
GREEN = (34, 177, 76)
BROWN = (185, 122, 87)
RED = (200, 0, 0)
DARK_GREEN = (0, 100, 0)
BLUE = (125, 249, 255)
PINK = (255, 208, 215)

# === SETUP ===
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")
clock = pygame.time.Clock()

def get_font():
    pygame.font.init()
    return pygame.font.SysFont(None, 24)