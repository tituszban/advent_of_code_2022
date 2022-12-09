Point = tuple[int, int]


def print_rope(rope: list[Point]):
    range_x = min(x := [p[0] for p in rope]), max(x) + 1
    range_y = min(y := [p[1] for p in rope]), max(y) + 1

    for y in reversed(range(*range_y)):
        for x in range(*range_x):
            for i, p in enumerate(rope):
                if (x, y) == p:
                    print(i, end="")
                    break
            else:
                if (x, y) == (0, 0):
                    print("s", end="")
                else:
                    print(".", end="")
        print()
    print()


def simulate(moves: list[tuple[str, int]]):
    directions = {
        "U": (0, 1),
        "D": (0, -1),
        "L": (-1, 0),
        "R": (1, 0)
    }

    rope: list[Point] = [(0, 0) for _ in range(10)]

    def dist_sq(p1: Point, p2: Point):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

    def sign(v: int):
        return 0 if v == 0 else (-1 if v < 0 else 1)

    tail_visited = {rope[-1]}

    for d, c in moves:
        dHead = directions[d]
        print(d, c)
        for _ in range(c):
            head = rope[0]
            head = (head[0] + dHead[0], head[1] + dHead[1])
            new_rope = [head]

            for i, p in enumerate(rope[1:]):
                prev_p = new_rope[i]
                if dist_sq(p, prev_p) > 2:
                    rel_pos = (
                        (dx := prev_p[0] - p[0]) - sign(dx), (dy := prev_p[1] - p[1]) - sign(dy))
                    new_rope.append(
                        (prev_p[0] - rel_pos[0], prev_p[1] - rel_pos[1]))
                else:
                    new_rope.append(p)

            tail_visited.add(new_rope[-1])
            rope = new_rope
        print_rope(rope)
        print(rope)
    return len(tail_visited)


def main():
    example_input = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
    """.strip().splitlines()
    example_input = list(map(lambda l: l.strip().split(), example_input))

    print(simulate([(l[0], int(l[1])) for l in example_input]), 1)

    example_input_2 = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
    """.strip().splitlines()
    example_input_2 = list(map(lambda l: l.strip().split(), example_input_2))

    print(simulate([(l[0], int(l[1])) for l in example_input_2]), 36)

    with open("09/input.txt") as f:
        test_input = list(map(lambda l: l.strip().split(), f.readlines()))

    print(simulate([(l[0], int(l[1])) for l in test_input]))


if __name__ == "__main__":
    main()
