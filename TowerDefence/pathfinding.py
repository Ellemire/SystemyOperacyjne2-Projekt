from map import MAP
from settings import TILE_SIZE

# === PATH FINDING ===
def get_path():
    visited, path = set(), []

    # Find the first tile with value 1 (start of the path)
    for y, row in enumerate(MAP):
        for x, tile in enumerate(row):
            if tile == 1:
                start = (x, y)
                break
        else:
            continue
        break

    queue = [start]  # Initialize BFS queue with starting point

    while queue:
        cx, cy = queue.pop(0)  # Current tile coordinates
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))

        # Convert tile coordinates to pixel coordinates (center of tile)
        path.append((cx * TILE_SIZE + TILE_SIZE // 2, cy * TILE_SIZE + TILE_SIZE // 2))

        # Explore neighbors: up, right, down, left
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = cx + dx, cy + dy
            # Check bounds and if neighbor is part of the path
            if (
                0 <= ny < len(MAP)
                and 0 <= nx < len(MAP[0])
                and MAP[ny][nx] == 1
                and (nx, ny) not in visited
            ):
                queue.append((nx, ny))

    return path

# List of pixel coordinates representing the enemy path
path_points = get_path()
