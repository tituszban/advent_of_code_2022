import numpy as np
import scipy.signal

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


def parse(lines: list[str]) -> np.ndarray[np.int8]:
    points = set([tuple(map(int, line.split(","))) for line in lines])

    x_min, x_max = min(x := [p[0] for p in points]), max(x)
    y_min, y_max = min(y := [p[1] for p in points]), max(y)
    z_min, z_max = min(z := [p[2] for p in points]), max(z)

    points = [add_point(p, (-x_min, -y_min, -z_min)) for p in points]

    x_range = x_max - x_min
    y_range = y_max - y_min
    z_range = z_max - z_min

    space = np.zeros((x_range + 1, y_range + 1, z_range + 1), dtype=np.int8)
    for point in points:
        space[point] = 1

    return space


def find_sides(space: np.ndarray[np.int8]):     # I was wrong
    kernel = np.array([[[0, 0, 0], [0, 1, 0], [0, 0, 0]], [[0, 1, 0], [
                      1, 0, 1], [0, 1, 0]], [[0, 0, 0], [0, 1, 0], [0, 0, 0]]])

    is_outside = np.pad(np.zeros_like(space), 1,
                        mode="constant", constant_values=1)
    padded_space = np.pad(space, 1, mode="constant", constant_values=0)

    def expant(_is_outside: np.ndarray[np.int8]):
        return np.clip(np.clip(scipy.signal.convolve(_is_outside, kernel, mode="same"), 0, 1) - padded_space, 0, 1)

    while not np.array_equal(is_outside, (expanded := expant(is_outside))):
        is_outside = expanded

    c = scipy.signal.convolve(is_outside, kernel, mode="same") * padded_space

    return np.sum(c)


def main():
    space = parse(example_input)

    print(find_sides(space), 58)

    with open("18/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    space = parse(test_input)

    print(find_sides(space))


if __name__ == "__main__":
    main()
