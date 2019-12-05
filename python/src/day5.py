# https://adventofcode.com/2019/day/5


def param(program, index, param_nb):
    operation = "{:>05}".format(program[index])
    if operation[-(2 + param_nb)] == "0":
        return program[index + param_nb]
    else:
        return index + param_nb


def run_program(program, input_v):
    i = 0
    while i < len(program) and program[i] != 99:
        opcode = program[i] % 100
        param1 = param(program, i, 1)
        param2 = param(program, i, 2)
        param3 = param(program, i, 3)
        if opcode == 1:
            # Addition
            program[param3] = program[param1] + program[param2]
            i += 4
        elif opcode == 2:
            # Multiplication
            program[param3] = program[param1] * program[param2]
            i += 4
        elif opcode == 3:
            # Input
            program[param1] = input_v
            i += 2
        elif opcode == 4:
            # Output
            yield program[param1]
            i += 2
        elif opcode == 5:
            # Jump if true
            if program[param1] != 0:
                i = program[param2]
            else:
                i += 3
        elif opcode == 6:
            # Jump if false
            if program[param1] == 0:
                i = program[param2]
            else:
                i += 3
        elif opcode == 7:
            # Less than
            if program[param1] < program[param2]:
                program[param3] = 1
            else:
                program[param3] = 0
            i += 4
        elif opcode == 8:
            # Equals
            if program[param1] == program[param2]:
                program[param3] = 1
            else:
                program[param3] = 0
            i += 4
    return


def puzzle1(program):
    output = ""
    for out in run_program(program, 1):
        output = out
    print(output)


def puzzle2(program):
    output = ""
    for out in run_program(program, 5):
        output = out
    print(output)


if __name__ == "__main__":
    with open("res/day5.txt", "r") as input_f:
        original_program = [int(x) for x in input_f.read().split(",")]
        puzzle1(original_program[:])
        puzzle2(original_program[:])
