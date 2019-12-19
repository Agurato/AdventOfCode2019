# https://adventofcode.com/2019/day/18
import copy


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"({self.x}, {self.y})"


def get_map(input_f):
    lines = []
    curr_pos = Point(0, 0)
    keys = {}
    y = 0
    for line_f in input_f.readlines():
        line = []
        x = 0
        for character in line_f.replace("\n", ""):
            if character == "@":
                curr_pos.x = x
                curr_pos.y = y
            elif "a" <= character <= "z":
                keys[character] = Point(x, y)
            line.append(character)
            x += 1
        lines.append(line)
        y += 1
    return curr_pos, lines, keys


def get_visible_keys(curr_pos, keys_found, lines):
    distance = 0
    run = True
    visible_keys = {}
    
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if lines[y][x] == "@":
                lines[y][x] = "."
            elif "a" <= lines[y][x] <= "z" and lines[y][x] in keys_found:
                lines[y][x] = "."
    lines[curr_pos.y][curr_pos.x] = "@"
    
    while run:
        new_lines = [x[:] for x in lines]
        for y in range(len(lines)):
            for x in range(len(lines[0])):
                if lines[y][x] == "@" or (
                    lines[y][x] == "."
                    and (
                        lines[y][x - 1] == "@"
                        or lines[y][x + 1] == "@"
                        or lines[y - 1][x] == "@"
                        or lines[y + 1][x] == "@"
                    )
                ):
                    new_lines[y][x] = "@"
                elif "a" <= lines[y][x] <= "z" and (
                        lines[y][x - 1] == "@"
                        or lines[y][x + 1] == "@"
                        or lines[y - 1][x] == "@"
                        or lines[y + 1][x] == "@"
                    ) and lines[y][x] not in visible_keys:
                    visible_keys[lines[y][x]] = distance + 1
                elif "A" <= lines[y][x] <= "Z" and (
                        lines[y][x - 1] == "@"
                        or lines[y][x + 1] == "@"
                        or lines[y - 1][x] == "@"
                        or lines[y + 1][x] == "@"
                    ) and lines[y][x].lower() in keys_found:
                    new_lines[y][x] = "@"
                else:
                    new_lines[y][x] = lines[y][x]
        distance += 1
        if new_lines == lines:
            run = False
        lines = [x[:] for x in new_lines]
    return visible_keys

def find_shortest(curr_pos, keys_found, lines, keys):
    if len(keys_found) == len(keys):
        return 0
    visible_keys = get_visible_keys(curr_pos, keys_found, [x[:] for x in lines])
    dist_min = len(lines)*len(lines[0])
    for k in visible_keys:
        dist = visible_keys[k]+find_shortest(keys[k], keys_found+[k], [x[:] for x in lines], keys)
        print(curr_pos, keys_found, visible_keys, k, dist)
        dist_min = min(dist_min, dist)
    return dist_min


def puzzle1(curr_pos, lines, keys):
    keys_found = []
    return find_shortest(curr_pos, keys_found, lines, keys)

def puzzle2():
    pass

if __name__ == "__main__":
    with open("res/day18.txt") as input_f:
        curr_pos, lines, keys = get_map(input_f)
        print(puzzle1(curr_pos, lines, keys))
        print(puzzle2())
