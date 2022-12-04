
def find_fully_overlapping_count(pairs: list[str]):
    def _to_binary_range(v1, v2):
        b = 0
        for i in range(v1-1, v2):
            b |= 1 << i
        return b

    sections = [
        tuple(map(
            lambda v: _to_binary_range(*tuple(map(int, v.split("-")))),
            p.split(",")))
        for p in pairs]

    fully_overlapping = [s[0] & s[1] == s[0]
                         or s[0] & s[1] == s[1] for s in sections]

    return sum(fully_overlapping)


def main():
    with open("04/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    print(find_fully_overlapping_count(test_input))


if __name__ == "__main__":
    main()
