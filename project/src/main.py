from parser import parse_input
from greedy import greedy_solution
from genetic_algorithm import ga_solution
from output import write_output
from evaluator import evaluate_solution
from models import Vehicle


def format_solution(solution):
    lines = []

    for vehicle_id, rides in enumerate(solution):
        ride_ids = [ride.id for ride in rides]
        lines.append(f"Vehicle {vehicle_id}: {ride_ids}")

    return "\n".join(lines)


def solve_instance(input_path, output_path, algorithm):
    problem = parse_input(input_path)

    if algorithm == "greedy":
        solution = greedy_solution(problem)
    elif algorithm == "ga":
        solution = ga_solution(problem)
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    score = evaluate_solution(problem, solution)
    
    write_output(solution, output_path)

    print(f"Input: {input_path}")
    print(f"Algorithm: {algorithm}")
    print(f"Score: {score}")
    print(f"Output: {output_path}") 
    print(f"{algorithm.upper()} solution (ride ids per vehicle):")
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
        user_value = input("Escolhe o algoritmo: \n1) Greedy \n2)Genetic Algorithm")

        if user_value == "1":
            return "greedy"
        if user_value == "2":
            return "ga"

        print("Valor invalido. Escolhe 1 ou 2.")


def main():
    instance_number = ask_instance_number()
    algorithm = ask_algorithm()

    input_path = f"data/input_{instance_number}.txt"
    output_path = f"results/{algorithm}_output_{instance_number}.txt"

    solve_instance(input_path, output_path, algorithm)


if __name__ == "__main__":
    main()
