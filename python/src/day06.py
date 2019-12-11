# https://adventofcode.com/2019/day/6


class Planet:
    def __init__(self, name, center):
        self.name = name
        self.center = center
        self.around = []
        self.distance = 0

    def calc_distance(self):
        if self.name == "COM":
            self.distance = 0
        elif self.center.name == "COM":
            self.distance = 1
        else:
            if self.center.distance == 0:
                self.center.calc_distance()
            self.distance = self.center.distance + 1

    def get_jumps(self):
        jumps = []
        p = self.center
        while p.name != "COM":
            jumps.insert(0, p.name)
            p = p.center
        jumps.insert(0, "COM")
        return jumps

    def __str__(self):
        return self.name + " : " + str(self.distance)


def compute_orbits(orbit_list):
    planets = {}
    for relation in orbit_list:
        center, orbit = relation.split(")")
        if center not in planets:
            planets[center] = Planet(center, None)
        if orbit not in planets:
            planets[orbit] = Planet(orbit, planets[center])
        else:
            planets[orbit].center = planets[center]
        planets[center].around.append(planets[orbit])

    for planet in planets.values():
        planet.calc_distance()

    return planets


def puzzle1(planets):
    return sum([planet.distance for planet in planets.values()])


def puzzle2(planets):
    from_YOU = planets["YOU"].get_jumps()
    from_SAN = planets["SAN"].get_jumps()

    for i in range(min(len(from_YOU), len(from_SAN))):
        if from_YOU[i] != from_SAN[i]:
            return (len(from_YOU) - i) + (len(from_SAN) - i)


if __name__ == "__main__":
    with open("res/day06.txt", "r") as input_f:
        orbit_list = [x.replace("\n", "") for x in input_f.readlines()]
        planets = compute_orbits(orbit_list)
        print(puzzle1(planets))
        print(puzzle2(planets))
