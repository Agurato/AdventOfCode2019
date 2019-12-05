# https://adventofcode.com/2019/day/5


def get_param_value(program, index, param_nb):
    operation = "{:>04}".format(program[index])
    if operation[-(2 + param_nb)] == "0":
        return program[program[index + param_nb]]
    else:
        return program[index + param_nb]


def run_program(program, input_v):
    i = 0
    while i < len(program):
        operation = "{:>04}".format(program[i])
        opcode = operation[-2:]
        if opcode == "01":
            # Addition
            program[program[i + 3]] = get_param_value(program, i, 1) + get_param_value(
                program, i, 2
            )
            i += 4
        elif opcode == "02":
            # Multiplication
            program[program[i + 3]] = get_param_value(program, i, 1) * get_param_value(
                program, i, 2
            )
            i += 4
        elif opcode == "03":
            # Input
            program[program[i + 1]] = input_v
            i += 2
        elif opcode == "04":
            # Output
            yield program[program[i + 1]]
            i += 2
        elif opcode == "05":
            # Jump if true
            if get_param_value(program, i, 1) != 0:
                i = get_param_value(program, i, 2)
            else:
                i += 3
        elif opcode == "06":
            # Jump if false
            if get_param_value(program, i, 1) == 0:
                i = get_param_value(program, i, 2)
            else:
                i += 3
        elif opcode == "07":
            # Less than
            if get_param_value(program, i, 1) < get_param_value(program, i, 2):
                program[program[i + 3]] = 1
            else:
                program[program[i + 3]] = 0
            i += 4
        elif opcode == "08":
            # Equals
            if get_param_value(program, i, 1) == get_param_value(program, i, 2):
                program[program[i + 3]] = 1
            else:
                program[program[i + 3]] = 0
            i += 4
        elif opcode == "99":
            # Halt
            break
    return


def puzzle1(program):
    output = ""
    for out in run_program(program, 1):
        output = out
    print(output)


def puzzle2(program):
    output = ""
    for out in run_program(program, 0):
        output = out
    print(output)


if __name__ == "__main__":
    with open("res/day5.txt", "r") as input_f:
        original_program = [int(x) for x in input_f.read().split(",")]
        puzzle1(original_program[:])
        puzzle2(original_program[:])
