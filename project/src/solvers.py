from greedy import greedy_solution
from hill_climbing import hill_climbing_solution
from simulated_annealing import simulated_annealing_solution
from genetic_algorithm import genetic_algorithm_solution
from evaluator import evaluate_solution


def greedy_solver(problem):
    solution = greedy_solution(problem)
    score = evaluate_solution(problem, solution)
    history = [score]
    return solution, score, history


def hill_climbing_solver(problem):
    initial_solution = greedy_solution(problem)
    solution, score, history = hill_climbing_solution(problem, initial_solution)
    return solution, score, history

def simulated_annealing_solver(problem, **kwargs):
    initial_solution = greedy_solution(problem)
    solution, score, history = simulated_annealing_solution(problem, initial_solution, **kwargs)
    return solution, score, history


def genetic_algorithm_solver(problem):
    solution, score, history = genetic_algorithm_solution(problem, return_history=True)
    return solution, score, history


SOLVERS = {
    "greedy": greedy_solver,
    "hill_climbing": hill_climbing_solver,
    "simulated_annealing": simulated_annealing_solver,
    "genetic_algorithm": genetic_algorithm_solver,
}


def solve_with_algorithm(problem, algorithm, **kwargs):
    if algorithm not in SOLVERS:
        available = ", ".join(SOLVERS.keys())
        raise ValueError(f"Unknown algorithm: {algorithm}. Available: {available}")
    
    return SOLVERS[algorithm](problem, **kwargs)
