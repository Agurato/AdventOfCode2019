# https://adventofcode.com/2019/day/16


def puzzle1(numbers):
    pattern = [0, 1, 0, -1]
    for phase in range(100):
        new_numbers = []
        for i in range(len(numbers)):
            sum = 0
            for j in range(i, len(numbers)):
                val = pattern[((j + 1) // (i + 1)) % 4]
                if val == 1:
                    sum += numbers[j]
                elif val == -1:
                    sum -= numbers[j]
            new_numbers.append(abs(sum) % 10)
        numbers = new_numbers
    return "".join(map(str, numbers[:8]))


def puzzle2(numbers):
    offset = int("".join(map(str, numbers[:7])))
    numbers = (numbers * 10000)[offset:]
    for phase in range(100):
        sum = 0
        for i in range(len(numbers) - 1, -1, -1):
            sum = (sum + numbers[i]) % 10
            numbers[i] = sum
    return "".join(map(str, numbers[:8]))


if __name__ == "__main__":
    with open("res/day16.txt") as input_f:
        numbers = [int(x) for x in input_f.read()]
        print(puzzle1(numbers[:]))
        print(puzzle2(numbers[:]))
