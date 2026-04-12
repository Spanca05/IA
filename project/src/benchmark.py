import argparse
import csv
import os
import random
import statistics
import time

from parser import parse_input
from solvers import solve_with_algorithm


INSTANCE_IDS = [1, 2, 3, 4, 5, 6, 7]
ALGORITHMS = ["greedy", "hill_climbing", "simulated_annealing", "genetic_algorithm"]

HC_PARAM_GRID = [
    {"start_strategy": "warm_start"},
    {"start_strategy": "cold_start"},
]

SA_PARAM_GRID = [
    {"start_strategy": "warm_start", "T0": 800, "alpha": 0.95, "max_iterations": 600, "max_no_improvement": 80},
    {"start_strategy": "cold_start", "T0": 800, "alpha": 0.95, "max_iterations": 600, "max_no_improvement": 80},
]

GA_PARAM_GRID = [
    {
        "population_size": 20,
        "generations": 60,
        "tournament_size": 3,
        "elite_count": 3,
        "mutation_rate": 0.30,
        "order_crossover_prob": 0.5,
    },
    {
        "population_size": 40,
        "generations": 100,
        "tournament_size": 4,
        "elite_count": 5,
        "mutation_rate": 0.40,
        "order_crossover_prob": 0.6,
    },
]


def _safe_stdev(values):
    if len(values) < 2:
        return 0.0
    return statistics.pstdev(values)


def _param_sets_for_algorithm(algorithm):
    if algorithm == "hill_climbing":
        return HC_PARAM_GRID
    if algorithm == "simulated_annealing":
        return SA_PARAM_GRID
    if algorithm == "genetic_algorithm":
        return GA_PARAM_GRID
    return [{}]


def _format_params(params):
    if not params:
        return "default"
    ordered = sorted(params.items(), key=lambda item: item[0])
    return ";".join(f"{key}={value}" for key, value in ordered)


def run_benchmark(runs_per_setup=10, seed=42):
    random.seed(seed)

    detailed_rows = []
    summary_rows = []

    for instance_id in INSTANCE_IDS:
        input_path = f"data/input_{instance_id}.txt"

        for algorithm in ALGORITHMS:
            for params in _param_sets_for_algorithm(algorithm):
                scores = []
                elapsed_ms_values = []

                for run_idx in range(runs_per_setup):
                    # Keep stochastic algorithms reproducible per run.
                    random.seed(seed + instance_id * 10000 + run_idx)

                    problem = parse_input(input_path)

                    start = time.perf_counter()
                    _solution, score, _history = solve_with_algorithm(problem, algorithm, params=params)
                    elapsed_ms = (time.perf_counter() - start) * 1000.0

                    scores.append(score)
                    elapsed_ms_values.append(elapsed_ms)

                    detailed_rows.append(
                        {
                            "instance": instance_id,
                            "algorithm": algorithm,
                            "params": _format_params(params),
                            "run": run_idx,
                            "score": score,
                            "time_ms": round(elapsed_ms, 3),
                        }
                    )

                summary_rows.append(
                    {
                        "instance": instance_id,
                        "algorithm": algorithm,
                        "params": _format_params(params),
                        "runs": runs_per_setup,
                        "avg_score": round(statistics.mean(scores), 3),
                        "std_score": round(_safe_stdev(scores), 3),
                        "best_score": max(scores),
                        "worst_score": min(scores),
                        "avg_time_ms": round(statistics.mean(elapsed_ms_values), 3),
                        "std_time_ms": round(_safe_stdev(elapsed_ms_values), 3),
                    }
                )

    return detailed_rows, summary_rows


def write_results(detailed_rows, summary_rows, output_dir="results"):
    os.makedirs(output_dir, exist_ok=True)

    detailed_csv = os.path.join(output_dir, "benchmark_detailed.csv")
    summary_csv = os.path.join(output_dir, "benchmark_summary.csv")
    summary_txt = os.path.join(output_dir, "benchmark_summary.txt")

    with open(detailed_csv, "w", newline="") as file:
        fieldnames = ["instance", "algorithm", "params", "run", "score", "time_ms"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(detailed_rows)

    with open(summary_csv, "w", newline="") as file:
        fieldnames = [
            "instance",
            "algorithm",
            "params",
            "runs",
            "avg_score",
            "std_score",
            "best_score",
            "worst_score",
            "avg_time_ms",
            "std_time_ms",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    with open(summary_txt, "w") as file:
        file.write("Benchmark Summary\n")
        file.write("=" * 80 + "\n")
        for row in summary_rows:
            file.write(
                f"instance={row['instance']} | algorithm={row['algorithm']} | params={row['params']} | "
                f"runs={row['runs']} | avg_score={row['avg_score']} | std_score={row['std_score']} | "
                f"best={row['best_score']} | worst={row['worst_score']} | "
                f"avg_time_ms={row['avg_time_ms']} | std_time_ms={row['std_time_ms']}\n"
            )

    return detailed_csv, summary_csv, summary_txt


def main():
    parser = argparse.ArgumentParser(description="Run benchmark comparisons across algorithms and parameterizations.")
    parser.add_argument("--runs", type=int, default=10, help="Number of runs per (instance, algorithm, params).")
    parser.add_argument("--seed", type=int, default=42, help="Base random seed for reproducibility.")
    args = parser.parse_args()

    if args.runs <= 0:
        raise ValueError("--runs must be > 0")

    print(f"Running benchmark with runs={args.runs}, seed={args.seed}...")
    detailed_rows, summary_rows = run_benchmark(runs_per_setup=args.runs, seed=args.seed)
    detailed_csv, summary_csv, summary_txt = write_results(detailed_rows, summary_rows)

    print("Done.")
    print(f"Detailed CSV: {detailed_csv}")
    print(f"Summary CSV: {summary_csv}")
    print(f"Summary TXT: {summary_txt}")


if __name__ == "__main__":
    main()
