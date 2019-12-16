# https://adventofcode.com/2019/day/16


def puzzle1(numbers):
    pattern = [0, 1, 0, -1]
    phase = 0
    while phase < 100:
        new_numbers = []
        for i in range(len(numbers)):
            sum = 0
            for j in range(len(numbers)):
                sum += numbers[j] * pattern[((j + 1) // (i + 1)) % 4]
            new_numbers.append(abs(sum) % 10)
        phase += 1
        numbers = new_numbers[:]
    return "".join([str(x) for x in numbers[:8]])


def puzzle2(numbers):
    pass


if __name__ == "__main__":
    with open("res/day16.txt") as input_f:
        numbers = [int(x) for x in input_f.read()]
        print(puzzle1(numbers[:]))
        print(puzzle2(numbers[:]))
