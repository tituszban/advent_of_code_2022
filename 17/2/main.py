from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar("T")
Point = tuple[int, int]


def point_add(p1: Point, p2: Point):
    return (p1[0] + p2[0], p1[1] + p2[1])


class CircularIterable(Generic[T]):
    def __init__(self, instructions: list[T]):
        self._instructions = instructions
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self):
        i = self._i
        v = self._instructions[i]
        self._i = (self._i + 1) % len(self._instructions)
        return v, i


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


def simulate(instructions: CircularIterable[int], width: int = 7, start_margin: int = 2, start_height: int = 3, iter_count: int = 2022):
    def _print(_field: set[Point], _max_height: int):
        for y in range(int(_max_height), -1, -1):
            for x in range(width):
                if (x, y) in _field:
                    print("#", end="")
                else:
                    print(".", end="")
            print()
        print("=" * width)

    def _collide(v: Point, _field: set[Point]):
        return not (0 <= v[0] < width) or v[1] < 0 or v in _field

    _shapes = CircularIterable(shapes)

    cache: dict[tuple[int, int], tuple[int, int]] = {}

    field: set[Point] = set()
    max_height = 0

    for n in range(iter_count):
        shape, i = next(_shapes)
        pos = (start_margin, max_height + start_height)
        for inst, j in instructions:
            px = point_add(pos, (inst, 0))
            if not any([_collide(p, field) for p in shape.offset(px)]):
                pos = px

            py = point_add(pos, (0, -1))
            if not any([_collide(p, field) for p in shape.offset(py)]):
                pos = py
            else:
                break
        final_shape = shape.offset(pos)
        field |= set(final_shape)
        max_height = max(max_height, *[p[1] + 1 for p in final_shape])

        if (c := cache.get((i, j))) is not None and (_it := iter_count - n) % (_n := c[0] - n) == 0:
            d = _it // _n
            return int(max_height + (c[1] - max_height) * d) - 1
        else:
            cache[(i, j)] = (n, max_height)

    return int(max_height)


def main():
    instructions = CircularIterable(
        [1 if c == ">" else -1 for c in example_input])

    print(simulate(instructions, iter_count=1_000_000_000_000), 1514285714288)

    with open("17/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))[0]

    instructions = CircularIterable(
        [1 if c == ">" else -1 for c in test_input])

    print(simulate(instructions, iter_count=1_000_000_000_000))


if __name__ == "__main__":
    main()
