from models import Ride, Vehicle

def gets_bonus(start_time, earliest_start):
    if start_time == earliest_start:
        return True
    return False
    
def receives_points(finish_time, latest_finish):
    if finish_time <= latest_finish:
        return True
    return False

def ride_simulation(vehicle, ride, bonus):
    points = 0

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

    return points


def simulate_rides_for_vehicle(vehicle, rides, bonus):
    points = 0

    temp_vehicle = Vehicle(vehicle.id, vehicle.row, vehicle.column, vehicle.time)

    for ride in rides:
        points += ride_simulation(temp_vehicle, ride, bonus)

    return points

def simulate_rides_for_vehicles(vehicles, solution, bonus):
    points = 0

    for (vehicle, rides) in zip(vehicles, solution):
        points += simulate_rides_for_vehicle(vehicle, rides, bonus)

    return points