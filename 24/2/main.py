from collections import defaultdict


Point = tuple[int, int]

example_input = """
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""".strip().splitlines()

directions = {
    0: (1, 0),
    1: (0, -1),
    2: (-1, 0),
    3: (0, 1)
}

blizzard_facings = ">^<v"

def add(p1: Point, p2: Point):
    return (p1[0] + p2[0], p1[1] + p2[1])


def update_map(blizzards: tuple[int, Point], width: int, height: int):
    w = width - 2
    h = height - 2

    def _update_blizzard(b: tuple[int, Point]):
        facing, pos = b
        step = directions[facing]
        return facing, (
            (pos[0] + step[0] - 1 + w) % w + 1,
            (pos[1] + step[1] - 1 + h) % h + 1,
        )
    return list(map(_update_blizzard, blizzards))

def print_map(width: int, height: int, blizzards: list[tuple[int, Point]], l: Point):
    blizzards_by_location: dict[Point, list[int]] = defaultdict(list)
    for f, p in blizzards:
        blizzards_by_location[p].append(f)

    for y in range(height):
        for x in range(width):
            p = (x, y)
            if p == l:
                print("E", end="")
            elif p in blizzards_by_location:
                if len(blizzards_by_location[p]) == 1:
                    print(blizzard_facings[blizzards_by_location[p][0]], end="")
                else:
                    print(len(blizzards_by_location[p]), end="")
            elif x > 0 and x < width - 1 and y > 0 and y < height - 1:
                print(".", end="")
            else:
                print("#", end="")
        print()
    print()
            

def explore(lines: list[str]):
    connected: dict[Point, list[Point]] = {}
    blizzards: list[tuple[int, Point]] = []
    height = len(lines)
    width = len(lines[0])

    start = (1, 0)
    goal = (width - 2, height - 1)

    for y, line in enumerate(lines):
        for x, v in enumerate(line):
            p = (x, y)
            if v == "#":
                continue
            connected[p] = []
            for s in directions.values():
                if (n := add(p, s)) in connected:
                    connected[n].append(p)
                    connected[p].append(n)

            if v in blizzard_facings:
                blizzards.append((blizzard_facings.index(v), p))

    
    # print_map(width, height, blizzards, start)

    def go(_start: Point, _goal: Point):
        nonlocal blizzards
        t = 0
        frontier: list[Point] = [_start]

        while True:
            t += 1
            blizzards = update_map(blizzards, width, height)
            blizzard_locations = {b[1] for b in blizzards}
            # print(t)
            # print_map(width, height, blizzards, frontier[0])

            new_frontier: set[Point] = set()
            for p in frontier:
                neighbours = connected[p]
                for f in [*neighbours, p]:
                    if f == _goal:
                        return t
                    if f not in blizzard_locations:
                        new_frontier.add(f)
        
            frontier = list(new_frontier)
    
    l1 = go(start, goal)
    l2 = go(goal, start)
    l3 = go(start, goal)

    return l1 + l2 + l3

                    


def main():
    print(explore(example_input), 54)

    with open("24/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    print(explore(test_input))


if __name__ == "__main__":
    main()
