from neighborhood import get_neighbors
from evaluator import evaluate_solution
import random
import math

DEFAULT_PARAMS = {
    "T0": 1000,
    "alpha": 0.95,
    "Tmin": 0.001,
    "max_iterations": 1000,
    "max_no_improvement": 100,
}

def schedule(t, T0, alpha):
    return T0 * (alpha ** t)

def simulated_annealing_solution(problem, initial_solution, params=None):
    merged_params = {**DEFAULT_PARAMS, **(params or {})}

    T0 = merged_params["T0"]
    alpha = merged_params["alpha"]
    Tmin = merged_params["Tmin"]
    max_iterations = merged_params["max_iterations"]
    max_no_improvement = merged_params["max_no_improvement"]

    current_solution = initial_solution
    current_score = evaluate_solution(problem, current_solution)

    best_solution = current_solution
    best_score = current_score
    
    no_improvement = 0
    t = 0
    T = schedule(t, T0, alpha)

    history = [best_score]

    while t < max_iterations and T > Tmin and no_improvement < max_no_improvement:
        neighbors = get_neighbors(current_solution)
        if not neighbors:
            break

        next_solution = random.choice(neighbors)
        next_score = evaluate_solution(problem, next_solution)

        delta = next_score - current_score
        
        if delta > 0:
            current_solution = next_solution
            current_score = next_score
        else:
            prob = math.exp(delta / T)
            if random.random() < prob:
                current_solution = next_solution
                current_score = next_score

        if current_score > best_score:
            best_solution = current_solution
            best_score = current_score
            no_improvement = 0
        else:
            no_improvement += 1


        t += 1
        T = schedule(t, T0, alpha)

        history.append(best_score)

    return best_solution, best_score, history