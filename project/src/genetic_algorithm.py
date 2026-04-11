import random

from evaluator import evaluate_solution
from greedy import greedy_solution


DEFAULT_POPULATION_SIZE = 30
DEFAULT_GENERATIONS = 80
DEFAULT_TOURNAMENT_SIZE = 3
DEFAULT_ELITE_COUNT = 4
DEFAULT_MUTATION_RATE = 0.35
DEFAULT_ORDER_CROSSOVER_PROB = 0.5


def clone_solution(solution):
    return [rides[:] for rides in solution]


def flatten_solution(solution):
    rides = []
    for vehicle_rides in solution:
        rides.extend(vehicle_rides)
    return rides


def build_solution_from_order(problem, ordered_rides):
    vehicles = problem.vehicles
    if vehicles <= 0:
        return []

    solution = [[] for _ in range(vehicles)]
    for index, ride in enumerate(ordered_rides):
        solution[index % vehicles].append(ride)

    return solution


def normalize_solution(problem, solution):
    if problem.vehicles <= 0:
        return []

    normalized = [[] for _ in range(problem.vehicles)]

    # Keep first occurrence and preserve per-vehicle ordering.
    seen = set()
    for vehicle_idx, rides in enumerate(solution):
        for ride in rides:
            if ride.id in seen:
                continue
            seen.add(ride.id)
            normalized[vehicle_idx].append(ride)

    # Repair missing rides so each ride appears exactly once.
    for ride in problem.rides:
        if ride.id in seen:
            continue
        target_vehicle = min(range(problem.vehicles), key=lambda idx: len(normalized[idx]))
        normalized[target_vehicle].append(ride)
        seen.add(ride.id)

    return normalized


def random_solution(problem):
    rides = list(problem.rides)
    random.shuffle(rides)
    return build_solution_from_order(problem, rides)


def initial_population(problem):
    population = []

    # Seed the population with one heuristic solution for faster convergence.
    population.append(clone_solution(greedy_solution(problem)))

    while len(population) < DEFAULT_POPULATION_SIZE:
        population.append(random_solution(problem))

    return population


def fitness(problem, solution):
    return evaluate_solution(problem, solution)


def tournament_selection(problem, population, fitness_cache):
    sample_size = min(DEFAULT_TOURNAMENT_SIZE, len(population))
    contenders = random.sample(population, sample_size)
    contenders.sort(key=lambda candidate: fitness_cache[id(candidate)], reverse=True)
    return contenders[0]


def ordered_crossover(problem, parent_a, parent_b):
    rides_a = flatten_solution(parent_a)
    rides_b = flatten_solution(parent_b)

    size = len(rides_a)
    if size == 0:
        return clone_solution(parent_a)

    left, right = sorted(random.sample(range(size), 2)) if size > 1 else (0, 0)

    child = [None] * size
    child[left:right + 1] = rides_a[left:right + 1]

    used = {ride.id for ride in child if ride is not None}
    insert_at = (right + 1) % size

    for ride in rides_b:
        if ride.id in used:
            continue
        child[insert_at] = ride
        insert_at = (insert_at + 1) % size

    # Fill any potential gaps to guarantee a valid permutation.
    if any(ride is None for ride in child):
        present_ids = {ride.id for ride in child if ride is not None}
        missing = [ride for ride in problem.rides if ride.id not in present_ids]
        for idx, value in enumerate(child):
            if value is None:
                child[idx] = missing.pop(0)

    return build_solution_from_order(problem, child)


def vehicle_based_crossover(problem, parent_a, parent_b):
    vehicle_count = problem.vehicles
    if vehicle_count <= 0:
        return []

    child = [[] for _ in range(vehicle_count)]
    chosen_count = random.randint(1, vehicle_count)
    inherited_vehicles = set(random.sample(range(vehicle_count), chosen_count))

    used = set()

    # Copy full vehicle plans from parent A for selected vehicles.
    for vehicle_idx in inherited_vehicles:
        for ride in parent_a[vehicle_idx]:
            if ride.id in used:
                continue
            child[vehicle_idx].append(ride)
            used.add(ride.id)

    # Fill remaining rides using parent B assignments and order.
    for vehicle_idx, rides in enumerate(parent_b):
        for ride in rides:
            if ride.id in used:
                continue
            child[vehicle_idx].append(ride)
            used.add(ride.id)

    return child


