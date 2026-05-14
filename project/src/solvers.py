from greedy import greedy_solution
from hill_climbing import hill_climbing_solution
from simulated_annealing import simulated_annealing_solution
from genetic_algorithm import genetic_algorithm_solution
from evaluator import evaluate_solution
import random


def _random_initial_solution(problem):
    if problem.vehicles <= 0:
        return []

    rides = list(problem.rides)
    random.shuffle(rides)
    solution = [[] for _ in range(problem.vehicles)]

    for index, ride in enumerate(rides):
        solution[index % problem.vehicles].append(ride)

    return solution


def _build_initial_solution(problem, params=None):
    strategy = (params or {}).get("start_strategy", "warm_start")

    if strategy in ("warm_start", "warm", "greedy"):
        return greedy_solution(problem)
    if strategy in ("cold_start", "cold", "random"):
        return _random_initial_solution(problem)

    raise ValueError("start_strategy must be 'warm_start' or 'cold_start'")


def greedy_solver(problem, params=None):
    solution = greedy_solution(problem)
    score = evaluate_solution(problem, solution)
    history = [score]
    return solution, score, history


def hill_climbing_solver(problem, params=None):
    initial_solution = _build_initial_solution(problem, params=params)
    solution, score, history = hill_climbing_solution(problem, initial_solution)
    return solution, score, history

def simulated_annealing_solver(problem, params=None):
    initial_solution = _build_initial_solution(problem, params=params)
    solution, score, history = simulated_annealing_solution(problem, initial_solution, params=params)
    return solution, score, history


def genetic_algorithm_solver(problem, params=None):
    solution, score, history = genetic_algorithm_solution(problem, return_history=True, **(params or {}))
    return solution, score, history


SOLVERS = {
    "greedy": greedy_solver,
    "hill_climbing": hill_climbing_solver,
    "simulated_annealing": simulated_annealing_solver,
    "genetic_algorithm": genetic_algorithm_solver,
}

def solve_with_algorithm(problem, algorithm, params=None):
    if algorithm not in SOLVERS:
        available = ", ".join(SOLVERS.keys())
        raise ValueError(f"Unknown algorithm: {algorithm}. Available: {available}")
    
    return SOLVERS[algorithm](problem, params=params)
