import heapq
from collections import deque

# Directions for movement (up, down, left, right)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIRECTION_NAMES = ['up', 'down', 'left', 'right']

def find_target_position(grid):
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 'T':
                return (x, y)
    return None

def is_valid_move(grid, x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != 1

def convert_to_directions(path):
    directions = []
    for i in range(1, len(path)):
        current = path[i - 1]
        next_pos = path[i]
        move = (next_pos[0] - current[0], next_pos[1] - current[1])
        if move in DIRECTIONS:
            direction = DIRECTION_NAMES[DIRECTIONS.index(move)]
            directions.append(direction)
    return directions

# A. Breadth-First Search (BFS)
def find_path_bfs(grid, start):
    target = find_target_position(grid)
    if not target:
        return "Target not found."

    queue = deque([start])
    visited = set([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == target:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return convert_to_directions(list(reversed(path)))

        for i, (dx, dy) in enumerate(DIRECTIONS):
            next_pos = (current[0] + dx, current[1] + dy)
            if is_valid_move(grid, next_pos[0], next_pos[1]) and next_pos not in visited:
                queue.append(next_pos)
                visited.add(next_pos)
                parent[next_pos] = current

    return "No path found."

# B. Depth-First Search (DFS)
def find_path_dfs(grid, start):
    target = find_target_position(grid)
    if not target:
        return "Target not found."
    
    stack = [start]
    visited = set([start])
    parent = {start: None}

    while stack:
        current = stack.pop()
        if current == target:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return convert_to_directions(list(reversed(path)))

        for i, (dx, dy) in enumerate(DIRECTIONS):
            next_pos = (current[0] + dx, current[1] + dy)
            if is_valid_move(grid, next_pos[0], next_pos[1]) and next_pos not in visited:
                stack.append(next_pos)
                visited.add(next_pos)
                parent[next_pos] = current

    return "No path found."

# C. A* Search
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_path_a_star(grid, start):
    target = find_target_position(grid)
    if not target:
        return "Target not found."

    open_set = []
    heapq.heappush(open_set, (0, start))
    g_score = {start: 0}
    f_score = {start: heuristic(start, target)}
    parent = {start: None}
    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == target:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return convert_to_directions(list(reversed(path)))

        visited.add(current)

        for i, (dx, dy) in enumerate(DIRECTIONS):
            next_pos = (current[0] + dx, current[1] + dy)
            if is_valid_move(grid, next_pos[0], next_pos[1]) and next_pos not in visited:
                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score.get(next_pos, float('inf')):
                    parent[next_pos] = current
                    g_score[next_pos] = tentative_g_score
                    f_score[next_pos] = tentative_g_score + heuristic(next_pos, target)
                    heapq.heappush(open_set, (f_score[next_pos], next_pos))

    return "No path found."


# Example Usage:
grid = [
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [1, 0, 0, 'T']
]

start = (0, 0)  # Starting position of the robot

path_bfs = find_path_bfs(grid, start)
path_dfs = find_path_dfs(grid, start)
path_a_star = find_path_a_star(grid, start)

print("BFS Path:", path_bfs)
print("DFS Path:", path_dfs)
print("A* Path:", path_a_star)
