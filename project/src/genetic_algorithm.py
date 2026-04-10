import random

from evaluator import evaluate_solution
from greedy import greedy_solution


POPULATION_SIZE = 30
GENERATIONS = 80
TOURNAMENT_SIZE = 3
ELITE_COUNT = 4
MUTATION_RATE = 0.35


def _clone_solution(solution):
    return [rides[:] for rides in solution]


def _flatten_solution(solution):
    rides = []
    for vehicle_rides in solution:
        rides.extend(vehicle_rides)
    return rides


def _build_solution_from_order(problem, ordered_rides):
    vehicles = problem.vehicles
    if vehicles <= 0:
        return []

    solution = [[] for _ in range(vehicles)]
    for index, ride in enumerate(ordered_rides):
        solution[index % vehicles].append(ride)

    return solution


def _normalize_solution(problem, solution):
    all_rides = _flatten_solution(solution)

    # Keep each ride only once and preserve the first occurrence order.
    seen = set()
    unique_rides = []
    for ride in all_rides:
        if ride.id in seen:
            continue
        seen.add(ride.id)
        unique_rides.append(ride)

    # Repair missing rides so the chromosome always contains each ride exactly once.
    for ride in problem.rides:
        if ride.id not in seen:
            unique_rides.append(ride)
            seen.add(ride.id)

    return _build_solution_from_order(problem, unique_rides)


def _random_solution(problem):
    rides = list(problem.rides)
    random.shuffle(rides)
    return _build_solution_from_order(problem, rides)


def _initial_population(problem):
    population = []

    # Seed the population with one heuristic solution for faster convergence.
    population.append(_clone_solution(greedy_solution(problem)))

    while len(population) < POPULATION_SIZE:
        population.append(_random_solution(problem))

    return population


def _fitness(problem, solution):
    return evaluate_solution(problem, solution)


def _tournament_selection(problem, population, fitness_cache):
    sample_size = min(TOURNAMENT_SIZE, len(population))
    contenders = random.sample(population, sample_size)
    contenders.sort(key=lambda candidate: fitness_cache[id(candidate)], reverse=True)
    return contenders[0]


def _ordered_crossover(problem, parent_a, parent_b):
    rides_a = _flatten_solution(parent_a)
    rides_b = _flatten_solution(parent_b)

    size = len(rides_a)
    if size == 0:
        return _clone_solution(parent_a)

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

    return _build_solution_from_order(problem, child)


def _mutate(problem, solution):
    mutated = _clone_solution(solution)

    rides = _flatten_solution(mutated)
    if len(rides) < 2:
        return mutated

    # Small mutation: swap two random rides in the global chromosome order.
    i, j = random.sample(range(len(rides)), 2)
    rides[i], rides[j] = rides[j], rides[i]

    return _build_solution_from_order(problem, rides)


def genetic_algorithm_solution(problem):
    population = _initial_population(problem)

    best_solution = None
    best_score = -1

    for _ in range(GENERATIONS):
        fitness_cache = {id(candidate): _fitness(problem, candidate) for candidate in population}

        generation_best = max(population, key=lambda candidate: fitness_cache[id(candidate)])
        generation_best_score = fitness_cache[id(generation_best)]

        if generation_best_score > best_score:
            best_score = generation_best_score
            best_solution = _clone_solution(generation_best)

        elites = sorted(population, key=lambda candidate: fitness_cache[id(candidate)], reverse=True)[:ELITE_COUNT]
        new_population = [_clone_solution(elite) for elite in elites]

        while len(new_population) < POPULATION_SIZE:
            parent_a = _tournament_selection(problem, population, fitness_cache)
            parent_b = _tournament_selection(problem, population, fitness_cache)

            child = _ordered_crossover(problem, parent_a, parent_b)
            if random.random() < MUTATION_RATE:
                child = _mutate(problem, child)

            new_population.append(_normalize_solution(problem, child))

        population = new_population

    return best_solution, best_score
