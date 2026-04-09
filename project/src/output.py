import os


def write_output(solution, file_path):
    output_dir = os.path.dirname(file_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(file_path, 'w') as file:
        for rides in solution:
            ride_ids = [str(ride.id) for ride in rides]
            line = f"{len(rides)}"

            if ride_ids:
                line += " " + " ".join(ride_ids)

            file.write(line + '\n')