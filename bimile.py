import argparse
from random import random
from wand.drawing import Drawing
from wand.color import Color
from wand.image import Image
import threading
import queue
from typing import List


class TrafficModel:
    DOWN = "D"
    RIGHT = "R"
    EMPTY = "."

    def __init__(self, scale: int, density: float):
        self.scale: int = scale
        self.density: float = density
        self.turn: str = self.DOWN

        self.cells: List[List[str]] = [
            [
                self.EMPTY
                if random() > density
                else self.DOWN
                if random() >= 0.5
                else self.RIGHT
                for x in range(self.scale)
            ]
            for y in range(self.scale)
        ]

        self.cell_history: List[List[List[str]]] = [self.cells]

    def __str__(self) -> str:
        return "\n".join(
            [
                " ".join([str(self.cells[y][x]) for x in range(self.scale)])
                for y in range(self.scale)
            ]
        )

    def step(self):

        cell_copy = [[self.EMPTY for x in range(self.scale)] for y in range(self.scale)]

        for y in reversed(range(self.scale)):
            for x in reversed(range(self.scale)):

                if self.cells[y][x] == self.EMPTY:
                    continue

                if self.turn == self.DOWN:
                    if (
                        self.cells[y][x] == self.DOWN
                        and self.cells[(y + 1) % self.scale][x] == self.EMPTY
                    ):
                        cell_copy[(y + 1) % self.scale][x] = self.DOWN
                    else:
                        cell_copy[y][x] = self.cells[y][x]

                elif self.turn == self.RIGHT:
                    if (
                        self.cells[y][x] == self.RIGHT
                        and self.cells[y][(x + 1) % self.scale] == self.EMPTY
                    ):
                        cell_copy[y][(x + 1) % self.scale] = self.RIGHT
                    else:
                        cell_copy[y][x] = self.cells[y][x]

        self.turn = self.DOWN if self.turn == self.RIGHT else self.RIGHT
        self.cells = cell_copy

    def save_state(self) -> None:
        self.cell_history.append(self.cells)


def render_frame(frame_index: int):
    print(f"\rFrame {frame_index}", end="")

    frame: Image = Image(
        width=traffic_model.scale * args.cell_size,
        height=traffic_model.scale * args.cell_size,
        background=Color("white"),
    )

    with Drawing() as draw:
        cell_types = {TrafficModel.DOWN: "#0000ff", TrafficModel.RIGHT: '#ff0000'}
        for cell_type, colour in cell_types.items():
            draw.fill_color = Color(colour)
            for y in range(traffic_model.scale):
                for x in range(traffic_model.scale):
                    if traffic_model.cell_history[frame_index][y][x] != cell_type:
                        continue

                    if args.cell_size == 1:
                        draw.point(x, y)
                    else:
                        draw.rectangle(
                            left=x * args.cell_size,
                            top=y * args.cell_size,
                            width=args.cell_size - 1,
                            height=args.cell_size - 1,
                        )

        draw(frame)

    frames.append(frame)


class RenderThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            frame_index = self.queue.get()
            render_frame(frame_index)
            self.queue.task_done()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Creates a Biham–Middleton–Levine traffic model gif"
    )
    parser.add_argument("scale", type=int, help="the height and width of the grid")

    parser.add_argument(
        "density", type=float, help="the density of the traffic (0.0 - 1.0)"
    )

    parser.add_argument(
        "frame_count", type=int, help="the number of frames in the output gif"
    )

    parser.add_argument(
        "--frame-skip",
        type=int,
        default=1,
        help="the number of spaces that the cells should move in each frame",
    )

    parser.add_argument(
        "--cell-size", type=int, default=1, help="the number of pixels for each cell"
    )

    args = parser.parse_args()

    traffic_model = TrafficModel(args.scale, args.density)

    for i in range(args.frame_count):
        for j in range(args.frame_skip):
            traffic_model.step()
            traffic_model.step()

        traffic_model.save_state()
        print(f"\rSimulation step {i}", end="")

    print("\nSimulation complete. Rendering...")
    frames: List[Image] = []

    render_queue = queue.Queue()
    for i in range(args.frame_count):
        render_queue.put(i)

    for i in range(1, 4):
        thread = RenderThread(render_queue)
        thread.setDaemon(True)
        thread.start()

    render_queue.join()

    with Image() as img:
        for frame in frames:
            img.sequence.append(frame)
            frame.delay = 10

        img.type = "optimize"
        img.save(filename="output.gif")
