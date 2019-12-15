# https://adventofcode.com/2019/day/15
import copy


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

    def run(self, input_v):
        while self.i < len(self.program) and self.program[self.i] != 99:
            opcode = self.program[self.i] % 100
            param1 = self.param(1)
            param2 = self.param(2)
            param3 = self.param(3)
            if opcode == 1:
                self.program[param3] = self.program[param1] + self.program[param2]
                self.i += 4
            elif opcode == 2:
                self.program[param3] = self.program[param1] * self.program[param2]
                self.i += 4
            elif opcode == 3:
                self.program[param1] = input_v
                self.i += 2
            elif opcode == 4:
                self.i += 2
                return self.program[param1]
            elif opcode == 5:
                if self.program[param1] != 0:
                    self.i = self.program[param2]
                else:
                    self.i += 3
            elif opcode == 6:
                if self.program[param1] == 0:
                    self.i = self.program[param2]
                else:
                    self.i += 3
            elif opcode == 7:
                if self.program[param1] < self.program[param2]:
                    self.program[param3] = 1
                else:
                    self.program[param3] = 0
                self.i += 4
            elif opcode == 8:
                if self.program[param1] == self.program[param2]:
                    self.program[param3] = 1
                else:
                    self.program[param3] = 0
                self.i += 4
            elif opcode == 9:
                self.relative_base += self.program[param1]
                self.i += 2
        self.has_halted = True
        return


def disp_map(tiles, robot_x, robot_y):
    min_x, max_x, min_y, max_y = 0, 0, 0, 0
    for key in tiles:
        min_x = min(min_x, key[0])
        max_x = max(max_x, key[0])
        min_y = min(min_y, key[1])
        max_y = max(max_y, key[1])
    disp = ""
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if x == robot_x and y == robot_y:
                disp += "D"
            elif x == 0 and y == 0:
                disp += "C"
            elif (x, y) in tiles:
                disp += tiles[(x, y)]
            else:
                disp += " "
        disp += "\n"
    return disp


def explore(program):
    tiles = {}
    directions = []
    x, y = 0, 0
    tiles[(x, y)] = "."
    objective = None
    went_reverse = False
    objective_dist = 0
    while objective is None or len(directions) > 0:
        direction = 0
        next_tile = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        for i in range(4):
            if next_tile[i] not in tiles:
                direction = i + 1
                went_reverse = False
                break
        if direction == 0:
            direction = directions[-1]
            if direction == 1:
                direction = 2
            elif direction == 2:
                direction = 1
            elif direction == 3:
                direction = 4
            elif direction == 4:
                direction = 3
            directions = directions[:-1]
            went_reverse = True
        out_v = program.run(direction)
        if out_v == 0:
            tiles[next_tile[direction - 1]] = "#"
        elif out_v == 1:
            tiles[next_tile[direction - 1]] = "."
            x = next_tile[direction - 1][0]
            y = next_tile[direction - 1][1]
            if not went_reverse:
                directions.append(direction)
        elif out_v == 2:
            objective = (x, y)
            tiles[next_tile[direction - 1]] = "O"
            x = next_tile[direction - 1][0]
            y = next_tile[direction - 1][1]
            if not went_reverse:
                directions.append(direction)
            objective_dist = len(directions)
    return tiles, objective_dist


def puzzle1(intcodes):
    p = Program(intcodes)
    return explore(p)[1]


def puzzle2(intcodes):
    p = Program(intcodes)
    tiles = explore(p)[0]
    min_x, max_x, min_y, max_y = 0, 0, 0, 0
    for key in tiles:
        min_x = min(min_x, key[0])
        max_x = max(max_x, key[0])
        min_y = min(min_y, key[1])
        max_y = max(max_y, key[1])
    minutes = -1
    empty_tiles = -1
    while empty_tiles != 0:
        empty_tiles = 0
        new_tiles = {}
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, y) in tiles:
                    if tiles[(x, y)] == ".":
                        empty_tiles += 1
                    if tiles[(x, y)] == "O" or (
                        tiles[(x, y)] == "."
                        and (
                            tiles[(x - 1, y)] == "0"
                            or tiles[(x + 1, y)] == "0"
                            or tiles[(x, y - 1)] == "0"
                            or tiles[(x, y + 1)] == "0"
                        )
                    ):
                        new_tiles[(x, y)] = "0"
                    else:
                        new_tiles[(x, y)] = tiles[(x, y)]
        minutes += 1
        tiles = copy.deepcopy(new_tiles)
    return minutes - 1


if __name__ == "__main__":
    with open("res/day15.txt") as input_f:
        original_intcodes = [int(x) for x in input_f.read().split(",")]
        print(puzzle1(original_intcodes[:]))
        print(puzzle2(original_intcodes[:]))
