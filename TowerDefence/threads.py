import time
import threading
from game_state import wave_lock, waves, enemies, enemy_lock, towers, projectile_lock, projectiles, game_lock, running
import game_state

# === THREAD FUNCTIONS ===

def spawn_wave(wave_index):
    """Spawn enemies for the specified wave index."""
    if wave_index >= len(waves): return
    for enemy_class, count in waves[wave_index].items():
        for _ in range(count):
            with enemy_lock:
                enemies.append(enemy_class())  # Add enemy to the list
            time.sleep(0.8)  # Delay between spawns

def wave_manager():
    """Manage the progression of enemy waves."""
    running_ = game_state.running
    with wave_lock:
        wave_ = game_state.wave
    total_waves = len(waves)

    while running_ and wave_ <= total_waves:
        # If no enemies are present, spawn the next wave
        if not enemies:
            spawn_wave(wave_ - 1)

            # Wait until the wave is fully cleared
            while running_:
                with enemy_lock:
                    if not enemies:
                        break
                time.sleep(0.5)

            # Proceed to next wave
            with wave_lock:
                wave_ += 1
                game_state.wave = wave_

        time.sleep(0.1)

    # After the last wave: check if player has won
    while running_:
        with enemy_lock:
            if not enemies:
                with game_lock:
                    game_state.game_won = True
                    game_state.running = False
                    break
        time.sleep(0.5)

def enemy_logic():
    """Update enemy movement in a separate thread."""
    while running:
        with enemy_lock:
            for enemy in enemies:
                enemy.move()
        time.sleep(0.02)  # Run at ~50 FPS

def tower_logic():
    """Update tower behavior (e.g., targeting, firing)."""
    while running:
        for tower in towers:
            tower.update()
        time.sleep(0.05)  # Run at ~20 FPS

def projectile_logic():
    """Update projectile movement and remove if it hits or exits."""
    while running:
        with projectile_lock:
            for p in projectiles[:]:
                if p.move():  # Returns True if projectile should be removed
                    projectiles.remove(p)
        time.sleep(0.01)  # Run at ~100 FPS

def start_threads():
    """Start all background threads for enemy, tower, projectile logic, and wave control."""
    threading.Thread(target=enemy_logic, daemon=True).start()
    threading.Thread(target=tower_logic, daemon=True).start()
    threading.Thread(target=projectile_logic, daemon=True).start()
    threading.Thread(target=wave_manager, daemon=True).start()
