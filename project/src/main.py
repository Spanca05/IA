from parser import parse_input
from greedy import greedy_solution
from output import write_output
from simulation import simulate_rides_for_vehicles
from models import Vehicle


def format_solution(solution):
    lines = []

    for vehicle_id, rides in enumerate(solution):
        ride_ids = [ride.id for ride in rides]
        lines.append(f"Vehicle {vehicle_id}: {ride_ids}")

    return "\n".join(lines)


def solve_instance(input_path, output_path, show_solution=True):
    problem = parse_input(input_path)
    solution = greedy_solution(problem)
    vehicles = [Vehicle(i) for i in range(problem.vehicles)]
    score = simulate_rides_for_vehicles(
        vehicles,
        solution,
        problem.bonus,
    )

    write_output(solution, output_path)

    print(f"Input: {input_path}")
    print(f"Score: {score}")
    print(f"Output: {output_path}")

    if show_solution:
        print("Greedy solution (ride ids per vehicle):")
        print(format_solution(solution))

    return score


def ask_instance_number():
    while True:
        user_value = input("Escolhe o numero da instancia (1-3): ").strip()

        if user_value in ("1", "2", "3"):
            return int(user_value)

        print("Valor invalido. Tem de ser um numero entre 1 e 3.")


def main():
    instance_number = ask_instance_number()

    input_path = f"data/input_{instance_number}.txt"
    output_path = f"results/greedy_output_{instance_number}.txt"

    solve_instance(input_path, output_path, show_solution=True)


main()
