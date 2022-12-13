from typing import Optional, Union
from itertools import chain
from functools import cmp_to_key, reduce
from operator import mul

example_input = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""".strip()

Li = Union[int, "Lists"]
Lists = list[Li]


def parse_lists(lists: list[list[str]]) -> list[tuple[Lists, Lists]]:
    evaled_lists = []
    for pair in lists:
        evaled_lists.append(tuple([eval(line) for line in pair if line]))
    return evaled_lists


def compare(left: Lists, right: Lists) -> Optional[bool]:
    def _compare(_left: Li, _right: Li) -> Optional[bool]:
        if isinstance(_left, int) and isinstance(_right, int):
            if _left == _right:
                return None
            return _left < _right
        if isinstance(_left, list) and isinstance(_right, list):
            return compare(_left, _right)
        if isinstance(_left, int):
            return compare([_left], _right)
        if isinstance(_right, int):
            return compare(_left, [_right])

    i = 0
    ln_l = len(left)
    ln_r = len(right)
    while i < min(ln_l, ln_r):
        v = _compare(left[i], right[i])
        if v is not None:
            return v
        i += 1
    if ln_l == ln_r:
        return None
    return ln_l < ln_r


def cmp(left: Lists, right: Lists) -> int:
    if (r := compare(left, right)) is None:
        return 0
    return 1 if r else -1


def solve(lists: list[tuple[Lists, Lists]]) -> int:
    dividers = [[[2]], [[6]]]
    flat = [*list(chain(*lists)), *dividers]

    s_lists = sorted(flat, key=cmp_to_key(cmp), reverse=True)

    return reduce(mul, [s_lists.index(d) + 1 for d in dividers])


def main():
    _example_input = list(map(lambda g: list(
        map(lambda l: l.strip(), g.split("\n"))), example_input.split("\n\n")))

    lists = parse_lists(_example_input)

    print(solve(lists), 140)

    with open("13/input.txt") as f:
        test_input = list(map(lambda g: list(
            map(lambda l: l.strip(), g.split("\n"))), f.read().split("\n\n")))

    lists = parse_lists(test_input)

    print(solve(lists))


if __name__ == "__main__":
    main()
