example_input = """
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
""".strip().splitlines()


def from_snafu(val: str):
    return sum([5 ** i * {
        "2": 2,
        "1": 1,
        "0": 0,
        "-": -1,
        "=": -2
    }[c] for i, c in enumerate(reversed(val))])


def to_snafu(val: int):
    s = ""
    while val > 0:
        m = val % 5
        v = m if m < 3 else -5+m
        s = {
            2: "2",
            1: "1",
            0: "0",
            -1: "-",
            -2: "="
        }[v] + s
        val //= 5
        if m >= 3:
            val += 1
    return s


def main():
    print(v := sum(map(from_snafu, example_input)), 4890)
    print(to_snafu(v))

    with open("25/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    print(v := sum(map(from_snafu, test_input)))
    print(to_snafu(v))


if __name__ == "__main__":
    main()
