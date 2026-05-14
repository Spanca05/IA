from models import Ride, Vehicle

def gets_bonus(start_time, earliest_start):
    return start_time == earliest_start
    
def receives_points(finish_time, latest_finish):
    return finish_time <= latest_finish

def ride_simulation(vehicle, ride, bonus):
    points = 0
    previous_time = vehicle.time

    start_arrival = vehicle.time + abs(ride.start_row - vehicle.row) + abs(ride.start_column - vehicle.column)
    start_time = max(start_arrival, ride.earliest_start)
    finish_time = start_time + ride.distance

    if receives_points(finish_time, ride.latest_finish):
        points += ride.distance
        
        if gets_bonus(start_time, ride.earliest_start):
            points += bonus

    vehicle.row = ride.end_row
    vehicle.column = ride.end_column
    vehicle.time = finish_time

    cost = finish_time - previous_time

    return (points, cost)


def simulate_rides_for_vehicle(vehicle, rides, bonus):
    points = 0

    temp_vehicle = Vehicle(vehicle.id, vehicle.row, vehicle.column, vehicle.time)

    for ride in rides:
        ride_points, _ = ride_simulation(temp_vehicle, ride, bonus)
        points += ride_points

    return points

def simulate_rides_for_vehicles(vehicles, solution, bonus):
    points = 0

    for (vehicle, rides) in zip(vehicles, solution):
        points += simulate_rides_for_vehicle(vehicle, rides, bonus)

    return points