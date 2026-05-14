from models import Vehicle
from simulation import ride_simulation


def greedy_heuristic(vehicle, ride, bonus):
    temp_vehicle = Vehicle(vehicle.id, vehicle.row, vehicle.column, vehicle.time)
    (points, cost) = ride_simulation(temp_vehicle, ride, bonus)

    if cost <= 0:
        return 0
    
    return points / cost
    

def greedy_solution(problem):
    vehicles = [Vehicle(id) for id in range(problem.vehicles)]
    solution = [[] for _ in range(problem.vehicles)]

    sorted_rides = sorted(problem.rides, key=lambda r: r.earliest_start)

    for ride in sorted_rides:
        best_vehicle = None
        best_value = 0

        for vehicle in vehicles:
            value = greedy_heuristic(vehicle, ride, problem.bonus)

            if value > best_value:
                best_value = value
                best_vehicle = vehicle
                
        if best_vehicle is not None and best_value > 0:
            solution[best_vehicle.id].append(ride)
            ride_simulation(best_vehicle, ride, problem.bonus)

    return solution