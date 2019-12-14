# https://adventofcode.com/2019/day/14
import math


class Reaction:
    def __init__(self, in_chems, in_chems_qty, out_chem, out_chem_qty):
        self.in_chems = in_chems
        self.in_chems_qty = in_chems_qty
        self.out_chem = out_chem
        self.out_chem_qty = out_chem_qty

    def __repr__(self):
        disp = ""
        for i in range(len(self.in_chems)):
            disp += f"{self.in_chems_qty[i]} {self.in_chems[i]} + "
        disp = disp[:-3]
        disp += f" => {self.out_chem_qty} {self.out_chem}"
        return disp


class Chemical:
    def __init__(self, name, from_reac=None):
        self.name = name
        self.from_reac = from_reac
        self.creates = []

    def __repr__(self):
        return f"{self.name}:\n\tFROM: {self.from_reac}\n\tTO: {self.creates}"


def get_chemicals(input_f):
    chemicals = {}
    for line in input_f.readlines():
        reaction_in, reaction_out = line.split(" => ")
        in_chems, in_chems_qty = [], []
        out_quantity, out_name = reaction_out.replace("\n", "").split(" ")
        for chem in reaction_in.split(", "):
            in_qty, in_name = chem.split(" ")
            in_chems_qty.append(int(in_qty))
            in_chems.append(in_name)
            if in_name in chemicals:
                chemicals[in_name].creates.append(out_name)
            else:
                chemicals[in_name] = Chemical(in_name)
                chemicals[in_name].creates.append(out_name)
        reaction = Reaction(in_chems, in_chems_qty, out_name, int(out_quantity))
        if out_name in chemicals:
            chemicals[out_name].from_reac = reaction
        else:
            chemicals[out_name] = Chemical(out_name, reaction)
    return chemicals


def get_ore_for(name, chemicals, chem_qty, chem_done):
    if name == "ORE":
        return
    can_get_ore = True
    for c in chemicals[name].creates:
        can_get_ore = can_get_ore and chem_done[c]
    if not can_get_ore or chem_done[name]:
        return

    reac = chemicals[name].from_reac
    nb = math.ceil(chem_qty[name] / reac.out_chem_qty)
    for i in range(len(reac.in_chems)):
        chem_qty[reac.in_chems[i]] += nb * reac.in_chems_qty[i]
    chem_done[name] = True

    for i in range(len(reac.in_chems)):
        get_ore_for(reac.in_chems[i], chemicals, chem_qty, chem_done)


def do_reaction(name, chemicals, chem_need_qty, chem_qty, chem_done):
    if name == "ORE":
        return
    can_get_ore = True
    for c in chemicals[name].creates:
        can_get_ore = can_get_ore and chem_done[c]
    if not can_get_ore or chem_done[name]:
        return

    reac = chemicals[name].from_reac
    nb = math.ceil(chem_need_qty[name] / reac.out_chem_qty)
    for i in range(len(reac.in_chems)):
        chem_need_qty[reac.in_chems[i]] += nb * reac.in_chems_qty[i]
    chem_done[name] = True

    if name == "FUEL" or chem_need_qty[name] > chem_qty[name]:
        chem_qty[name] += reac.out_chem_qty
        for i in range(len(reac.in_chems)):
            do_reaction(reac.in_chems[i], chemicals, chem_need_qty, chem_qty, chem_done)
    chem_qty[name] -= chem_need_qty[name]


def puzzle1(chemicals):
    chem_qty = {k: 0 for k in chemicals.keys()}
    chem_qty["FUEL"] = 1
    chem_done = {k: False for k in chemicals.keys()}
    get_ore_for("FUEL", chemicals, chem_qty, chem_done)
    return chem_qty["ORE"]


def puzzle2(chemicals):
    thresh_min = 0
    thresh_max = 1000000000000
    run = True
    while run:
        chem_qty = {k: 0 for k in chemicals.keys()}
        test_value = (thresh_min + thresh_max) // 2
        chem_qty["FUEL"] = test_value
        chem_done = {k: False for k in chemicals.keys()}
        get_ore_for("FUEL", chemicals, chem_qty, chem_done)
        if chem_qty["ORE"] < 1000000000000:
            thresh_min = test_value
        elif chem_qty["ORE"] > 1000000000000:
            thresh_max = test_value
        else:
            return test_value
        if thresh_max - thresh_min == 1:
            return thresh_min


if __name__ == "__main__":
    with open("res/day14.txt") as input_f:
        chemicals = get_chemicals(input_f)
        print(puzzle1(chemicals))
        print(puzzle2(chemicals))
