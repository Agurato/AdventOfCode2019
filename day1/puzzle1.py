# https://adventofcode.com/2019/day/1

if __name__ == '__main__':
    with open("input.txt", "r") as input_f:
        fuel_sum = 0
        for line in input_f:
            fuel_sum += int(line) // 3 - 2
        print("Total fuel sum (part 1) :")
        print(fuel_sum)