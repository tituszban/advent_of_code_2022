from dataclasses import dataclass
from typing import TypeVar, Generic

Point = tuple[int, int]

T = TypeVar("T")


class CircularIterable(Generic[T]):
    def __init__(self, instructions: list[T]):
        self._instructions = instructions
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self):
        v = self._instructions[self._i % len(self._instructions)]
        self._i += 1
        return v


example_input = """
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
""".strip()


@dataclass
class Shape:
    points: list[Point]

    def offset(self, p: Point) -> list[Point]:
        return [(point[0] + p[0], point[1] + p[1]) for point in self.points]


shapes = [
    Shape([(0, 0), (1, 0), (2, 0), (3, 0)]),
    Shape([(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]),
    Shape([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),
    Shape([(0, 0), (0, 1), (0, 2), (0, 3)]),
    Shape([(0, 0), (1, 0), (0, 1), (1, 1)])
]


def simulate(instructions: CircularIterable[int], width: int = 7, start_margin: int = 2, start_height: int = 3, iter: int = 2022):
    def _print(_field: dict[Point, bool], _max_height: int):
        for y in range(_max_height, -1, -1):
            for x in range(width):
                if (x, y) in _field:
                    print("#", end="")
                else:
                    print(".", end="")
            print()
        print("=" * width)

    _shapes = CircularIterable(shapes)

    field: dict[Point, bool] = {}
    max_height = 0

    for _ in range(iter):
        shape = next(_shapes)
        pos = (start_margin, max_height + start_height)
        for inst in instructions:
            try_pos_x = (pos[0] + inst, pos[1])
            try_shape_x = shape.offset(try_pos_x)
            if not any(p[0] >= width or p[0] < 0 or p in field for p in try_shape_x):
                pos = try_pos_x
            try_pos_y = (pos[0], pos[1] - 1)
            try_shape_y = shape.offset(try_pos_y)
            pos_shape = shape.offset(pos)
            if not any(p[1] < 0 or p in field for p in try_shape_y):
                pos = try_pos_y
            else:
                for p in pos_shape:
                    field[p] = True
                max_height = max(max_height, *[p[1] + 1 for p in pos_shape])
                break
        # _print(field, max_height)
    return max_height


def main():
    instructions = CircularIterable(
        [1 if c == ">" else -1 for c in example_input])

    print(simulate(instructions, iter=2022), 3068)

    with open("17/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))[0]

    instructions = CircularIterable(
        [1 if c == ">" else -1 for c in test_input])

    print(simulate(instructions, iter=2022))


if __name__ == "__main__":
    main()
