# https://adventofcode.com/2019/day/2


def puzzle1(intcodes):
    for op in range(0, len(intcodes), 4):
        if intcodes[op] == 1:
            intcodes[intcodes[op + 3]] = (
                intcodes[intcodes[op + 1]] + intcodes[intcodes[op + 2]]
            )
        elif intcodes[op] == 2:
            intcodes[intcodes[op + 3]] = (
                intcodes[intcodes[op + 1]] * intcodes[intcodes[op + 2]]
            )
        elif intcodes[op] == 99:
            break
    return intcodes[0]


def puzzle2(original):
    for noun in range(100):
        for verb in range(100):
            intcodes = original[:]
            intcodes[1] = noun
            intcodes[2] = verb
            puzzle1(intcodes)
            if intcodes[0] == 19690720:
                return 100 * noun + verb
    return -1


if __name__ == "__main__":
    with open("input.txt", "r") as input_f:
        inputcodes = [int(i) for i in input_f.read().split(",")]
        inputcodes[1] = 12
        inputcodes[2] = 2
        print(puzzle1(inputcodes[:]))
        print(puzzle2(inputcodes))
