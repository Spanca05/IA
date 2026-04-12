def evaluate_solution(problem, solution):
    total_points = 0
    bonus = problem.bonus

    for rides in solution:
        row = 0
        column = 0
        time = 0

        for ride in rides:
            start_arrival = time + abs(ride.start_row - row) + abs(ride.start_column - column)
            start_time = max(start_arrival, ride.earliest_start)
            finish_time = start_time + ride.distance

            if finish_time <= ride.latest_finish:
                total_points += ride.distance
                if start_time == ride.earliest_start:
                    total_points += bonus

            row = ride.end_row
            column = ride.end_column
            time = finish_time

    return total_points
