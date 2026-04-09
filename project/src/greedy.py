from models import Vehicle
from simulation import ride_simulation

def greedy_heuristic(vehicle, ride, bonus):
    temp_vehicle = Vehicle(vehicle.id, vehicle.row, vehicle.column, vehicle.time)
    (points, cost) = ride_simulation(temp_vehicle, ride, bonus)

    if cost == 0:
        return 0
    
    return points / cost
    

def greedy_solution(problem):
    vehicles = []
    remaining_rides = list(problem.rides)
    solution = [[] for _ in range(problem.vehicles)]

    for id in range(problem.vehicles):
        vehicle = Vehicle(id)
        vehicles.append(vehicle)

    while (remaining_rides):
        best_vehicle = None
        best_ride = None
        best_value = 0

        for vehicle in vehicles:
            for ride in remaining_rides:
                value = greedy_heuristic(vehicle, ride, problem.bonus)

                if value > best_value:
                    best_value = value
                    best_vehicle = vehicle
                    best_ride = ride
                
        if best_vehicle is None or best_ride is None or best_value <= 0:
            break

        solution[best_vehicle.id].append(best_ride)
        ride_simulation(best_vehicle, best_ride, problem.bonus)
        remaining_rides.remove(best_ride)

    return solution