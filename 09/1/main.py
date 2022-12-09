Point = tuple[int, int]


def simulate(moves: list[tuple[str, int]]):
    directions = {
        "U": (0, 1),
        "D": (0, -1),
        "L": (-1, 0),
        "R": (1, 0)
    }
    head: Point = (0, 0)
    tail: Point = (0, 0)

    def dist_sq(p1: Point, p2: Point):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

    tail_visited = {tail}

    for d, c in moves:
        dHead = directions[d]
        for _ in range(c):
            head = (head[0] + dHead[0], head[1] + dHead[1])
            if dist_sq(head, tail) > 2:
                tail = (head[0] - dHead[0], head[1] - dHead[1])
                tail_visited.add(tail)
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

    print(simulate([(l[0], int(l[1])) for l in example_input]), 13)

    with open("09/input.txt") as f:
        test_input = list(map(lambda l: l.strip().split(), f.readlines()))

    print(simulate([(l[0], int(l[1])) for l in test_input]))


if __name__ == "__main__":
    main()
