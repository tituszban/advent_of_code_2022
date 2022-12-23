import re

Point = tuple[int, int]
Location = tuple[int, Point]
Edge = tuple[Point, Point]

example_input = """
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
""".strip(" ").lstrip("\n").split("\n\n")

test_input = """
        ....
        ....
        ....
        ....
............
............
............
............
        ........
        ........
        ........
        ........

16R1R15L16L1L11R16L1L16
""".strip(" ").lstrip("\n").split("\n\n")


def get_direction(facing: int) -> Point:
    return {
        0: (1, 0),
        1: (0, 1),
        2: (-1, 0),
        3: (0, -1)
    }[facing]


def lerp(r1: tuple[int, int], r2: tuple[int, int], v):
    if (r1[0] > r1[1]) == (r2[0] > r2[1]):
        return v - min(r1) + min(r2)
    else:
        return max(r1) - v + min(r2)


def is_vertical(edge: Edge):
    return edge[0][0] == edge[1][0]


class Cube:
    def __init__(self, _map: list[str], mappings: list[tuple[Edge, Edge]]) -> None:
        self._map = _map
        self._mappings = mappings

    def _off_the_map(self, pos: Point):
        return pos[1] >= len(self._map) or pos[1] < 0 or pos[0] >= len(self._map[pos[1]]) or pos[0] < 0 or self._map[pos[1]][pos[0]] == " "

    def _find_mapping(self, location: Location):
        facing, position = location

        def _in_range(edge: Edge):
            p1, p2 = edge
            if p1[0] == p2[0] and p1[0] == position[0] and sorted([p1[1], p2[1], position[1]])[1] == position[1]:
                return True
            if p1[1] == p2[1] and p1[1] == position[1] and sorted([p1[0], p2[0], position[0]])[1] == position[0]:
                return True
            return False

        for e1, e2 in self._mappings:
            if _in_range(e1) and ((is_vertical(e1) and facing in [0, 2]) or (not is_vertical(e1) and facing in [1, 3])):
                return e1, e2
            if _in_range(e2) and ((is_vertical(e2) and facing in [0, 2]) or (not is_vertical(e2) and facing in [1, 3])):
                return e2, e1

        assert False

    def _step_edge(self, location: Location, from_edge: Edge, to_edge: Edge) -> Location:
        facing, position = location
        if is_vertical(from_edge):      # Vertical from edge
            if is_vertical(to_edge):      # Vertical to edge
                new_x = lerp((from_edge[0][1], from_edge[1][1]),
                             (to_edge[0][1], to_edge[1][1]), position[1])
                pos = (to_edge[0][0], new_x)
                facing = facing if (from_edge[0][1] > from_edge[1][1]) == (to_edge[0][1] > to_edge[1][1]) else (facing + 2) % 4
                return facing, pos
            else:   # Horizontal to edge
                new_x = lerp((from_edge[0][1], from_edge[1][1]),
                             (to_edge[0][0], to_edge[1][0]), position[1])
                pos = (new_x, to_edge[0][1])
                facing = (facing + 3) % 4 if (from_edge[0][1] > from_edge[1][1]) == (to_edge[0][0] > to_edge[1][0]) else (facing + 1) % 4
                return facing, pos
        else:       # Horizontal from edge
            if is_vertical(to_edge):      # Vertical to edge
                new_x = lerp((from_edge[0][0], from_edge[1][0]),
                             (to_edge[0][1], to_edge[1][1]), position[0])
                pos = (to_edge[0][0], new_x)
                facing = (facing + 1) % 4 if (from_edge[0][0] > from_edge[1][0]) == (to_edge[0][1] > to_edge[1][1]) else (facing + 3) % 4
                return facing, pos
            else:   # Horizontal to edge
                new_x = lerp((from_edge[0][0], from_edge[1][0]),
                             (to_edge[0][0], to_edge[1][0]), position[0])
                pos = (new_x, to_edge[0][1])
                facing = facing if (from_edge[0][0] > from_edge[1][0]) == (to_edge[0][0] > to_edge[1][0]) else (facing + 2) % 4
                return facing, pos

    def step(self, location: Location):
        facing, position = location
        new_facing = facing
        direction = get_direction(facing)
        new_position: Point = (
            position[0] + direction[0], position[1] + direction[1])
        if self._off_the_map(new_position):
            from_edge, to_edge = self._find_mapping(location)

            new_facing, new_position = self._step_edge(
                location, from_edge, to_edge)

        if self._map[new_position[1]][new_position[0]] == "#":
            return facing, position
        return new_facing, new_position


def walk(_map: list[str], _input: str, cube: Cube):
    def _rotate(loc: Location, rot: str) -> Location:
        facing, position = loc
        if rot == "R":
            return (facing + 1) % 4, position
        else:
            return (facing + 3) % 4, position

    r = re.compile(r"\d+[RL]?")
    instructions = r.findall(_input)

    location: Location = 0, (_map[0].index("."), 0)

    hist = {}

    def _print():
        for y, row in enumerate(_map):
            for x, c in enumerate(row):
                if (x, y) in hist:
                    print({0: ">", 1: "v", 2: "<", 3: "^"}
                          [hist[(x, y)]], end="")
                else:
                    print(c, end="")
            print()
        print()

    for instruction in instructions:
        step, rotate = (int(instruction[:-1]), instruction[-1]) if instruction[-1] in (
            "L", "R") else (int(instruction), None)
        # print(instruction)
        for _ in range(step):
            next_loc = cube.step(location)
            if next_loc == location:
                break
            location = next_loc
            f, p = location
            hist[p] = f
            # _print()
        if rotate is not None:
            location = _rotate(location, rotate)
        f, p = location
        hist[p] = f
        # _print()

    facing, position = location
    return 1000 * (position[1] + 1) + 4 * (position[0] + 1) + facing


def main():
    _map, _input = example_input
    _map = _map.splitlines()
    _cube = Cube(_map, [
        (((8, 0), (8, 3)), ((4, 4), (7, 4))),
        (((8, 0), (11, 0)), ((3, 4), (0, 4))),
        (((11, 0), (11, 3)), ((15, 11), (15, 8))),
        (((11, 4), (11, 7)), ((15, 8), (12, 8))),
        (((15, 11), (12, 11)), ((0, 4), (0, 7))),
        (((11, 11), (8, 11)), ((0, 7), (3, 7))),
        (((8, 11), (8, 8)), ((4, 7), (7, 7))),
    ])

    print(walk(_map, _input, _cube), 5031)

    with open("22/input.txt") as f:
        _map, _input = list(map(lambda l: l.rstrip(), f.read().split("\n\n")))
    _map = _map.splitlines()
    _cube = Cube(_map, [
        (((100, 49), (149, 49)), ((99, 50), (99, 99))),
        (((149, 49), (149, 0)), ((99, 100), (99, 149))),
        (((50, 149), (99, 149)), ((49, 150), (49, 199))),
        (((49, 199), (0, 199)), ((149, 0), (100, 0))),
        (((99, 0), (50, 0)), ((0, 199), (0, 150))),
        (((50, 49), (50, 0)), ((0, 100), (0, 149))),
        (((50, 99), (50, 50)), ((49, 100), (0, 100)))
    ])

    print(walk(_map, _input, _cube))


if __name__ == "__main__":
    main()
