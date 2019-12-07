# https://adventofcode.com/2019/day/7
import itertools


def param(program, index, param_nb):
    operation = "{:>05}".format(program[index])
    if operation[-(2 + param_nb)] == "0":
        return program[index + param_nb]
    else:
        return index + param_nb


def run_program(program, inputs):
    i = 0
    input_c = 0
    out_v = 0
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
            program[param1] = inputs[input_c]
            input_c += 1
            i += 2
        elif opcode == 4:
            # Output
            out_v = program[param1]
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
    return out_v


def puzzle1(program):
    max_out = 0
    for phases in itertools.permutations([0, 1, 2, 3, 4]):
        input_v = 0
        for p in phases:
            input_v = run_program(program[:], [p, input_v])
        max_out = max(max_out, input_v)
    return max_out


def puzzle2(program):
    pass


if __name__ == "__main__":
    with open("res/day7.txt") as input_f:
        original_program = [int(x) for x in input_f.read().split(",")]
        print(puzzle1(original_program[:]))
        print(puzzle2(original_program[:]))
