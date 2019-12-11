# https://adventofcode.com/2019/day/8


class Layer:
    def __init__(self, width=0, height=0):
        self.lines = []
        self.width = width
        self.height = height
        if width != 0 and height != 0:
            for i in range(height):
                self.lines.append(["2"] * width)

    def add_line(self, line):
        self.lines.append(line)

    def count(self, c):
        count = 0
        for line in self.lines:
            count += line.count(c)
        return count

    def get_pixel(self, width, height):
        return self.lines[height][width]

    def set_pixel(self, width, height, pixel):
        self.lines[height][width] = pixel

    def display(self):
        disp = ""
        for line in self.lines:
            for p in line:
                if p == "0":
                    disp += " "
                elif p == "1":
                    disp += "█"
            disp += "\n"
        return disp

    def __repr__(self):
        return str(self.lines)


def build_layers(input_s, width, height):
    layers = []
    line = []
    layer = Layer()
    for i, c in enumerate(input_s):
        if i % width == 0:
            layer.add_line(line[:])
            line = []
        if i % (width * height) == 0:
            layers.append(layer)
            layer = Layer()
        line.append(c)
    layer.add_line(line[:])
    layers.append(layer)
    del layers[0]
    return layers


def puzzle1(input_s, width, height):
    layers = build_layers(input_s, width, height)
    layer_min = -1
    layer_min_c = len(input_s)
    for layer_i, layer in enumerate(layers):
        nb_of_0 = layer.count("0")
        if nb_of_0 < layer_min_c:
            layer_min_c = nb_of_0
            layer_min = layer_i
    return layers[layer_min].count("1") * layers[layer_min].count("2")


def puzzle2(input_s, width, height):
    layers = build_layers(input_s, width, height)
    final_layer = Layer(width, height)
    for layer in reversed(layers):
        for h in range(height):
            for w in range(width):
                layer_pixel = layer.get_pixel(w, h)
                if layer_pixel != "2":
                    final_layer.set_pixel(w, h, layer_pixel)
    return final_layer.display()


if __name__ == "__main__":
    with open("res/day08.txt") as input_f:
        width = 25
        height = 6
        print(puzzle1(input_f.read(), width, height))
        input_f.seek(0)
        print(puzzle2(input_f.read(), width, height))
