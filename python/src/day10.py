# https://adventofcode.com/2019/day/10
import math


class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"


def display_map(asteroid_map):
    disp = ""
    height = len(asteroid_map[0])
    width = len(asteroid_map)
    for h in range(height):
        for w in range(width):
            disp += asteroid_map[w][h]
        disp += "\n"
    return disp


def get_asteroid_map(input_f):
    lines = [line.replace("\n", "") for line in input_f.readlines()]
    height = len(lines)
    width = len(lines[0])
    asteroid_map = [None] * width
    for w in range(width):
        asteroid_map[w] = [None] * height
        for h in range(height):
            asteroid_map[w][h] = lines[h][w]
    return asteroid_map


def get_asteroids(input_f):
    asteroid_map = get_asteroid_map(input_f)
    height = len(asteroid_map[0])
    width = len(asteroid_map)
    asteroid_loc = []
    for x in range(width):
        for y in range(height):
            if asteroid_map[x][y] == "#":
                asteroid_loc.append(Coordinates(x, y))
    return asteroid_loc


def best_station(asteroids):
    max_monitoring = 0
    best_station = None
    for asteroid in asteroids:
        azimuths = set()
        for other in asteroids:
            if other.x != asteroid.x or other.y != asteroid.y:
                azimuths.add(azimuth(asteroid, other) * 180 / math.pi)
        if len(azimuths) > max_monitoring:
            max_monitoring = len(azimuths)
            best_station = Coordinates(asteroid.x, asteroid.y)
    return max_monitoring, best_station


def get_visible_asteroids(station, asteroids):
    azimuths = {}
    for other in asteroids:
        if other.x != station.x or other.y != station.y:
            angle = azimuth(station, other) * 180 / math.pi
            if angle < -90:
                angle += 450
            else:
                angle += 90
            if not (
                angle in azimuths
                and azimuths[angle].x + azimuths[angle].y > other.x + other.y
            ):
                azimuths[angle] = other
    return azimuths


def azimuth(from_coord, to_coord):
    return math.atan2(to_coord.y - from_coord.y, to_coord.x - from_coord.x)


def puzzle1(asteroids):
    return best_station(asteroids)[0]


def puzzle2(asteroids):
    station = best_station(asteroids)[1]
    vaporize_count = 0
    while vaporize_count <= 200:
        azimuths = get_visible_asteroids(station, asteroids)
        for angle in sorted(azimuths):
            if vaporize_count == 199:
                target = azimuths[angle]
                return 100 * target.x + target.y
            asteroids.remove(azimuths[angle])
            vaporize_count += 1


if __name__ == "__main__":
    with open("res/day10.txt") as input_f:
        asteroids = get_asteroids(input_f)
        print(puzzle1(asteroids))
        print(puzzle2(asteroids))
