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


def sublist_indexes(sublist, full_list):
    if len(sublist) > len(full_list):
        return []
    indexes = []
    for i in range(len(full_list) - len(sublist) + 1):
        is_sublist = True
        for j in range(len(sublist)):
            if sublist[j] != full_list[i + j]:
                is_sublist = False
                break
        if is_sublist:
            indexes.append(i)
    return indexes


def separate_moves(total_moves):
    move_functions = []
    abc = ["A", "B", "C"]

    for abc_pos in range(3):
        start = 0
        for i in range(start, len(total_moves)):
            if len(total_moves[i]) != 1:
                break
            start = i + 1
        curr_move = []
        curr_pos = []
        for length in range(1, 6):
            short_move = total_moves[start : start + length]
            cancel = False
            for move in short_move:
                if len(move) == 1:
                    cancel = True
                    break
            if cancel:
                break
            indexes = sublist_indexes(short_move, total_moves)
            if len(indexes) == 1 or sum([len(x) for x in short_move]) > 11:
                break
            curr_pos = indexes[:]
            curr_move = short_move[:]
        for pos in reversed(curr_pos):
            del total_moves[pos : pos + len(curr_move)]
            total_moves.insert(pos, abc[abc_pos])
        move_functions.append(curr_move)

    input_data = [ord(x) for x in ",".join(total_moves) + "\n"]

    for move_func in move_functions:
        for i in range(len(move_func)):
            move_func[i] = move_func[i][0] + "," + move_func[i][1:]
        input_data += [ord(x) for x in ",".join(move_func) + "\n"]
    return input_data + [ord(x) for x in "n\n"]


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
    total_moves = [
        total_moves[i] + total_moves[i + 1] for i in range(0, len(total_moves), 2)
    ]
    input_data = separate_moves(total_moves)

    intcodes[0] = 2
    p = Program(intcodes)
    disp = ""
    out_v = 0
    for output in p.run(input_data):
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
