class Ride:
    def __init__(self, start_row, start_column, end_row, end_column, earliest_start, latest_finish, ride_id=None):
        self.id = ride_id
        self.start_row = start_row
        self.start_column = start_column
        self.end_row = end_row
        self.end_column = end_column
        self.earliest_start = earliest_start
        self.latest_finish = latest_finish
        self.distance = abs(end_row - start_row) + abs(end_column - start_column)

    def __str__(self):
        ride_id = "?" if self.id is None else self.id
        return f"Ride {ride_id}: ({self.start_row},{self.start_column}) -> ({self.end_row},{self.end_column}), earliest start {self.earliest_start}, latest finish {self.latest_finish}, distance {self.distance}"
    
    def __repr__(self):
        if self.id is None:
            return "Ride(?)"
        return f"Ride({self.id})"

class Problem:
    def __init__(self, rows, columns, vehicles, rides, bonus, steps):
        self.grid_rows = rows
        self.grid_columns = columns
        self.vehicles = vehicles
        self.rides = rides
        self.bonus = bonus
        self.steps = steps

    def __str__(self):
        return f"Grid is ({self.grid_rows},{self.grid_columns}), there are {self.vehicles} vehicles in total, {self.rides} rides, the per-ride bonus is {self.bonus} and the number of steps in the simulation are {self.steps}"
    
class Vehicle:
    def __init__(self, id, row=0, column=0, time=0):
        self.id = id
        self.row = row
        self.column = column
        self.time = time
        self.rides = []

    def __str__(self):
        return f"Vehicle {self.id} is in position {self.position} at time {self.time}, with scheduled rides {self.rides}"
    