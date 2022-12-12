from dataclasses import dataclass


Point = tuple[int, int]


@dataclass(frozen=True)
class GridPoint:
    location: Point
    height: int
    neighbours: tuple[Point, ...]


@dataclass(frozen=True)
class FrontierPoint:
    location: Point
    history: tuple[Point, ...]
    hist_len: int
    heuristic: int

    @property
    def score(self):
        return self.hist_len + self.heuristic


class Frontier:
    def __init__(self, *values: FrontierPoint):
        self._sorted: list[FrontierPoint] = sorted(
            values, key=lambda p: p.score)
        self._lookup: dict[Point, FrontierPoint] = {
            value.location: value for value in values}

    def any(self):
        return any(self._sorted)

    def add(self, value: FrontierPoint):
        if value.location in self._lookup:
            p = self._lookup[value.location]
            self._sorted.remove(p)
        self._lookup[value.location] = value

        i = 0
        while i < len(self._sorted) and value.score > self._sorted[i].score:
            i += 1

        self._sorted.insert(i, value)

    def pop(self) -> FrontierPoint:
        p = self._sorted.pop(0)
        del self._lookup[p.location]
        return p

    def has(self, p: Point) -> bool:
        return p in self._lookup


def a_star(grid: dict[Point, GridPoint], start: Point, end: Point):
    frontier: Frontier = Frontier(FrontierPoint(end, tuple(), 0, 0))
    explored: set[Point] = set()

    while frontier.any():
        p = frontier.pop()

        explored.add(p.location)

        g = grid[p.location]

        if g.height == 0:
            return p.hist_len

        for neighbour in g.neighbours:
            if grid[neighbour].height >= g.height - 1 and neighbour not in explored and not frontier.has(neighbour):
                frontier.add(FrontierPoint(
                    neighbour, tuple([*p.history, p.location]),
                    p.hist_len + 1,
                    g.height
                ))


def grid_to_points(grid: list[str]) -> tuple[dict[Point, GridPoint], Point, Point]:
    grid_points: dict[Point, GridPoint] = {}
    height = len(grid)
    width = len(grid[0])
    start = None
    end = None

    def _get_neighbours(x, y) -> tuple[Point, ...]:
        neighbours = []
        if x + 1 < width:
            neighbours.append((x + 1, y))
        if y + 1 < height:
            neighbours.append((x, y + 1))
        if x - 1 >= 0:
            neighbours.append((x - 1, y))
        if y - 1 >= 0:
            neighbours.append((x, y - 1))
        return tuple(neighbours)
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            p = (x, y)
            if c == "S":
                start = p
                c = "a"
            elif c == "E":
                end = p
                c = "z"
            grid_points[p] = GridPoint(
                p, ord(c) - ord("a"), _get_neighbours(x, y))
    return grid_points, start, end


example_input = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""".strip().splitlines()


def main():
    grid, start, end = grid_to_points(example_input)
    print(a_star(grid, start, end), 29)

    with open("12/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    grid, start, end = grid_to_points(test_input)
    print(a_star(grid, start, end))


if __name__ == "__main__":
    main()
