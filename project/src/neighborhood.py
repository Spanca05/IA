def _clone_solution(solution):
    return [rides[:] for rides in solution]


def get_neighbors(solution):
    neighbors = []

    neighbors.extend(get_move_neighbors(solution))
    neighbors.extend(get_swap_neighbors(solution))
    neighbors.extend(get_reorder_neighbors(solution))

    return neighbors


def get_move_neighbors(solution):
    neighbors = []
    vehicle_count = len(solution)

    for from_vehicle in range(vehicle_count):
        if not solution[from_vehicle]:
            continue

        for ride_idx in range(len(solution[from_vehicle])):
            for to_vehicle in range(vehicle_count):
                if to_vehicle == from_vehicle:
                    continue

                for insert_pos in range(len(solution[to_vehicle]) + 1):
                    candidate = _clone_solution(solution)
                    ride = candidate[from_vehicle].pop(ride_idx)
                    candidate[to_vehicle].insert(insert_pos, ride)
                    neighbors.append(candidate)

    return neighbors


def get_swap_neighbors(solution):
    neighbors = []
    vehicle_count = len(solution)

    for first_vehicle in range(vehicle_count):
        if not solution[first_vehicle]:
            continue

        for second_vehicle in range(first_vehicle + 1, vehicle_count):
            if not solution[second_vehicle]:
                continue

            for first_idx in range(len(solution[first_vehicle])):
                for second_idx in range(len(solution[second_vehicle])):
                    candidate = _clone_solution(solution)
                    candidate[first_vehicle][first_idx], candidate[second_vehicle][second_idx] = (
                        candidate[second_vehicle][second_idx],
                        candidate[first_vehicle][first_idx],
                    )
                    neighbors.append(candidate)

    return neighbors


def get_reorder_neighbors(solution):
    neighbors = []

    for vehicle_idx, rides in enumerate(solution):
        ride_count = len(rides)
        if ride_count < 2:
            continue

        # Reorder por trocas de pares dentro do mesmo veiculo.
        for i in range(ride_count):
            for j in range(i + 1, ride_count):
                candidate = _clone_solution(solution)
                candidate[vehicle_idx][i], candidate[vehicle_idx][j] = (
                    candidate[vehicle_idx][j],
                    candidate[vehicle_idx][i],
                )
                neighbors.append(candidate)

    return neighbors