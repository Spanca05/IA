from models import Ride, Problem

def parse_input(file_path):
    with open(file_path, 'r') as file:
        data = file.readline()
        rows, columns, vehicles, number_of_rides, bonus, steps = map(int, data.split())
        rides = file.readlines()
        rides_list = []
        for ride in rides:
            row_start, column_start, row_end, column_end, earliest_start, latest_finish = map(int, ride.split())
            ride_obj = Ride(row_start, column_start, row_end, column_end, earliest_start, latest_finish)
            rides_list.append(ride_obj)

        if (number_of_rides != len(rides_list)):
            raise ValueError(f"{number_of_rides} were expected, instead received {len(rides_list)} rides.")

        return Problem(rows, columns, vehicles, rides_list, bonus, steps)
