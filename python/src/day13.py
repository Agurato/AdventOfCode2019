# https://adventofcode.com/2019/day/13
from enum import Enum


class Tile(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


class Program:
    def __init__(self, program):
        self.i = 0
        self.program = program + [0] * 10000
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

    def run(self, inputs):
        input_c = 0
        outputs = []
        while self.i < len(self.program) and self.program[self.i] != 99:
            opcode = self.program[self.i] % 100
            param1 = self.param(1)
            param2 = self.param(2)
            param3 = self.param(3)
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
                self.i += 2
                if len(outputs) == 3:
                    return outputs
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


def get_pos(tiles, target):
    for pos in tiles:
        if tiles[pos] == target:
            return pos
    return None


def puzzle1(intcodes):
    p = Program(intcodes)
    tiles = {}
    while not p.has_halted:
        outputs = p.run([])
        if len(outputs) == 3:
            tiles[(outputs[0], outputs[1])] = Tile(outputs[2])
    return len(list(filter(lambda x: x == Tile.BLOCK, tiles.values())))


def puzzle2(intcodes):
    intcodes[0] = 2
    p = Program(intcodes)
    tiles = {}
    score = 0
    next_input = 0
    while not p.has_halted:
        outputs = p.run([next_input])
        if len(outputs) == 3:
            if outputs[0] == -1 and outputs[1] == 0:
                score = outputs[2]
            else:
                tiles[(outputs[0], outputs[1])] = Tile(outputs[2])
            paddle = get_pos(tiles, Tile.PADDLE)
            ball = get_pos(tiles, Tile.BALL)
            if paddle is not None and ball is not None:
                if paddle[0] < ball[0]:
                    next_input = 1
                elif paddle[0] > ball[0]:
                    next_input = -1
                else:
                    next_input = 0
    return score


if __name__ == "__main__":
    with open("res/day13.txt") as input_f:
        original_intcodes = [int(x) for x in input_f.read().split(",")]
        print(puzzle1(original_intcodes[:]))
        print(puzzle2(original_intcodes[:]))
