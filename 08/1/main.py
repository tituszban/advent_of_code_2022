def count_visible(grid):
    is_visible = [[False for _ in row] for row in grid]

    for i, col in enumerate(grid):
        max_val = -1
        for j, v in enumerate(col):
            if v > max_val:
                max_val = v
                is_visible[i][j] = True
        max_val = -1
        for j, v in reversed(list(enumerate(col))):
            if v > max_val:
                max_val = v
                is_visible[i][j] = True
    
    is_visible_T = list(map(list, zip(*is_visible)))
    grid_T = list(zip(*grid))

    for i, col in enumerate(grid_T):
        max_val = -1
        for j, v in enumerate(col):
            if v > max_val:
                max_val = v
                is_visible_T[i][j] = True
        max_val = -1
        for j, v in reversed(list(enumerate(col))):
            if v > max_val:
                max_val = v
                is_visible_T[i][j] = True

    return sum([sum(col) for col in is_visible_T])


def main():
    example_input = """
30373
25512
65332
33549
35390
    """.strip().splitlines()
    example_input = list(map(lambda v: list(map(int, v)), example_input))

    print(count_visible(example_input), 21)

    with open("08/input.txt") as f:
        test_input = list(map(lambda l: list(map(int, l.strip())), f.readlines()))

    print(count_visible(test_input))


if __name__ == "__main__":
    main()
