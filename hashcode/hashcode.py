from math import floor

class City:
    def __init__(self, rows, columns, cars, rides, bonuses, steps):
        self.rows = int(rows)
        self.columns = int(columns)
        self.number_cars = int(cars)
        self.number_rides = int(rides)
        self.bonuses = int(bonuses)
        self.steps = int(steps)
        self.rides = []
        self.cars = []
        self.assigned = False

    def check_if_possible(self, ride):  # eliminate rides that cannot be taken from beginning at all
        approach_time = ride.starting_position[0] + ride.starting_position[1]
        ride_time = abs(ride.finishing_position[0] - ride.starting_position[0]) \
            + abs(ride.finishing_position[1] - ride.starting_position[1])

        if approach_time + ride_time <= ride.latest_time:
            ride.time = ride_time
            self.rides.append(ride)

    def start(self, rides):  # start everything: add rides(and check), sort them by starting time, add cars, update
        for i in range(0, len(rides)):
            line = rides[i].split(" ")
            self.check_if_possible(Ride(line[0], line[1], line[2], line[3], line[4], line[5], i))

        self.rides.sort(key=lambda x: x.starting_position[0] + x.starting_position[1])
        # self.rides.sort(key=lambda x: x.earliest_time)
        for car in range(self.number_cars):
            self.cars.append(Car())

        self.update()

    def update(self):
        self.pick_rides()
        if self.assigned:
            self.pick_rides()

    def pick_rides(self):
        self.assigned = False
        for ride in self.rides:
            for car in self.cars:
                # first, ride that will get bonus
                if ride.earliest_time - (self.steps / self.number_rides) * 50 \
                        <= car.approach_time(ride) + car.time <= ride.earliest_time:
                    car.give_ride(ride.finishing_position, ride.earliest_time + ride.time, ride.id)
                    self.rides.remove(ride)
                    car.moved = True
                    self.assigned = True
                    break
                # ride that will not get bonus by arriving too late but will be completed
                elif car.approach_time(ride) + car.time > ride.earliest_time \
                        and car.approach_time(ride) + car.time + ride.time < ride.latest_time  \
                        and len(car.finished_rides) < self.number_rides / self.number_cars:
                    car.give_ride(ride.finishing_position, car.approach_time(ride) + car.time + ride.time, ride.id)
                    self.rides.remove(ride)
                    car.moved = True
                    self.assigned = True
                    break
                car.change_spot(self.steps, self.rows, self.columns)


class Car:
    def __init__(self):
        self.position = [0, 0]
        self.time = 0
        self.finished_rides = []
        self.moved = False

    def give_ride(self, position, time, identifier):
        self.position = position
        self.time = time
        self.finished_rides.append(identifier)

    def approach_time(self, ride):
        return abs(self.position[0] - ride.starting_position[0]) + abs(self.position[1] - ride.starting_position[1])

    def change_spot(self, steps, rows, columns):
        if not self.moved:
            go_row = floor(steps / rows)
            go_column = floor(steps / columns)

            if self.position[0] + go_row < rows and self.position[1] + go_column < columns:
                self.position = [self.position[0] + go_row, self.position[1] + go_column]
                self.time += go_row + go_column
        self.moved = False



class Ride:
    def __init__(self, x1, y1, x2, y2, t1, t2, num):
        self.id = num
        self.starting_position = [int(x1), int(y1)]
        self.finishing_position = [int(x2), int(y2)]
        self.earliest_time = int(t1)
        self.latest_time = int(t2)
        self.time = abs(self.finishing_position[0] - self.starting_position[0]) \
            + abs(self.finishing_position[1] - self.starting_position[1])

    def __str__(self):
        return "Start: " + str(self.earliest_time)


def out(name):
    file = open(name, 'r').read().splitlines()
    fl = file[0].split(' ')
    town = City(fl[0], fl[1], fl[2], fl[3], fl[4], fl[5])
    town.start(file[1:])
    result = ''
    total = 0
    for car in town.cars:
        if len(car.finished_rides) > 0:
            total += len(car.finished_rides)
            ans = str(len(car.finished_rides)) + ' '
            for i in car.finished_rides:
                ans += str(i) + ' '
            ans += '\n'
            result += ans
        else:
            result += "0\n"
    result = result[:-1]
    text_file = open("Output_{}.txt".format(name), "w")
    text_file.write(result)
    text_file.close()
    print(n, " done")
    print('{}/{}'.format(total, town.number_rides))


names = ['a_example.in', 'b_should_be_easy.in', 'c_no_hurry.in', 'd_metropolis.in', 'e_high_bonus.in']
for n in names:
    out(n)

