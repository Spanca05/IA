def write_output(solution, file_path):
    with open(file_path, 'w') as file:
        for rides in solution:
            ride_ids = [str(ride.id) for ride in rides]
            line = f"{len(rides)}"

            if ride_ids:
                line += " " + " ".join(ride_ids)

            file.write(line + '\n')
