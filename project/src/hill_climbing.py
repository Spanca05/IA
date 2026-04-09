from neighborhood import get_neighbors
from evaluator import evaluate_solution


def get_best_neighbor(problem, neighbors, current_score):
    best_neighbor = None
    best_score = current_score

    for neighbor in neighbors:
        score = evaluate_solution(problem, neighbor)

        if score > best_score:
            best_neighbor = neighbor
            best_score = score

    return best_neighbor, best_score

def hill_climbing_solution(problem, solution):
    current_solution = solution
    current_score = evaluate_solution(problem, current_solution)

    while True:
        neighbors = get_neighbors(current_solution)

        if not neighbors:
            break

        best_neighbor, best_score = get_best_neighbor(problem, neighbors, current_score)

        if best_neighbor is None:
            break
        
        current_solution = best_neighbor
        current_score = best_score

    return current_solution, current_score

