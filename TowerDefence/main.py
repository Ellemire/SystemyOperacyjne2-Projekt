import time
from settings import *
from map import MAP
from game_state import *
from enemy import *
from tower import *
from threads import start_threads
from assets import grass_img
from HUD import draw_hud, draw_ghost_tower

# === START GAME ===
start_threads()
selected_tower_class = FastTower
font = get_font()

# === MAIN LOOP ===
while running:
    clock.tick(FPS)

    # Rysowanie tła mapy
    for y, row in enumerate(MAP):
        for x, tile in enumerate(row):
            if tile == 1:
                pygame.draw.rect(screen, BROWN, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            else:
                screen.blit(grass_img, (x * TILE_SIZE, y * TILE_SIZE)) 

    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                selected_tower_class = BaseTower
            elif event.key == pygame.K_2:
                selected_tower_class = FastTower
            elif event.key == pygame.K_3:
                selected_tower_class = SniperTower
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            tile_x, tile_y = mx // TILE_SIZE, my // TILE_SIZE
            if MAP[tile_y][tile_x] == 0:
                cost = selected_tower_class.cost
                if money >= cost:
                    towers.append(selected_tower_class(tile_x * TILE_SIZE + TILE_SIZE // 2, tile_y * TILE_SIZE + TILE_SIZE // 2))
                    with money_lock:
                        money -= cost

    # Rysowanie wrogów
    with enemy_lock:
        for enemy in enemies[:]:
            enemy.draw()
            if enemy.health <= 0:
                enemies.remove(enemy)
                with money_lock:
                    money += 10
            elif enemy.has_finished():
                enemies.remove(enemy)
                with money_lock:
                    lives -= 1
                    if lives <= 0:
                        with game_lock:
                            game_over = True
                            running = False

    # Rysowanie wież
    for tower in towers:
        tower.draw()

    # Rysowanie pocisków
    with projectile_lock:
        for projectile in projectiles:
            projectile.draw()

    # screen.blit(font.render(f"Money: {money}", True, WHITE), (10, 10))
    # screen.blit(font.render(f"Lives: {lives}", True, WHITE), (10, 30))
    # screen.blit(font.render(f"Wave: {min(wave, len(waves))}/{len(waves)}", True, WHITE), (WIDTH - 150, 10))
    # screen.blit(font.render(f"1: Fast ({FastTower.cost})  2: Sniper ({SniperTower.cost})", True, WHITE), (10, 50))
    # screen.blit(font.render(f"Selected: {'Fast' if selected_tower_class == FastTower else 'Sniper'}", True, WHITE), (10, 70))

    # Synchronizacja numeru fali
    with wave_lock:
        current_wave = wave
        print(current_wave)

    # Rysowanie HUD
    draw_hud(screen, font, money, lives, current_wave, waves, selected_tower_class)

    # Rysowanie podglądu wieży
    draw_ghost_tower(screen)

    pygame.display.flip()

    with game_lock:
        if game_won or game_over:
            screen.fill((0, 100, 0) if game_won else (100, 0, 0))
            msg = "Wygrałeś wszystkie fale!" if game_won else "Przegrałeś!"
            text = font.render(msg, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            time.sleep(4)

pygame.quit()
