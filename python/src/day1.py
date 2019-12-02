# https://adventofcode.com/2019/day/1


def puzzle1(input_f):
    fuel_sum = 0
    for line in input_f:
        fuel_sum += int(line) // 3 - 2
    return fuel_sum


def puzzle2(input_f):
    def calculate_fuel(mass):
        fuel_mass = mass // 3 - 2
        if fuel_mass <= 0:
            return 0
        return fuel_mass + calculate_fuel(fuel_mass)

    fuel_sum = 0
    for line in input_f:
        fuel_sum += calculate_fuel(int(line))

    return fuel_sum


if __name__ == "__main__":
    with open("res/day1.txt", "r") as input_f:
        print(puzzle1(input_f))
        input_f.seek(0)
        print(puzzle2(input_f))
