Point = tuple[int, int]


class Line:
    def __init__(self, start: Point, end: Point):
        self._start = start
        self._end = end

    def apply(self, grid: dict[Point, "Line"]):
        for x in range(min(self._start[0], self._end[0]), max(self._start[0], self._end[0]) + 1):
            for y in range(min(self._start[1], self._end[1]), max(self._start[1], self._end[1]) + 1):
                grid[(x, y)] = self
        return grid


example_input = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""".strip().splitlines()


def parse(lines: list[str]) -> list[tuple[Line]]:
    points = [
        [tuple(map(int, seg.split(",")))
         for seg in line.split(" -> ")]
        for line in lines
        if line
    ]

    parsed_lines: list[tuple[Line]] = []
    for ps in points:
        parsed_lines.append(tuple([Line(p1, p2)
                            for p1, p2 in zip(ps, ps[1:])]))
    return parsed_lines


def simulate(grid: dict[Point, Line], start: Point = (500, 0)):
    count = 0
    bottom = max(key[1] for key in grid)
    seen: set[Point] = set()

    def _step(point: Point):
        nonlocal count
        seen.add(point)
        if point in grid:
            return True
        if point[1] >= bottom + 2:
            return True

        for x in [0, -1, 1]:
            np = (point[0] + x, point[1] + 1)
            if np in seen:
                continue
            if not _step(np):
                return False
        count += 1
        return True

    _step(start)

    return count


def main():
    lines = parse(example_input)

    grid: dict[Point, Line] = {}
    for line in lines:
        for seg in line:
            seg.apply(grid)

    print(simulate(grid), 93)

    with open("14/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    lines = parse(test_input)

    grid: dict[Point, Line] = {}
    for line in lines:
        for seg in line:
            seg.apply(grid)

    print(simulate(grid))


if __name__ == "__main__":
    main()
