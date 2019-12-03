# https://adventofcode.com/2019/day/3


def get_wire(line):
    wire = [(0, 0)]
    count = 0
    for instruction in line.split(","):
        direction = instruction[0]
        if direction == "U":
            wire.append((wire[count][0], wire[count][1] + int(instruction[1:])))
        if direction == "D":
            wire.append((wire[count][0], wire[count][1] - int(instruction[1:])))
        if direction == "L":
            wire.append((wire[count][0] - int(instruction[1:]), wire[count][1]))
        if direction == "R":
            wire.append((wire[count][0] + int(instruction[1:]), wire[count][1]))
        count += 1
    return wire


def get_segment(line):
    prev_point = (0, 0)
    for instruction in line.split(","):
        direction = instruction[0]
        curr_point = (0, 0)
        if direction == "U":
            curr_point = (prev_point[0], prev_point[1] + int(instruction[1:]))
        if direction == "D":
            curr_point = (prev_point[0], prev_point[1] - int(instruction[1:]))
        if direction == "L":
            curr_point = (prev_point[0] - int(instruction[1:]), prev_point[1])
        if direction == "R":
            curr_point = (prev_point[0] + int(instruction[1:]), prev_point[1])

        yield (prev_point, curr_point)
        prev_point = curr_point[:]
    return


def get_intersec(wire, segment):
    wire_steps = 0
    for i in range(len(wire) - 1):
        if segment[0][0] == segment[1][0] and wire[i][1] == wire[i + 1][1]:
            if (
                min(segment[0][1], segment[1][1]) < wire[i][1]
                and max(segment[0][1], segment[1][1]) > wire[i][1]
                and min(wire[i][0], wire[i + 1][0]) < segment[0][0]
                and max(wire[i][0], wire[i + 1][0]) > segment[0][0]
            ):
                return (
                    segment[0][0],
                    wire[i][1],
                    wire_steps + abs(segment[0][0] - wire[i][0]),
                )
        elif segment[0][1] == segment[1][1] and wire[i][0] == wire[i + 1][0]:
            if (
                min(segment[0][0], segment[1][0]) < wire[i][0]
                and max(segment[0][0], segment[1][0]) > wire[i][0]
                and min(wire[i][1], wire[i + 1][1]) < segment[0][1]
                and max(wire[i][1], wire[i + 1][1]) > segment[0][1]
            ):
                return (
                    wire[i][0],
                    segment[0][1],
                    wire_steps + abs(segment[0][1] - wire[i][1]),
                )
        wire_steps += abs(wire[i + 1][0] - wire[i][0]) + abs(
            wire[i + 1][1] - wire[i][1]
        )

    return


def manhattan(point1, point2):
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])


def puzzle1(input_f):
    wire1 = get_wire(input_f.readline())
    min_dist = 0
    for segment in get_segment(input_f.readline()):
        intersec = get_intersec(wire1, segment)
        if intersec is not None:
            dist = manhattan((0, 0), intersec[0:2])
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
            steps = wire2_steps + manhattan(segment[0], intersec[0:2]) + intersec[2]
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
