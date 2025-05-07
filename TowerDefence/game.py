import pygame
import math
import threading
import time

pygame.init()

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

# === SETUP ===
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# === MAP ===
MAP = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# === PATH ===
def get_path():
    visited, path = set(), []
    for y, row in enumerate(MAP):
        for x, tile in enumerate(row):
            if tile == 1:
                start = (x, y)
                break
        else:
            continue
        break

    queue = [start]
    while queue:
        cx, cy = queue.pop(0)
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))
        path.append((cx * TILE_SIZE + TILE_SIZE // 2, cy * TILE_SIZE + TILE_SIZE // 2))

        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= ny < len(MAP) and 0 <= nx < len(MAP[0]) and MAP[ny][nx] == 1 and (nx, ny) not in visited:
                queue.append((nx, ny))
    return path

path_points = get_path()

# === LOCKS ===
enemy_lock = threading.Lock()
projectile_lock = threading.Lock()
money_lock = threading.Lock()

# === CLASSES ===
class BaseEnemy:
    def __init__(self):
        self.path = path_points
        self.path_index = 0
        self.pos = list(self.path[0])
        self.speed = 1.0
        self.health = self.max_health = 100
        self.color = RED

    def move(self):
        if self.path_index < len(self.path) - 1:
            target = self.path[self.path_index + 1]
            dx, dy = target[0] - self.pos[0], target[1] - self.pos[1]
            dist = math.hypot(dx, dy)
            if dist < self.speed:
                self.pos = list(target)
                self.path_index += 1
            else:
                self.pos[0] += dx / dist * self.speed
                self.pos[1] += dy / dist * self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), 10)
        hp_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (0, 0, 0), (self.pos[0]-10, self.pos[1]-20, 20, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.pos[0]-10, self.pos[1]-20, 20 * hp_ratio, 5))

    def hit(self, damage):
        self.health -= damage

    def has_finished(self):
        return self.path_index >= len(self.path) - 1

class FastEnemy(BaseEnemy):
    def __init__(self):
        super().__init__()
        self.speed = 2.0
        self.health = self.max_health = 60
        self.color = (255, 100, 100)

class NormalEnemy(BaseEnemy):
    def __init__(self):
        super().__init__()
        self.speed = 1.0
        self.health = self.max_health = 100
        self.color = RED

class TankEnemy(BaseEnemy):
    def __init__(self):
        super().__init__()
        self.speed = 0.5
        self.health = self.max_health = 250
        self.color = (100, 0, 0)

class BaseTower:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.range = 100
        self.fire_rate = 30
        self.timer = 0
        self.damage = 25
        self.color = DARK_GREEN

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x - 15, self.y - 15, 30, 30))
        pygame.draw.circle(screen, (0, 150, 0), (self.x, self.y), self.range, 1)

    def update(self):
        self.timer += 1
        if self.timer >= self.fire_rate:
            with enemy_lock:
                for enemy in enemies:
                    dx = enemy.pos[0] - self.x
                    dy = enemy.pos[1] - self.y
                    if dx * dx + dy * dy <= self.range * self.range and enemy.health > 0:
                        with projectile_lock:
                            projectiles.append(Projectile(self.x, self.y, enemy, self.damage))
                        self.timer = 0
                        break

class FastTower(BaseTower):
    cost = 40
    def __init__(self, x, y):
        super().__init__(x, y)
        self.fire_rate = 10
        self.range = 80
        self.damage = 15
        self.color = (0, 200, 200)

class SniperTower(BaseTower):
    cost = 70
    def __init__(self, x, y):
        super().__init__(x, y)
        self.fire_rate = 40
        self.range = 180
        self.damage = 50
        self.color = (200, 200, 50)

class Projectile:
    def __init__(self, x, y, target, damage):
        self.x, self.y = x, y
        self.target = target
        self.speed = 5
        self.damage = damage

    def move(self):
        dx, dy = self.target.pos[0] - self.x, self.target.pos[1] - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.x += dx / dist * self.speed
            self.y += dy / dist * self.speed
        if dist < self.speed:
            self.target.hit(self.damage)
            return True
        return False

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 5)

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

# === THREAD FUNCTIONS ===
def spawn_wave(wave_index):
    if wave_index >= len(waves): return
    for enemy_class, count in waves[wave_index].items():
        for _ in range(count):
            with enemy_lock:
                enemies.append(enemy_class())
            time.sleep(0.5)

def wave_manager():
    global wave, game_won, running
    total_waves = len(waves)
    while running and wave <= total_waves:
        if not enemies:
            spawn_wave(wave - 1)
            while running:
                with enemy_lock:
                    if not enemies:
                        break
                time.sleep(0.5)
            wave += 1
        time.sleep(0.1)
    while running:
        with enemy_lock:
            if not enemies:
                game_won = True
                running = False
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

# === START GAME ===
start_threads()
selected_tower_class = FastTower

# === MAIN LOOP ===
while running:
    clock.tick(FPS)
    screen.fill(GREEN)

    for y, row in enumerate(MAP):
        for x, tile in enumerate(row):
            if tile == 1:
                pygame.draw.rect(screen, BROWN, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                selected_tower_class = FastTower
            elif event.key == pygame.K_2:
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
                        game_over = True
                        running = False

    for tower in towers:
        tower.draw()

    with projectile_lock:
        for projectile in projectiles:
            projectile.draw()

    screen.blit(font.render(f"Money: {money}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Lives: {lives}", True, WHITE), (10, 30))
    screen.blit(font.render(f"Wave: {min(wave, len(waves))}/{len(waves)}", True, WHITE), (WIDTH - 150, 10))
    screen.blit(font.render(f"1: Fast ({FastTower.cost})  2: Sniper ({SniperTower.cost})", True, WHITE), (10, 50))
    screen.blit(font.render(f"Selected: {'Fast' if selected_tower_class == FastTower else 'Sniper'}", True, WHITE), (10, 70))

    pygame.display.flip()

    if game_won or game_over:
        screen.fill((0, 100, 0) if game_won else (100, 0, 0))
        msg = "Wygrałeś wszystkie fale!" if game_won else "Przegrałeś!"
        text = font.render(msg, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        time.sleep(4)

pygame.quit()
