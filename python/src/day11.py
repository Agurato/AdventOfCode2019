# https://adventofcode.com/2019/day/11
from enum import Enum


class Painter:
    def __init__(self, program_l):
        self.x = 0
        self.y = 0
        self.dir = 0
        self.program = Program(program_l)

    def step(self, turn_dir):
        if turn_dir == 0:
            # Go left
            self.dir = (self.dir - 1) % 4
        else:
            # Go right
            self.dir = (self.dir + 1) % 4
        if self.dir == 0:
            self.y += 1
        elif self.dir == 1:
            self.x += 1
        elif self.dir == 2:
            self.y -= 1
        else:
            self.x -= 1


class Program:
    def __init__(self, program):
        self.i = 0
        self.program = program
        self.relative_base = 0
        self.has_halted = False

    def param(self, param_nb):
        operation = "{:>05}".format(self.program[self.i])
        param_mode = operation[-(2 + param_nb)]
        if param_mode == "0":
            if self.i + param_nb >= len(self.program):
                return 0
            return self.program[self.i + param_nb]
        elif param_mode == "1":
            return self.i + param_nb
        elif param_mode == "2":
            if self.i + param_nb >= len(self.program):
                return 0
            return self.program[self.i + param_nb] + self.relative_base

    def extend_program(self, param1, param2, param3):
        if max(param1, param2, param3) > len(self.program):
            self.program += [0] * (max(param1, param2, param3) - len(self.program))

    def run(self, inputs):
        input_c = 0
        outputs = []
        while self.i < len(self.program) and self.program[self.i] != 99:
            opcode = self.program[self.i] % 100
            param1 = self.param(1)
            param2 = self.param(2)
            param3 = self.param(3)
            self.extend_program(param1, param2, param3)
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
                outputs.append(self.program[param1])
                if len(outputs) == 2:
                    return outputs
                self.i += 2
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
            elif opcode == 9:
                self.relative_base += self.program[param1]
                self.i += 2
        self.has_halted = True
        return outputs


def puzzle1(program_l):
    painter = Painter(program_l)
    panels = {}
    while not painter.program.has_halted:
        color = 0
        if (painter.x, painter.y) in panels:
            color = panels[(painter.x, painter.y)]
        outputs = painter.program.run([color])
        panels[(painter.x, painter.y)] = outputs[0]
        painter.step(outputs[1])

    return len(panels)


def puzzle2(program_l):
    pass


if __name__ == "__main__":
    with open("res/day11.txt") as input_f:
        original_program = [int(x) for x in input_f.read().split(",")]
        print(puzzle1(original_program[:]))
        # print(puzzle2(original_program[:]))
