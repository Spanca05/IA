from parser import parse_input
from solvers import solve_with_algorithm
from output import write_output
from simulated_annealing import DEFAULT_PARAMS
import time


def format_solution(solution):
    lines = []

    for vehicle_id, rides in enumerate(solution):
        ride_ids = [ride.id for ride in rides]
        lines.append(f"Vehicle {vehicle_id}: {ride_ids}")

    return "\n".join(lines)


def solve_instance(input_path, output_path, algorithm_name, params=None, show_solution=True):
    problem = parse_input(input_path)

    start_time = time.perf_counter()
    solution, score = solve_with_algorithm(problem, algorithm_name, params=params)
    end_time = time.perf_counter()

    write_output(solution, output_path)

    print(f"Input: {input_path}")
    print(f"Algorithm: {algorithm_name}")
    if params:
        print(f"Params: {params}")
    print(f"Score: {score}")
    print(f"Runtime: {end_time - start_time:.6f} seconds")
    print(f"Output: {output_path}")

    if show_solution:
        print(f"{algorithm_name.capitalize()} solution (ride ids per vehicle):")
        print(format_solution(solution))

    return score


def ask_instance_number():
    while True:
        user_value = input("Escolhe o numero da instancia (1-3): ").strip()

        if user_value in ("1", "2", "3"):
            return int(user_value)

        print("Valor invalido. Tem de ser um numero entre 1 e 3.")

def ask_algorithm():
    while True:
        print("Algoritmos disponíveis:")
        print("1. Greedy algorithm")
        print("2. Hill-Climbing algorithm")
        print("3. Simulated Annealing algorithm")
        user_value = input("Escolha o número do algoritmo (1-3):").strip()

        if user_value in ("1", "2", "3"):
            return int(user_value)
        
        print("Valor inválido. Tem de ser um numero entre 1 e 3.")


def ask_yes_no(prompt):
    while True:
        user_value = input(prompt).strip().lower()

        if user_value in ("s", "sim", "y", "yes"):
            return True

        if user_value in ("n", "nao", "não", "no"):
            return False

        print("Valor inválido. Responde com s/n.")


def ask_float_param(name, default_value, min_value=None, max_value=None, recommended_min=None, recommended_max=None):
    while True:
        raw_value = input(f"{name} [default={default_value}]: ").strip()
        if raw_value == "":
            value = float(default_value)
        else:
            try:
                value = float(raw_value)
            except ValueError:
                print("Valor inválido. Introduz um número.")
                continue

        if min_value is not None and value <= min_value:
            print(f"{name} tem de ser > {min_value}.")
            continue

        if max_value is not None and value >= max_value:
            print(f"{name} tem de ser < {max_value}.")
            continue

        if recommended_min is not None and value < recommended_min:
            print(f"Aviso: {name} abaixo do recomendado ({recommended_min} a {recommended_max}).")

        if recommended_max is not None and value > recommended_max:
            print(f"Aviso: {name} acima do recomendado ({recommended_min} a {recommended_max}).")

        return value


def ask_int_param(name, default_value, min_value=0, recommended_min=None, recommended_max=None):
    while True:
        raw_value = input(f"{name} [default={default_value}]: ").strip()
        if raw_value == "":
            value = int(default_value)
        else:
            try:
                value = int(raw_value)
            except ValueError:
                print("Valor inválido. Introduz um inteiro.")
                continue

        if value <= min_value:
            print(f"{name} tem de ser > {min_value}.")
            continue

        if recommended_min is not None and value < recommended_min:
            print(f"Aviso: {name} abaixo do recomendado ({recommended_min} a {recommended_max}).")

        if recommended_max is not None and value > recommended_max:
            print(f"Aviso: {name} acima do recomendado ({recommended_min} a {recommended_max}).")

        return value


def ask_simulated_annealing_params():
    print("\nParâmetros do Simulated Annealing")
    print("Carrega Enter para usar o default de cada parâmetro.")

    return {
        "T0": ask_float_param(
            name="T0",
            default_value=DEFAULT_PARAMS["T0"],
            min_value=0,
            recommended_min=10,
            recommended_max=10000,
        ),
        "alpha": ask_float_param(
            name="alpha",
            default_value=DEFAULT_PARAMS["alpha"],
            min_value=0,
            max_value=1,
            recommended_min=0.8,
            recommended_max=0.999,
        ),
        "Tmin": ask_float_param(
            name="Tmin",
            default_value=DEFAULT_PARAMS["Tmin"],
            min_value=0,
            recommended_min=1e-9,
            recommended_max=1e-2,
        ),
        "max_iterations": ask_int_param(
            name="max_iterations",
            default_value=DEFAULT_PARAMS["max_iterations"],
            min_value=0,
            recommended_min=100,
            recommended_max=100000,
        ),
        "max_no_improvement": ask_int_param(
            name="max_no_improvement",
            default_value=DEFAULT_PARAMS["max_no_improvement"],
            min_value=0,
            recommended_min=10,
            recommended_max=10000,
        ),
    }


def main():
    instance_number = ask_instance_number()
    algorithm_number = ask_algorithm()

    switcher = {
        1: "greedy",
        2: "hill_climbing",
        3: "simulated_annealing"
    }

    algorithm_name = switcher.get(algorithm_number)
    params = None

    if algorithm_name == "simulated_annealing":
        use_custom_params = ask_yes_no("Queres configurar parâmetros do Simulated Annealing? (s/n): ")
        if use_custom_params:
            params = ask_simulated_annealing_params()

    input_path = f"data/input_{instance_number}.txt"
    output_path = f"results/{algorithm_name}_output_{instance_number}.txt"

    solve_instance(input_path, output_path, algorithm_name, params=params, show_solution=True)


main()
