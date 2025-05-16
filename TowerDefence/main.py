import time
from settings import *
from map import MAP
import game_state
from game_state import *
from enemy import *
from tower import *
from threads import start_threads
from assets import grass_img
from HUD import draw_hud, draw_ghost_tower

# === GAME INITIALIZATION ===
start_threads()
selected_tower_class = BaseTower
font = get_font()

# === MAIN GAME LOOP ===
while running:
    clock.tick(FPS)

    # Drawing the map background
    for y, row in enumerate(MAP):
        for x, tile in enumerate(row):
            if tile == 1:
                # Draw a path tile (brown rectangle)
                pygame.draw.rect(screen, BROWN, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            else:
                # Draw a grass tile
                screen.blit(grass_img, (x * TILE_SIZE, y * TILE_SIZE))

    # Handling events (keyboard, mouse, quit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Tower selection by keyboard
            if event.key == pygame.K_1:
                selected_tower_class = BaseTower
            elif event.key == pygame.K_2:
                selected_tower_class = FastTower
            elif event.key == pygame.K_3:
                selected_tower_class = SniperTower
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Placing a tower with mouse click
            mx, my = pygame.mouse.get_pos()
            tile_x, tile_y = mx // TILE_SIZE, my // TILE_SIZE
            if MAP[tile_y][tile_x] == 0:  # Only place tower on grass
                cost = selected_tower_class.cost
                if money >= cost:
                    # Create and place new tower
                    towers.append(selected_tower_class(
                        tile_x * TILE_SIZE + TILE_SIZE // 2,
                        tile_y * TILE_SIZE + TILE_SIZE // 2
                    ))
                    # Deduct cost
                    with money_lock:
                        money -= cost

    # Drawing enemies
    with enemy_lock:
        for enemy in enemies[:]:
            enemy.draw()
            if enemy.health <= 0:
                enemies.remove(enemy)
                with money_lock:
                    money += 10  # Reward for killing an enemy
            elif enemy.has_finished():
                enemies.remove(enemy)
                with money_lock:
                    lives -= 1  # Player loses a life
                    if lives <= 0:
                        with game_lock:
                            game_over = True
                            running = False

    # Drawing towers
    for tower in towers:
        tower.draw()

    # Drawing projectiles
    with projectile_lock:
        for projectile in projectiles:
            projectile.draw()

    # Sync current wave number from game state
    with wave_lock:
        current_wave = game_state.wave

    # Drawing the HUD (money, lives, wave, etc.)
    draw_hud(screen, font, money, lives, current_wave, waves, selected_tower_class)

    # Drawing the "ghost" preview of the tower at mouse location
    draw_ghost_tower(screen)

    # Display everything drawn in this frame
    pygame.display.flip()

    # Check for end of game (win or lose)
    with game_lock:
        if game_state.game_won or game_over:
            # Show win/lose screen
            screen.fill((0, 100, 0) if game_state.game_won else (100, 0, 0))
            msg = "You won!" if game_state.game_won else "Game Over!"
            text = font.render(msg, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            time.sleep(4)
            break

# Exit the game
pygame.quit()
