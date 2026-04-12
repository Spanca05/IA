from parser import parse_input
from solvers import solve_with_algorithm
from output import write_output


def format_solution(solution):
    lines = []

    for vehicle_id, rides in enumerate(solution):
        ride_ids = [ride.id for ride in rides]
        lines.append(f"Vehicle {vehicle_id}: {ride_ids}")

    return "\n".join(lines)


def solve_instance(input_path, output_path, algorithm_name, show_solution=True):
    problem = parse_input(input_path)
    
    solution, score, history = solve_with_algorithm(problem, algorithm_name)
    
    write_output(solution, output_path)

    print(f"Input: {input_path}")
    print(f"Algorithm: {algorithm_name}")
    print(f"Score: {score}")
    print(f"Output: {output_path}")

    if show_solution:
        print(f"{algorithm_name.capitalize()} solution (ride ids per vehicle):")
        print(format_solution(solution))

    return score


def ask_instance_number():
    while True:
        user_value = input("Escolhe o numero da instancia (1-7): ").strip()

        if user_value in ("1", "2", "3", "4", "5", "6", "7"):
            return int(user_value)

        print("Valor invalido. Tem de ser um numero entre 1 e 7.")

def ask_algorithm():
    while True:
        print("Algoritmos disponíveis:")
        print("1. Greedy algorithm")
        print("2. Hill-Climbing algorithm")
        print("3. Simulated Annealing algorithm")
        print("4. Genetic Algorithm")
        user_value = input("Escolha o número do algoritmo (1-4):").strip()

        if user_value in ("1", "2", "3", "4"):
            return int(user_value)
        
        print("Valor inválido. Tem de ser um numero entre 1 e 4.")


def main():
    instance_number = ask_instance_number()
    algorithm_number = ask_algorithm()

    switcher = {
        1: "greedy",
        2: "hill_climbing",
        3: "simulated_annealing",
        4: "genetic_algorithm",
    }

    algorithm_name = switcher.get(algorithm_number)

    input_path = f"data/input_{instance_number}.txt"
    output_path = f"results/{algorithm_name}_output_{instance_number}.txt"

    solve_instance(input_path, output_path, algorithm_name, show_solution=True)


if __name__ == "__main__":
    main()
