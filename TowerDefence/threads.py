import time
import threading
from game_state import wave_lock, waves, enemies, enemy_lock,  towers, projectile_lock, projectiles, game_lock, running
import game_state

# === THREAD FUNCTIONS ===
def spawn_wave(wave_index):
    if wave_index >= len(waves): return
    for enemy_class, count in waves[wave_index].items():
        for _ in range(count):
            with enemy_lock:
                enemies.append(enemy_class())
            time.sleep(0.5)

def wave_manager():
    running_ = game_state.running
    with wave_lock:
        wave_ = game_state.wave
    total_waves = len(waves)
    while running_ and wave_ <= total_waves:
        if not enemies:
            spawn_wave(wave_ - 1)
            while running_:
                with enemy_lock:
                    if not enemies:
                        break
                time.sleep(0.5)
            with wave_lock:
                wave_ += 1
                game_state.wave = wave_
                print(f"Fala {game_state.wave} {wave_}")
        time.sleep(0.1)
    while running_:
        with enemy_lock:
            if not enemies:
                with game_lock:
                    game_state.game_won = True
                    game_state.running = False
                    break
        time.sleep(0.5)

def enemy_logic():
    while running:
        with enemy_lock:
            for enemy in enemies:
                enemy.move()
        time.sleep(0.02)

def tower_logic():
    while running:
        for tower in towers:
            tower.update()
        time.sleep(0.05)

def projectile_logic():
    while running:
        with projectile_lock:
            for p in projectiles[:]:
                if p.move():
                    projectiles.remove(p)
        time.sleep(0.01)

def start_threads():
    threading.Thread(target=enemy_logic, daemon=True).start()
    threading.Thread(target=tower_logic, daemon=True).start()
    threading.Thread(target=projectile_logic, daemon=True).start()
    threading.Thread(target=wave_manager, daemon=True).start()
