from dataclasses import dataclass, asdict
from pathlib import Path
import csv
import json
import time
import argparse

from parser import parse_input
from solvers import solve_with_algorithm
from output import write_output


@dataclass
class ExperimentResult:
	instance_path: str
	algorithm: str
	params: dict | None
	score: int
	runtime_seconds: float
	output_path: str | None = None


def run_experiment(input_path, algorithm_name, params=None, output_path=None, write_solution=True):
	problem = parse_input(input_path)

	start_time = time.perf_counter()
	solution, score = solve_with_algorithm(problem, algorithm_name, params=params)
	end_time = time.perf_counter()

	if write_solution and output_path is not None:
		write_output(solution, output_path)

	return ExperimentResult(
		instance_path=str(input_path),
		algorithm=algorithm_name,
		params=params,
		score=score,
		runtime_seconds=end_time - start_time,
		output_path=str(output_path) if output_path is not None else None,
	)


def run_experiments(input_paths, algorithm_names, params_by_algorithm=None, output_dir=None, write_solution=True):
	results = []
	output_dir_path = Path(output_dir) if output_dir is not None else None
	params_by_algorithm = params_by_algorithm or {}

	for input_path in input_paths:
		for algorithm_name in algorithm_names:
			params = params_by_algorithm.get(algorithm_name)
			output_path = None

			if output_dir_path is not None:
				output_dir_path.mkdir(parents=True, exist_ok=True)
				instance_name = Path(input_path).stem
				output_path = output_dir_path / f"{instance_name}_{algorithm_name}.txt"

			result = run_experiment(
				input_path=input_path,
				algorithm_name=algorithm_name,
				params=params,
				output_path=output_path,
				write_solution=write_solution,
			)
			results.append(result)

	return results


def write_experiment_results(results, csv_path):
	fieldnames = ["instance_path", "algorithm", "params", "score", "runtime_seconds", "output_path"]

	with open(csv_path, "w", newline="") as file:
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()

		for result in results:
			row = asdict(result)
			row["params"] = json.dumps(row["params"], ensure_ascii=False) if row["params"] is not None else ""
			writer.writerow(row)


def print_results_summary(results):
	if not results:
		print("No experiment results to show.")
		return

	print("\nExperiment summary:")
	for result in results:
		print(
			f"- {Path(result.instance_path).name} | {result.algorithm} | "
			f"score={result.score} | runtime={result.runtime_seconds:.6f}s"
		)


def build_default_input_paths(base_dir):
	return [
		str(Path(base_dir) / "data" / "input_1.txt"),
		str(Path(base_dir) / "data" / "input_2.txt"),
		str(Path(base_dir) / "data" / "input_3.txt"),
	]


def main():
	parser = argparse.ArgumentParser(description="Run algorithm experiments and export CSV results.")
	parser.add_argument("--inputs", nargs="*", help="Input files. Default: data/input_1..3.txt")
	parser.add_argument(
		"--algorithms",
		nargs="+",
		default=["greedy", "hill_climbing", "simulated_annealing"],
		help="Algorithms to run",
	)
	parser.add_argument(
		"--output-dir",
		default="results",
		help="Directory for solution output files",
	)
	parser.add_argument(
		"--csv",
		default="results/experiment_results.csv",
		help="CSV file path to store benchmark results",
	)
	args = parser.parse_args()

	base_dir = Path(__file__).resolve().parent.parent
	input_paths = args.inputs if args.inputs else build_default_input_paths(base_dir)

	results = run_experiments(
		input_paths=input_paths,
		algorithm_names=args.algorithms,
		output_dir=args.output_dir,
		write_solution=True,
	)

	csv_path = Path(args.csv)
	csv_path.parent.mkdir(parents=True, exist_ok=True)
	write_experiment_results(results, csv_path)
	print_results_summary(results)
	print(f"\nCSV written to: {csv_path}")


if __name__ == "__main__":
	main()

