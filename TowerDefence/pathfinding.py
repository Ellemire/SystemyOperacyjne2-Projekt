from map import MAP
from settings import TILE_SIZE

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