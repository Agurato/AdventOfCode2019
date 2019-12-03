# https://adventofcode.com/2019/day/3


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def get_wire(line):
    wire = [Point(0, 0)]
    count = 0
    for instruction in line.split(","):
        direction = instruction[0]
        if direction == "U":
            wire.append(Point(wire[count].x, wire[count].y + int(instruction[1:])))
        if direction == "D":
            wire.append(Point(wire[count].x, wire[count].y - int(instruction[1:])))
        if direction == "L":
            wire.append(Point(wire[count].x - int(instruction[1:]), wire[count].y))
        if direction == "R":
            wire.append(Point(wire[count].x + int(instruction[1:]), wire[count].y))
        count += 1
    return wire


def get_segment(line):
    prev_point = Point(0, 0)
    for instruction in line.split(","):
        direction = instruction[0]
        curr_point = Point(0, 0)
        if direction == "U":
            curr_point = Point(prev_point.x, prev_point.y + int(instruction[1:]))
        if direction == "D":
            curr_point = Point(prev_point.x, prev_point.y - int(instruction[1:]))
        if direction == "L":
            curr_point = Point(prev_point.x - int(instruction[1:]), prev_point.y)
        if direction == "R":
            curr_point = Point(prev_point.x + int(instruction[1:]), prev_point.y)

        yield (prev_point, curr_point)
        prev_point = Point(curr_point.x, curr_point.y)
    return


def get_intersec(wire, segment):
    wire_steps = 0
    for i in range(len(wire) - 1):
        if segment[0].x == segment[1].x and wire[i].y == wire[i + 1].y:
            if (
                min(segment[0].y, segment[1].y) < wire[i].y
                and max(segment[0].y, segment[1].y) > wire[i].y
                and min(wire[i].x, wire[i + 1].x) < segment[0].x
                and max(wire[i].x, wire[i + 1].x) > segment[0].x
            ):
                return (
                    Point(segment[0].x, wire[i].y),
                    wire_steps + abs(segment[0].x - wire[i].x),
                )
        elif segment[0].y == segment[1].y and wire[i].x == wire[i + 1].x:
            if (
                min(segment[0].x, segment[1].x) < wire[i].x
                and max(segment[0].x, segment[1].x) > wire[i].x
                and min(wire[i].y, wire[i + 1].y) < segment[0].y
                and max(wire[i].y, wire[i + 1].y) > segment[0].y
            ):
                return (
                    Point(wire[i].x, segment[0].y),
                    wire_steps + abs(segment[0].y - wire[i].y),
                )
        wire_steps += abs(wire[i + 1].x - wire[i].x) + abs(wire[i + 1].y - wire[i].y)

    return


def manhattan(point1, point2):
    return abs(point2.x - point1.x) + abs(point2.y - point1.y)


def puzzle1(input_f):
    wire1 = get_wire(input_f.readline())
    min_dist = 0
    for segment in get_segment(input_f.readline()):
        intersec = get_intersec(wire1, segment)
        if intersec is not None:
            dist = manhattan(Point(0, 0), intersec[0])
            if min_dist == 0:
                min_dist = dist
            else:
                min_dist = min(min_dist, dist)
    return min_dist


def puzzle2(input_f):
    wire1 = get_wire(input_f.readline())
    wire2_steps = 0
    min_steps = 0
    for segment in get_segment(input_f.readline()):
        intersec = get_intersec(wire1, segment)
        if intersec is not None:
            steps = wire2_steps + manhattan(segment[0], intersec[0]) + intersec[1]
            if min_steps == 0:
                min_steps = steps
            else:
                min_steps = min(min_steps, steps)
        wire2_steps += manhattan(*segment)
    return min_steps


if __name__ == "__main__":
    with open("res/day3.txt", "r") as input_f:
        print(puzzle1(input_f))
        input_f.seek(0)
        print(puzzle2(input_f))
