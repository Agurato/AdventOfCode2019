# https://adventofcode.com/2019/day/19


class Program:
    def __init__(self, program):
        self.i = 0
        self.program = program + [0] * 10000
        self.original_program = self.program[:]
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

    def reset(self):
        self.i = 0
        self.has_halted = False
        self.relative_base = 0
        self.program = self.original_program[:]


def get_bounds(intcodes):
    p = Program(intcodes[:])
    min_x, max_x, x = 0, 0, 0
    found_beam = False
    while max_x == 0:
        if p.run([x, 10000]) == 0:
            if found_beam:
                max_x = x - 1
        else:
            if not found_beam:
                min_x = x
            found_beam = True
        x += 1
        p.reset()
    return 10000 / (max_x + 1), 10000 / (min_x - 1)


def puzzle1(intcodes):
    beam = set()
    p = Program(intcodes[:])
    for y in range(50):
        beam_at_y = False
        for x in range(50):
            if p.run([x, y]) == 1:
                beam_at_y = True
                beam.add((x, y))
            elif beam_at_y:
                break
            p.reset()
    return len(beam)


def puzzle2(intcodes):
    p = Program(intcodes[:])
    lower_bound, higher_bound = get_bounds(intcodes)
    x_min = 100 * (lower_bound + 1) / (higher_bound - lower_bound)
    y_min = lower_bound * (x_min + 100)
    x_min = int(x_min)
    y_min = int(y_min)
    for x in range(x_min - 10, x_min + 2):
        for y in range(y_min - 15, y_min + 2):
            count_x, count_y = 0, 0
            for dy in range(100):
                count_y += p.run([x, y + dy])
                p.reset()
            if count_y != 100:
                break
            for dx in range(100):
                count_x += p.run([x + dx, y])
                p.reset()
            if count_x == 100 and count_y == 100:
                return x * 10000 + y


if __name__ == "__main__":
    with open("res/day19.txt") as input_f:
        original_intcodes = [int(x) for x in input_f.read().split(",")]
        print(puzzle1(original_intcodes[:]))
        print(puzzle2(original_intcodes[:]))
