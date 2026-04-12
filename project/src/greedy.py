from models import Vehicle
from simulation import ride_simulation


def greedy_heuristic(vehicle, ride, bonus):
    temp_vehicle = Vehicle(vehicle.id, vehicle.row, vehicle.column, vehicle.time)
    (points, cost) = ride_simulation(temp_vehicle, ride, bonus)

    if cost <= 0:
        return 0
    
    return points / cost
    

def greedy_solution(problem):
    # Inicializar veículos e solução
    vehicles = [Vehicle(id) for id in range(problem.vehicles)]
    solution = [[] for _ in range(problem.vehicles)]

    # O SEGREDO DO SUCESSO: Ordenar as viagens pela hora de início (earliest_start)
    # Assim só precisamos de iterar uma única vez pelas viagens!
    sorted_rides = sorted(problem.rides, key=lambda r: r.earliest_start)

    for ride in sorted_rides:
        best_vehicle = None
        best_value = 0

        # Para esta viagem específica, qual é o melhor carro disponível agora?
        for vehicle in vehicles:
            value = greedy_heuristic(vehicle, ride, problem.bonus)

            if value > best_value:
                best_value = value
                best_vehicle = vehicle
                
        # Se algum carro conseguiu um valor positivo, atribui e avança
        if best_vehicle is not None and best_value > 0:
            solution[best_vehicle.id].append(ride)
            ride_simulation(best_vehicle, ride, problem.bonus)

    return solution