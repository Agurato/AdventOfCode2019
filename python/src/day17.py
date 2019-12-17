# https://adventofcode.com/2019/day/17


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


def puzzle1(intcodes):
    lines = get_map(intcodes)
    sum = 0
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if 0 < x < len(lines[y]) - 1 and 0 < y < len(lines) - 1:
                if (
                    lines[y][x] == "#"
                    and lines[y - 1][x] == "#"
                    and lines[y + 1][x] == "#"
                    and lines[y][x - 1] == "#"
                    and lines[y][x + 1] == "#"
                ):
                    sum += x * y
    return sum


def puzzle2(intcodes):
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
