import re

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

def walk(_map: list[str], _input: str):
    def _rotate(facing: int, rot: str):
        if rot == "R":
            return (facing + 1) % 4
        else:
            return (facing + 3) % 4
    
    def _get_direction(facing: int) -> tuple[int, int]:
        return {
            0: (1, 0),
            1: (0, 1),
            2: (-1, 0),
            3: (0, -1)
        }[facing]

    def _off_the_map(pos: tuple[int, int]):
        return pos[1] >= len(_map) or pos[1] < 0 or pos[0] >= len(_map[pos[1]]) or pos[0] < 0 or _map[pos[1]][pos[0]] == " "

    def _get_step(facing: int, position: tuple[int, int]):
        direction = _get_direction(facing)
        coord = (position[0] + direction[0], position[1] + direction[1])
        if _off_the_map(coord):
            i = -1
            cp = position
            while not _off_the_map(c := (position[0] + direction[0] * i, position[1] + direction[1] * i)):
                i -= 1
                cp = c
            coord = cp
        if _map[coord[1]][coord[0]] == "#":
            return position
        return coord

    
    r = re.compile(r"\d+[RL]?")
    instructions = r.findall(_input)
    
    facing = 0
    position = (_map[0].index("."), 0)

    hist = {}

    def _print():
        for y, row in enumerate(_map):
            for x, c in enumerate(row):
                if (x, y) in hist:
                    print({0: ">", 1: "v", 2: "<", 3: "I"}[hist[(x, y)]], end="")
                elif (x, y) == position:
                    print("x", end="")
                else:
                    print(c, end="")
            print()


    for instruction in instructions:
        step, rotate = (int(instruction[:-1]), instruction[-1]) if instruction[-1] in ("L", "R") else (int(instruction), None)
        # print(instruction)
        for _ in range(step):
            next_pos = _get_step(facing, position)
            if next_pos == position:
                break
            position = next_pos
            hist[position] = facing
        if rotate is not None:
            facing = _rotate(facing, rotate)
        hist[position] = facing
    _print()
    
    return 1000 * (position[1] + 1) + 4 * (position[0] + 1) + facing


def main():
    _map, _input = example_input

    print(walk(_map.splitlines(), _input), 6032)

    with open("22/input.txt") as f:
        _map, _input = list(map(lambda l: l.rstrip(), f.read().split("\n\n")))

    print(walk(_map.splitlines(), _input))

    


if __name__ == "__main__":
    main()
