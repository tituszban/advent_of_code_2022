def calculate_scenic_score(grid):
    scenic_score = [[1 for _ in row] for row in grid]

    for i, col in enumerate(grid):
        scores = {k: 0 for k in range(10)}
        for j, v in enumerate(col):
            scenic_score[i][j] *= scores[v]
            scores = {k: 1 if k <= v else scores[k] + 1 for k in range(10)}
        scores = {k: 0 for k in range(10)}
        for j, v in reversed(list(enumerate(col))):
            scenic_score[i][j] *= scores[v]
            scores = {k: 1 if k <= v else scores[k] + 1 for k in range(10)}
    
    scenic_score_T = list(map(list, zip(*scenic_score)))
    grid_T = list(zip(*grid))

    for i, col in enumerate(grid_T):
        scores = {k: 0 for k in range(10)}
        for j, v in enumerate(col):
            scenic_score_T[i][j] *= scores[v]
            scores = {k: 1 if k <= v else scores[k] + 1 for k in range(10)}
        scores = {k: 0 for k in range(10)}
        for j, v in reversed(list(enumerate(col))):
            scenic_score_T[i][j] *= scores[v]
            scores = {k: 1 if k <= v else scores[k] + 1 for k in range(10)}

    return max([max(col) for col in scenic_score_T])


def main():
    example_input = """
30373
25512
65332
33549
35390
    """.strip().splitlines()
    example_input = list(map(lambda v: list(map(int, v)), example_input))

    print(calculate_scenic_score(example_input), 8)

    with open("08/input.txt") as f:
        test_input = list(map(lambda l: list(map(int, l.strip())), f.readlines()))

    print(calculate_scenic_score(test_input))


if __name__ == "__main__":
    main()
