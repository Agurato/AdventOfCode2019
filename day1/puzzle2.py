# https://adventofcode.com/2019/day/1#part2


def calculate_fuel(mass):
    fuel_mass = mass // 3 - 2
    if fuel_mass <= 0:
        return 0
    return fuel_mass + calculate_fuel(fuel_mass)


if __name__ == '__main__':
    with open("input.txt", "r") as input_f:
        fuel_sum = 0
        for line in input_f:
            fuel_sum += calculate_fuel(int(line))
        print("Total fuel sum (part 2) :")
        print(fuel_sum)