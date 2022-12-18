Point = tuple[int, int, int]

def add_point(p1: Point, p2: Point) -> Point:
    return (p1[0] + p2[0], p1[1] + p2[1], p1[2] + p2[2])

example_input = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
""".strip().splitlines()

def parse(lines: list[str]) -> set[Point]:
    return set([tuple(map(int, line.split(","))) for line in lines])


def find_sides(points: set[Point]):     # This is so simple, surely I won't need numpy and convolution
    c = 0

    for point in points:
        for neighbour in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            if add_point(point, neighbour) not in points:
                c += 1
    return c


def main():
    points = parse(example_input)

    print(find_sides(points), 64)

    with open("18/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    points = parse(test_input)

    print(find_sides(points))

    


if __name__ == "__main__":
    main()
