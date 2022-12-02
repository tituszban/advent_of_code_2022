
def score_round(opponent: str, us: str):
    base_score = {
        "X": 1,
        "Y": 2,
        "Z": 3
    }

    o = (ord(opponent) - ord("A"))
    u = (ord(us) - ord("X"))

    win_score = 3 if o == u else (6 if (o + 1) % 3 == u else 0)

    return base_score[us] + win_score


def evaluate(rounds: list[tuple[str, str]]):
    return sum(list(map(lambda v: score_round(*v), rounds)))


def main():
    with open("02/input.txt") as f:
        test_input = list(map(lambda l: l.strip().split(), f.readlines()))

    results = evaluate(test_input)

    print(results)


if __name__ == "__main__":
    main()
