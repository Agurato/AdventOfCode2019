# https://adventofcode.com/2019/day/12
import itertools
import json


class Moon:
    def __init__(self, pos):
        self.pos = pos
        self.vel = XYZ(0, 0, 0)
    
    def update_pos(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.pos.z += self.vel.z
    
    def energy(self):
        return self.pos.energy() * self.vel.energy()
    
    def __repr__(self):
        return f"pos={self.pos}, vel={self.vel}"


class XYZ:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)
    
    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"


def calc_gravity(moon1, moon2):
    if moon1.pos.x < moon2.pos.x:
        moon1.vel.x += 1
        moon2.vel.x -= 1
    elif moon1.pos.x > moon2.pos.x:
        moon1.vel.x -= 1
        moon2.vel.x += 1
    if moon1.pos.y < moon2.pos.y:
        moon1.vel.y += 1
        moon2.vel.y -= 1
    elif moon1.pos.y > moon2.pos.y:
        moon1.vel.y -= 1
        moon2.vel.y += 1
    if moon1.pos.z < moon2.pos.z:
        moon1.vel.z += 1
        moon2.vel.z -= 1
    elif moon1.pos.z > moon2.pos.z:
        moon1.vel.z -= 1
        moon2.vel.z += 1


def get_moons(lines):
    return [Moon(XYZ(*[int(pair.split("=")[1].replace(">", "")) for pair in line.split(", ")])) for line in lines]
    
    
def gcd(a, b):
    """Compute the greatest common divisor of a and b"""
    while b > 0:
        a, b = b, a % b
    return a
    
def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b // gcd(a, b)

def puzzle1(input_f):
    moons = get_moons(input_f.readlines())
    for _ in range(1000):
        for pair in itertools.combinations(moons, r=2):
            calc_gravity(*pair)
        for moon in moons:
            moon.update_pos()
    return sum(moon.energy() for moon in moons)


def puzzle2(input_f):
    moons = get_moons(input_f.readlines())
    x_history = set()
    x_repeat = 0
    y_history = set()
    y_repeat = 0
    z_history = set()
    z_repeat = 0
    count = 0
    run = True
    while(run):
        for pair in itertools.combinations(moons, r=2):
            calc_gravity(*pair)
        for moon in moons:
            moon.update_pos()
        if x_repeat == 0:
            x = tuple((moon.pos.x, moon.vel.x) for moon in moons)
            if x in x_history:
                x_repeat = count
            else:
                x_history.add(x)
        if y_repeat == 0:
            y = tuple((moon.pos.y, moon.vel.y) for moon in moons)
            if y in y_history:
                y_repeat = count
            else:
                y_history.add(y)
        if z_repeat == 0:
            z = tuple((moon.pos.z, moon.vel.z) for moon in moons)
            if z in z_history:
                z_repeat = count
            else:
                z_history.add(z)
        if x_repeat != 0 and y_repeat != 0 and z_repeat != 0:
            run = False
        count += 1
    return lcm(lcm(x_repeat, y_repeat), z_repeat)


if __name__ == "__main__":
    with open("res/day12.txt") as input_f:
        print(puzzle1(input_f))
        input_f.seek(0)
        print(puzzle2(input_f))
            