def crossover(problem, parent_a, parent_b):
    if random.random() < DEFAULT_ORDER_CROSSOVER_PROB:
        return ordered_crossover(problem, parent_a, parent_b)
    return vehicle_based_crossover(problem, parent_a, parent_b)


def mutate_swap(solution):
    positions = []
    for vehicle_idx, rides in enumerate(solution):
        for ride_idx, _ in enumerate(rides):
            positions.append((vehicle_idx, ride_idx))

    if len(positions) < 2:
        return False

    (v1, r1), (v2, r2) = random.sample(positions, 2)
    solution[v1][r1], solution[v2][r2] = solution[v2][r2], solution[v1][r1]
    return True


def mutate_move(solution):
    non_empty_vehicles = [idx for idx, rides in enumerate(solution) if rides]
    if not non_empty_vehicles or len(solution) < 2:
        return False

    from_vehicle = random.choice(non_empty_vehicles)
    to_options = [idx for idx in range(len(solution)) if idx != from_vehicle]
    if not to_options:
        return False

    to_vehicle = random.choice(to_options)

    ride_idx = random.randrange(len(solution[from_vehicle]))
    ride = solution[from_vehicle].pop(ride_idx)

    insert_pos = random.randrange(len(solution[to_vehicle]) + 1)
    solution[to_vehicle].insert(insert_pos, ride)
    return True


def mutate_reorder(solution):
    reorderable_vehicles = [idx for idx, rides in enumerate(solution) if len(rides) >= 2]
    if not reorderable_vehicles:
        return False

    vehicle_idx = random.choice(reorderable_vehicles)
    i, j = random.sample(range(len(solution[vehicle_idx])), 2)
    solution[vehicle_idx][i], solution[vehicle_idx][j] = solution[vehicle_idx][j], solution[vehicle_idx][i]
    return True


def mutate(solution):
    mutated = clone_solution(solution)

    mutation_ops = [mutate_move, mutate_swap, mutate_reorder]
    random.shuffle(mutation_ops)

    for mutate_op in mutation_ops:
        if mutate_op(mutated):
            return mutated

    # No feasible mutation for this chromosome shape.
    if len(flatten_solution(mutated)) < 2:
        return mutated

    return mutated


def genetic_algorithm_solution(problem, return_history=False):
    population = initial_population(problem)

    best_solution = None
    best_score = -1
    history = []

    for generation in range(DEFAULT_GENERATIONS):
        fitness_cache = {id(candidate): fitness(problem, candidate) for candidate in population}

        generation_best = max(population, key=lambda candidate: fitness_cache[id(candidate)])
        generation_best_score = fitness_cache[id(generation_best)]

        if generation_best_score > best_score:
            best_score = generation_best_score
            best_solution = clone_solution(generation_best)

        history.append({"generation": generation, "best_score": best_score})

        elites = sorted(population, key=lambda candidate: fitness_cache[id(candidate)], reverse=True)[:DEFAULT_ELITE_COUNT]
        new_population = [clone_solution(elite) for elite in elites]

        while len(new_population) < DEFAULT_POPULATION_SIZE:
            parent_a = tournament_selection(problem, population, fitness_cache)
            parent_b = tournament_selection(problem, population, fitness_cache)

            child = crossover(problem, parent_a, parent_b)
            if random.random() < DEFAULT_MUTATION_RATE:
                child = mutate(child)

            new_population.append(normalize_solution(problem, child))

        population = new_population

    if return_history:
        return best_solution, best_score, history

    return best_solution, best_score
