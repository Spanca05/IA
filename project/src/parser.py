from models import Ride, Problem

def parse_input(file_path):
    with open(file_path, 'r') as file:
        header = file.readline()
        header_parts = header.split()

        if len(header_parts) != 6:
            raise ValueError(
                f"Invalid header in {file_path}. Expected 6 integers (R C V N B T), got: '{header}'"
            )

        rows, columns, vehicles, number_of_rides, bonus, steps = map(int, header_parts)
        rides = file.readlines()
        rides_list = []

        ride_id = 0
        for line_index, ride in enumerate(rides, start=2):
            ride_line = ride.strip()
            if not ride_line:
                continue

            ride_parts = ride_line.split()
            if len(ride_parts) != 6:
                raise ValueError(
                    f"Invalid ride line {line_index} in {file_path}. Expected 6 integers, got: '{ride_line}'"
                )

            row_start, column_start, row_end, column_end, earliest_start, latest_finish = map(int, ride_parts)

            if earliest_start > latest_finish:
                raise ValueError(
                    f"Invalid ride window on line {line_index} in {file_path}: "
                    f"earliest_start ({earliest_start}) cannot be greater than latest_finish ({latest_finish})."
                )

            ride_obj = Ride(
                row_start,
                column_start,
                row_end,
                column_end,
                earliest_start,
                latest_finish,
                ride_id=ride_id,
            )
            rides_list.append(ride_obj)
            ride_id += 1

        if (number_of_rides != len(rides_list)):
            raise ValueError(f"{number_of_rides} were expected, instead received {len(rides_list)} rides.")

        return Problem(rows, columns, vehicles, rides_list, bonus, steps)