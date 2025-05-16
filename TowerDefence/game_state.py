import threading
from enemy import FastEnemy, NormalEnemy, TankEnemy

# === GAME STATE ===

# Lists to keep track of active objects in the game
enemies = []          # All active enemies
towers = []           # All placed towers
projectiles = []      # All active projectiles

# Player state
money = 100          # Starting money
lives = 5             # Lives remaining
wave = 1              # Current wave number

# Game status flags
game_won = False      # True if player wins
game_over = False     # True if player loses
running = True        # Game loop control flag

# Definition of enemy waves (each dictionary = one wave)
# Format: {EnemyClass: count}
waves = [
    {FastEnemy: 3, NormalEnemy: 5, TankEnemy: 1},
    {FastEnemy: 4, NormalEnemy: 6, TankEnemy: 2},
    {FastEnemy: 5, NormalEnemy: 8, TankEnemy: 3},
    {FastEnemy: 6, NormalEnemy: 10, TankEnemy: 4}
]

# === THREADING LOCKS ===
# Locks are used to synchronize access to shared resources in multi-threaded environment

enemy_lock = threading.Lock()        # Protects access to enemies list
projectile_lock = threading.Lock()   # Protects access to projectiles list
money_lock = threading.Lock()        # Ensures safe changes to money
wave_lock = threading.Lock()         # Controls access to current wave variable
game_lock = threading.Lock()         # Protects game status flags (win/lose)
