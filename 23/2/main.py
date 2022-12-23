import numpy as np
import scipy.signal
from collections import defaultdict, deque


example_input = """
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
""".strip().splitlines()

example_input_small = """
.....
..##.
..#..
.....
..##.
.....
""".strip().splitlines()


def _print(area: np.ndarray[np.int8]):
    points = list(zip(*area.nonzero()))
    x_range = max(x := [p[1] for p in points]), min(x)
    y_range = max(y := [p[0] for p in points]), min(y)

    ar = area[y_range[1]:y_range[0] + 1, x_range[1]:x_range[0] + 1]

    for y in range(ar.shape[0]):
        for x in range(ar.shape[1]):
            print("." if ar[y][x] == 0 else "#", end="")
        print()
    print()


def step(lines: list[str]):
    kernels: deque[tuple[np.ndarray, tuple[int, int]]] = deque([
        (np.array([[0, 0, 0], [0, 0, 0], [1, 1, 1]]), (-1, 0)),
        (np.array([[1, 1, 1], [0, 0, 0], [0, 0, 0]]), (1, 0)),
        (np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1]]), (0, -1)),
        (np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0]]), (0, 1)),
    ])

    area = np.zeros((len(lines), len(lines[0])), dtype=np.int8)
    for y, row in enumerate(lines):
        for x, v in enumerate(row):
            if v == "#":
                area[y][x] = 1

    count = np.sum(area)

    i = 0
    while True:
        i += 1
        # print(i)
        if np.any(area[0, :] > 0) or np.any(area[-1, :] > 0) or np.any(area[:, 0] > 0) or np.any(area[:, -1] > 0):
            area = np.pad(area, 1, mode="constant", constant_values=0)
        valid_moves = [
            (np.array(1 - np.clip(
                scipy.signal.convolve2d(area, kernel, mode="same", boundary="fill", fillvalue=0), 0, 1),
                dtype=np.int8) * area, move)
            for kernel, move in kernels
        ]

        frozen = np.array(area)
        for places, _ in valid_moves:
            frozen = np.clip(frozen - (1 - places), 0, 1)

        moves: dict[tuple[int, int], tuple[int, int]] = {}
        move_to_count = defaultdict(int)

        while any(valid_moves):
            places, move = valid_moves.pop(0)
            places = np.clip(places - frozen, 0, 1)

            move_from = list(zip(*places.nonzero()))
            move_to = list(
                zip(*[a + b for a, b in zip(places.nonzero(), move)]))

            for f, t in zip(move_from, move_to):
                assert f not in moves
                moves[f] = t
                move_to_count[t] += 1

            valid_moves = [(np.clip(_places - places, 0, 1), _move)
                           for _places, _move in valid_moves]

        assert np.sum(area) == count
        if not any(moves):
            return i

        for f, t in moves.items():
            if move_to_count[t] < 2:
                area[f[0]][f[1]] = 0
                area[t[0]][t[1]] = 1
        # _print(area)
        assert np.sum(area) == count

        kernels.rotate(-1)


def main():
    print(step(example_input), 20)

    with open("23/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    print(step(test_input))


if __name__ == "__main__":
    main()
