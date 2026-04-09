from dataclasses import dataclass
import random
from typing import Dict, List, Tuple

from evaluator import evaluate_solution
from greedy import greedy_solution


@dataclass
class Chromosome:
    permutation: List[int]
    bucket_counts: List[int]

    def copy(self) -> "Chromosome":
        return Chromosome(self.permutation.copy(), self.bucket_counts.copy())


def _build_ride_lookup(problem) -> Dict[int, object]:
    lookup = {}
    for ride in problem.rides:
        if ride.id is None:
            raise ValueError("All rides must have an id to run the genetic algorithm.")
        if ride.id in lookup:
            raise ValueError(f"Duplicate ride id found: {ride.id}")
        lookup[ride.id] = ride
    return lookup


def _all_ride_ids(problem) -> List[int]:
    return [ride.id for ride in problem.rides]


def _random_bucket_counts(total_rides: int, bucket_count: int, rng: random.Random) -> List[int]:
    counts = [0 for _ in range(bucket_count)]
    for _ in range(total_rides):
        counts[rng.randrange(bucket_count)] += 1
    return counts


def _decode_chromosome(problem, chromosome: Chromosome, ride_lookup: Dict[int, object]):
    vehicle_count = problem.vehicles
    expected_bucket_count = vehicle_count + 1  # Last bucket means unassigned rides.

    if len(chromosome.bucket_counts) != expected_bucket_count:
        raise ValueError(
            f"Invalid bucket count length. Expected {expected_bucket_count}, got {len(chromosome.bucket_counts)}."
        )

    if sum(chromosome.bucket_counts) != len(chromosome.permutation):
        raise ValueError("Chromosome bucket counts do not match permutation length.")

    solution = [[] for _ in range(vehicle_count)]
    index = 0

    for vehicle_id in range(vehicle_count):
        count = chromosome.bucket_counts[vehicle_id]
        ride_ids = chromosome.permutation[index:index + count]
        index += count
        solution[vehicle_id] = [ride_lookup[ride_id] for ride_id in ride_ids]

    index += chromosome.bucket_counts[-1]
    if index != len(chromosome.permutation):
        raise ValueError("Chromosome decoding consumed an unexpected number of rides.")

    return solution


def _fitness(problem, chromosome: Chromosome, ride_lookup: Dict[int, object], cache: Dict[Tuple[Tuple[int, ...], Tuple[int, ...]], int]) -> int:
    key = (tuple(chromosome.permutation), tuple(chromosome.bucket_counts))
    if key in cache:
        return cache[key]

    solution = _decode_chromosome(problem, chromosome, ride_lookup)
    score = evaluate_solution(problem, solution)
    cache[key] = score
    return score


def _random_chromosome(problem, rng: random.Random) -> Chromosome:
    ride_ids = _all_ride_ids(problem)
    rng.shuffle(ride_ids)
    bucket_counts = _random_bucket_counts(len(ride_ids), problem.vehicles + 1, rng)
    return Chromosome(ride_ids, bucket_counts)


def _greedy_seed_chromosome(problem, rng: random.Random) -> Chromosome:
    seed_solution = greedy_solution(problem)

    assigned_ids = []
    bucket_counts = []

    for vehicle_rides in seed_solution:
        vehicle_ids = [ride.id for ride in vehicle_rides]
        assigned_ids.extend(vehicle_ids)
        bucket_counts.append(len(vehicle_ids))

    all_ids = [ride.id for ride in problem.rides]
    assigned_set = set(assigned_ids)
    unassigned_ids = [ride_id for ride_id in all_ids if ride_id not in assigned_set]
    rng.shuffle(unassigned_ids)

    permutation = assigned_ids + unassigned_ids
    bucket_counts.append(len(unassigned_ids))

    return Chromosome(permutation, bucket_counts)


def _tournament_selection(population: List[Chromosome], scores: List[int], rng: random.Random, tournament_size: int = 3) -> Chromosome:
    best_index = None
    best_score = None

    for _ in range(tournament_size):
        idx = rng.randrange(len(population))
        score = scores[idx]

        if best_index is None or score > best_score:
            best_index = idx
            best_score = score

    return population[best_index].copy()


