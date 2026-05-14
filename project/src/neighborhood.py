import random

def _clone_solution(solution):
    return [rides[:] for rides in solution]

def get_neighbors(solution, num_neighbors=50):
    neighbors = []
    
    for _ in range(num_neighbors):
        candidate = get_random_neighbor(solution)
        neighbors.append(candidate)
        
    return neighbors

def get_random_neighbor(solution):
    operations = [0, 1, 2]
    random.shuffle(operations)

    for op in operations:
        candidate = _clone_solution(solution)
        if op == 0 and _apply_random_move(candidate): return candidate
        if op == 1 and _apply_random_swap(candidate): return candidate
        if op == 2 and _apply_random_reorder(candidate): return candidate

    return _clone_solution(solution)

def _apply_random_move(candidate):
    non_empty_vehicles = [i for i, rides in enumerate(candidate) if rides]
    if not non_empty_vehicles or len(candidate) < 2: return False
    
    from_vehicle = random.choice(non_empty_vehicles)
    to_options = [i for i in range(len(candidate)) if i != from_vehicle]
    if not to_options: return False
    to_vehicle = random.choice(to_options)

    ride_idx = random.randrange(len(candidate[from_vehicle]))
    ride = candidate[from_vehicle].pop(ride_idx)
    insert_pos = random.randrange(len(candidate[to_vehicle]) + 1)
    candidate[to_vehicle].insert(insert_pos, ride)
    return True

def _apply_random_swap(candidate):
    non_empty_vehicles = [i for i, rides in enumerate(candidate) if rides]
    if len(non_empty_vehicles) < 2: return False
    
    v1, v2 = random.sample(non_empty_vehicles, 2)
    r1 = random.randrange(len(candidate[v1]))
    r2 = random.randrange(len(candidate[v2]))
    
    candidate[v1][r1], candidate[v2][r2] = candidate[v2][r2], candidate[v1][r1]
    return True

def _apply_random_reorder(candidate):
    valid_vehicles = [i for i, rides in enumerate(candidate) if len(rides) >= 2]
    if not valid_vehicles: return False
    
    v = random.choice(valid_vehicles)
    i, j = random.sample(range(len(candidate[v])), 2)
    candidate[v][i], candidate[v][j] = candidate[v][j], candidate[v][i]
    return True