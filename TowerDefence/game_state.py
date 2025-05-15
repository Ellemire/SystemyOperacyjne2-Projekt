import threading
from enemy import FastEnemy, NormalEnemy, TankEnemy

# === GAME STATE ===
enemies = []
towers = []
projectiles = []
money = 1000
lives = 5
wave = 1
game_won = False
game_over = False
running = True

waves = [
    {FastEnemy: 3, NormalEnemy: 5, TankEnemy: 1},
    {FastEnemy: 4, NormalEnemy: 6, TankEnemy: 2},
    {FastEnemy: 5, NormalEnemy: 8, TankEnemy: 3},
    {FastEnemy: 6, NormalEnemy: 10, TankEnemy: 4}
]

# === LOCKS ===
enemy_lock = threading.Lock()
projectile_lock = threading.Lock()
money_lock = threading.Lock()
wave_lock = threading.Lock()
game_lock = threading.Lock()