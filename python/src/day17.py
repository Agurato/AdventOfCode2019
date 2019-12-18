# https://adventofcode.com/2019/day/17


class Robot:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir


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
                self.program[param1] = inputs[input_c]
                input_c += 1
                self.i += 2
            elif opcode == 4:
                self.i += 2
                yield self.program[param1]
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


def get_map(intcodes):
    p = Program(intcodes)
    disp = ""
    lines = []
    line = []
    for output in p.run(None):
        character = chr(output)
        disp += character
        if character == "\n":
            lines.append(line)
            line = []
        else:
            line.append(chr(output))
    print(disp)
    return lines[:-1]


def is_intersection(lines, x, y):
    total = 0
    if lines[y][x] == "#":
        if y > 0 and lines[y - 1][x] == "#":
            total += 1
        if y < len(lines) - 1 and lines[y + 1][x] == "#":
            total += 1
        if x > 0 and lines[y][x - 1] == "#":
            total += 1
        if x < len(lines[y]) - 1 and lines[y][x + 1] == "#":
            total += 1
    return total > 2


def get_direction(lines, robot):
    if robot.dir == "<" and robot.x > 0 and lines[robot.y][robot.x - 1] == "#":
        if not is_intersection(lines, robot.x, robot.y):
            lines[robot.y][robot.x] = "."
        robot.x = robot.x - 1
        return "F"
    elif (
        robot.dir == ">"
        and robot.x < len(lines[robot.y]) - 1
        and lines[robot.y][robot.x + 1] == "#"
    ):
        if not is_intersection(lines, robot.x, robot.y):
            lines[robot.y][robot.x] = "."
        robot.x = robot.x + 1
        return "F"
    elif robot.dir == "^" and robot.y > 0 and lines[robot.y - 1][robot.x] == "#":
        if not is_intersection(lines, robot.x, robot.y):
            lines[robot.y][robot.x] = "."
        robot.y = robot.y - 1
        return "F"
    elif (
        robot.dir == "v"
        and robot.y < len(lines) - 1
        and lines[robot.y + 1][robot.x] == "#"
    ):
        if not is_intersection(lines, robot.x, robot.y):
            lines[robot.y][robot.x] = "."
        robot.y = robot.y + 1
        return "F"

    new_dir = robot.dir
    if robot.x > 0 and lines[robot.y][robot.x - 1] == "#":
        new_dir = "<"
        robot.x = robot.x - 1
    elif robot.x < len(lines[robot.y]) - 1 and lines[robot.y][robot.x + 1] == "#":
        new_dir = ">"
        robot.x = robot.x + 1
    elif robot.y > 0 and lines[robot.y - 1][robot.x] == "#":
        new_dir = "^"
        robot.y = robot.y - 1
    elif robot.y < len(lines) - 1 and lines[robot.y + 1][robot.x] == "#":
        new_dir = "v"
        robot.y = robot.y + 1
    else:
        return None

    result = ""

    if robot.dir == "^":
        if new_dir == ">":
            result = "R"
        elif new_dir == "<":
            result = "L"
    elif robot.dir == ">":
        if new_dir == "v":
            result = "R"
        elif new_dir == "^":
            result = "L"
    elif robot.dir == "v":
        if new_dir == ">":
            result = "L"
        elif new_dir == "<":
            result = "R"
    elif robot.dir == "<":
        if new_dir == "v":
            result = "L"
        elif new_dir == "^":
            result = "R"

    robot.dir = new_dir
    return result


def separate_moves(total_moves):
    for length in range(len(total_moves)//6):




def puzzle1(intcodes):
    lines = get_map(intcodes)
    sum = 0
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if 0 < x < len(lines[y]) - 1 and 0 < y < len(lines) - 1:
                if is_intersection(lines, x, y):
                    sum += x * y
    return sum


def puzzle2(intcodes):
    lines = get_map(intcodes)
    robot = Robot(0, 0, "^")
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            tile = lines[y][x]
            if tile == "^" or tile == "v" or tile == "<" or tile == ">":
                robot.x = x
                robot.y = y
                robot.dir = tile
    total_moves = []
    forward = 0
    run = True
    while run:
        direction = get_direction(lines, robot)
        if direction is None:
            run = False
        else:
            if direction == "F":
                forward += 1
            else:

                if forward > 0:
                    total_moves.append(str(forward + 1))
                total_moves.append(direction)
                forward = 0
    total_moves.append(str(forward + 1))
    print(total_moves)
    separate_moves(total_moves)

    intcodes[0] = 2
    main_movement = [ord(x) for x in "A,A,B,C,B,C,B,C,C,A\n"]
    A_movement = [ord(x) for x in "R,8,L,4,R,4,R,10,R,8\n"]
    B_movement = [ord(x) for x in "L,12,L,12,R,8,R,8\n"]
    C_movement = [ord(x) for x in "R,10,R,4,R,4\n"]
    video = [ord(x) for x in "n\n"]
    p = Program(intcodes)
    disp = ""
    out_v = 0
    for output in p.run(main_movement + A_movement + B_movement + C_movement + video):
        character = chr(output)
        out_v = output
        if character == "\n":
            disp = ""
        else:
            disp += character
    return out_v


if __name__ == "__main__":
    with open("res/day17.txt") as input_f:
        original_intcodes = [int(x) for x in input_f.read().split(",")]
        print(puzzle1(original_intcodes[:]))
        print(puzzle2(original_intcodes[:]))
