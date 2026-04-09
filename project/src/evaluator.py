from models import Vehicle
from simulation import simulate_rides_for_vehicles


def evaluate_solution(problem, solution):
    vehicles = [Vehicle(i) for i in range(problem.vehicles)]
    
    score = simulate_rides_for_vehicles(
        vehicles,
        solution,
        problem.bonus
    )
    
    return score
