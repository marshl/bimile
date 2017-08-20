import argparse
from random import random


class TrafficModel:
    DOWN = 'D'
    RIGHT = 'R'
    EMPTY = '.'

    def __init__(self, scale: int, density: float):
        self.scale = scale
        self.density = density
        self.turn = self.DOWN

        self.cells = [[
            self.EMPTY if random() > density
            else self.DOWN if random() >= 0.5
            else self.RIGHT
            for x in range(self.scale)
        ] for y in range(self.scale)]

    def __str__(self):
        # return "\n".join([' '.join([str(self.cells[y][x]) for x in range(self.scale)]) for y in range(self.scale)])
        str = ''
        for y in range(self.scale):
            str += ' '.join(self.cells[y]) + "\n"

        return str

    def step(self):

        cell_copy = [[self.EMPTY for x in range(self.scale)] for y in range(self.scale)]

        for y in reversed(range(self.scale)):
            for x in reversed(range(self.scale)):

                if self.cells[y][x] == self.EMPTY:
                    continue

                if self.turn == self.DOWN:
                    if self.cells[y][x] == self.DOWN and self.cells[(y + 1) % self.scale][x] == self.EMPTY:
                        cell_copy[(y + 1) % self.scale][x] = self.DOWN
                    else:
                        cell_copy[y][x] = self.cells[y][x]

                elif self.turn == self.RIGHT:
                    if self.cells[y][x] == self.RIGHT and self.cells[y][(x + 1) % self.scale] == self.EMPTY:
                        cell_copy[y][(x + 1) % self.scale] = self.RIGHT
                    else:
                        cell_copy[y][x] = self.cells[y][x]

        self.turn = self.DOWN if self.turn == self.RIGHT else self.RIGHT
        self.cells = cell_copy


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates a Biham–Middleton–Levine traffic model gif')
    parser.add_argument('scale', type=int,
                        help='the height and width of the grid')

    parser.add_argument('density', type=float,
                        help='the density of the traffic (0.0 - 1.0)')

    args = parser.parse_args()

    traffic_model = TrafficModel(args.scale, args.density)
    # print(traffic_model)
    # traffic_model.step()
    # print("\n")
    # print(traffic_model)
    for x in range(1000):
        print("\n")
        print(traffic_model.turn);
        print(traffic_model)
        traffic_model.step()
