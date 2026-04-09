from greedy import greedy_solution
from hill_climbing import hill_climbing_solution
from evaluator import evaluate_solution


def greedy_solver(problem):
    solution = greedy_solution(problem)
    score = evaluate_solution(problem, solution)
    return solution, score


def hill_climbing_solver(problem):
    initial_solution = greedy_solution(problem)
    solution, score = hill_climbing_solution(problem, initial_solution)
    return solution, score


SOLVERS = {
    "greedy": greedy_solver,
    "hill_climbing": hill_climbing_solver,
}


def solve_with_algorithm(problem, algorithm):
    if algorithm not in SOLVERS:
        available = ", ".join(SOLVERS.keys())
        raise ValueError(f"Unknown algorithm: {algorithm}. Available: {available}")
    
    return SOLVERS[algorithm](problem)