def _ordered_crossover(parent_a: Chromosome, parent_b: Chromosome, rng: random.Random) -> Tuple[Chromosome, Chromosome]:
    size = len(parent_a.permutation)
    if size < 2:
        return parent_a.copy(), parent_b.copy()

    left, right = sorted(rng.sample(range(size), 2))

    def build_child(a_perm: List[int], b_perm: List[int]) -> List[int]:
        child = [None] * size
        child[left:right + 1] = a_perm[left:right + 1]

        selected = set(child[left:right + 1])
        b_candidates = [value for value in b_perm if value not in selected]

        cursor = 0
        for i in range(size):
            if child[i] is None:
                child[i] = b_candidates[cursor]
                cursor += 1

        return child

    child_a_perm = build_child(parent_a.permutation, parent_b.permutation)
    child_b_perm = build_child(parent_b.permutation, parent_a.permutation)

    child_a_counts = parent_a.bucket_counts.copy() if rng.random() < 0.5 else parent_b.bucket_counts.copy()
    child_b_counts = parent_b.bucket_counts.copy() if rng.random() < 0.5 else parent_a.bucket_counts.copy()

    return Chromosome(child_a_perm, child_a_counts), Chromosome(child_b_perm, child_b_counts)


def _mutate_chromosome(chromosome: Chromosome, rng: random.Random):
    size = len(chromosome.permutation)

    if size > 1:
        mutation_roll = rng.random()

        if mutation_roll < 0.5:
            i, j = rng.sample(range(size), 2)
            chromosome.permutation[i], chromosome.permutation[j] = chromosome.permutation[j], chromosome.permutation[i]
        elif mutation_roll < 0.8:
            i, j = rng.sample(range(size), 2)
            ride_id = chromosome.permutation.pop(i)
            chromosome.permutation.insert(j, ride_id)
        else:
            i, j = sorted(rng.sample(range(size), 2))
            chromosome.permutation[i:j + 1] = reversed(chromosome.permutation[i:j + 1])

    non_empty_buckets = [idx for idx, count in enumerate(chromosome.bucket_counts) if count > 0]
    if non_empty_buckets and len(chromosome.bucket_counts) > 1 and rng.random() < 0.35:
        from_bucket = rng.choice(non_empty_buckets)
        target_buckets = [idx for idx in range(len(chromosome.bucket_counts)) if idx != from_bucket]
        to_bucket = rng.choice(target_buckets)

        chromosome.bucket_counts[from_bucket] -= 1
        chromosome.bucket_counts[to_bucket] += 1


def ga_solution(
    problem,
    population_size: int = 60,
    generations: int = 250,
    crossover_rate: float = 0.8,
    mutation_rate: float = 0.18,
    elite_size: int = 2,
    stagnation_limit: int = 60,
    seed: int = 42,
):
    if problem.vehicles <= 0:
        raise ValueError("Problem must have at least one vehicle.")

    if population_size < 4:
        raise ValueError("Population size must be at least 4.")

    if elite_size < 1 or elite_size >= population_size:
        raise ValueError("Elite size must be at least 1 and smaller than population size.")

    rng = random.Random(seed)
    ride_lookup = _build_ride_lookup(problem)

    population = []
    greedy_seed_count = max(1, population_size // 5)

    for _ in range(greedy_seed_count):
        population.append(_greedy_seed_chromosome(problem, rng))

    for _ in range(population_size - greedy_seed_count):
        population.append(_random_chromosome(problem, rng))

    fitness_cache: Dict[Tuple[Tuple[int, ...], Tuple[int, ...]], int] = {}

    best_chromosome = None
    best_score = -1
    stagnant_generations = 0

    for _ in range(generations):
        scores = [_fitness(problem, chromosome, ride_lookup, fitness_cache) for chromosome in population]

        ranked = sorted(zip(scores, population), key=lambda item: item[0], reverse=True)
        generation_best_score, generation_best = ranked[0]

        if generation_best_score > best_score:
            best_score = generation_best_score
            best_chromosome = generation_best.copy()
            stagnant_generations = 0
        else:
            stagnant_generations += 1

        if stagnation_limit > 0 and stagnant_generations >= stagnation_limit:
            break

        next_population = [chromosome.copy() for (_, chromosome) in ranked[:elite_size]]

        while len(next_population) < population_size:
            parent_a = _tournament_selection(population, scores, rng)
            parent_b = _tournament_selection(population, scores, rng)

            if rng.random() < crossover_rate:
                child_a, child_b = _ordered_crossover(parent_a, parent_b, rng)
            else:
                child_a, child_b = parent_a.copy(), parent_b.copy()

            if rng.random() < mutation_rate:
                _mutate_chromosome(child_a, rng)
            if rng.random() < mutation_rate:
                _mutate_chromosome(child_b, rng)

            next_population.append(child_a)
            if len(next_population) < population_size:
                next_population.append(child_b)

        population = next_population

    if best_chromosome is None:
        scores = [_fitness(problem, chromosome, ride_lookup, fitness_cache) for chromosome in population]
        best_idx = max(range(len(population)), key=lambda i: scores[i])
        best_chromosome = population[best_idx]

    return _decode_chromosome(problem, best_chromosome, ride_lookup)
