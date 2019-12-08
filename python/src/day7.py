# https://adventofcode.com/2019/day/7
import itertools


class Program:
    def __init__(self, program, phase):
        self.i = 0
        self.program = program
        self.phase = phase
        self.last_out = 0
        self.has_halted = False

    def run(self, inputs):
        input_c = 0
        while self.i < len(self.program) and self.program[self.i] != 99:
            opcode = self.program[self.i] % 100
            param1 = param(self.program, self.i, 1)
            param2 = param(self.program, self.i, 2)
            param3 = param(self.program, self.i, 3)
            if opcode == 1:
                # Addition
                self.program[param3] = self.program[param1] + self.program[param2]
                self.i += 4
            elif opcode == 2:
                # Multiplication
                self.program[param3] = self.program[param1] * self.program[param2]
                self.i += 4
            elif opcode == 3:
                # Input
                self.program[param1] = inputs[input_c]
                input_c += 1
                self.i += 2
            elif opcode == 4:
                # Output
                self.last_out = self.program[param1]
                self.i += 2
                return self.last_out
            elif opcode == 5:
                # Jump if true
                if self.program[param1] != 0:
                    self.i = self.program[param2]
                else:
                    self.i += 3
            elif opcode == 6:
                # Jump if false
                if self.program[param1] == 0:
                    self.i = self.program[param2]
                else:
                    self.i += 3
            elif opcode == 7:
                # Less than
                if self.program[param1] < self.program[param2]:
                    self.program[param3] = 1
                else:
                    self.program[param3] = 0
                self.i += 4
            elif opcode == 8:
                # Equals
                if self.program[param1] == self.program[param2]:
                    self.program[param3] = 1
                else:
                    self.program[param3] = 0
                self.i += 4
        self.has_halted = True
        return self.last_out


def param(program, index, param_nb):
    operation = "{:>05}".format(program[index])
    if operation[-(2 + param_nb)] == "0":
        if index + param_nb >= len(program):
            return 0
        return program[index + param_nb]
    else:
        return index + param_nb


def puzzle1(program):
    max_out = 0
    for phases in itertools.permutations([0, 1, 2, 3, 4]):
        programs = [Program(program[:], phases[i]) for i in range(5)]
        input_v = 0
        for p in programs:
            input_v = p.run([p.phase, input_v])
        max_out = max(max_out, input_v)
    return max_out


def puzzle2(program):
    max_out = 0
    for phases in itertools.permutations([5, 6, 7, 8, 9]):
        programs = [Program(program[:], phases[i]) for i in range(5)]
        input_v = 0
        for p in programs:
            input_v = p.run([p.phase, input_v])
        curr_program = 0
        while not programs[4].has_halted:
            input_v = programs[curr_program % 5].run([input_v])
            curr_program += 1
        max_out = max(max_out, input_v)
    return max_out


if __name__ == "__main__":
    with open("res/day7.txt") as input_f:
        original_program = [int(x) for x in input_f.read().split(",")]
        # print(puzzle1(original_program[:]))
        print(puzzle2(original_program[:]))
