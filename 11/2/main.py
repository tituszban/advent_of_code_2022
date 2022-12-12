from typing import Callable


class Monkey:
    def __init__(self,
                 operation: Callable[[int], int],
                 test: Callable[[int], int],
                 starting_values: list[int],
                 max_mod: int):
        self._operation = operation
        self._test = test
        self._values = starting_values
        self._inspect_count = 0
        self._max_mod = max_mod

    def get_throws(self) -> list[tuple[int, int]]:
        throws: list[tuple[int, int]] = []
        while any(self._values):
            self._inspect_count += 1
            v_old = self._values.pop(0)
            v_new = self._operation(v_old) % self._max_mod
            throw_to = self._test(v_new)
            throws.append((v_new, throw_to))
        return throws

    def receive_throw(self, v: int):
        self._values.append(v)

    @property
    def inspect_count(self):
        return self._inspect_count


example_input = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""


def main():
    example_max_mod = 23 * 19 * 13 * 17
    example_monkeys = {
        0: Monkey(
            lambda o: o * 19,
            lambda v: 2 if v % 23 == 0 else 3,
            [79, 98],
            example_max_mod
        ),
        1: Monkey(
            lambda o: o + 6,
            lambda v: 2 if v % 19 == 0 else 0,
            [54, 65, 75, 74],
            example_max_mod
        ),
        2: Monkey(
            lambda o: o * o,
            lambda v: 1 if v % 13 == 0 else 3,
            [79, 60, 97],
            example_max_mod
        ),
        3: Monkey(
            lambda o: o + 3,
            lambda v: 0 if v % 17 == 0 else 1,
            [74],
            example_max_mod
        )
    }

    for i in range(10000):
        for monkey in example_monkeys.values():
            throws = monkey.get_throws()
            for v, to in throws:
                example_monkeys[to].receive_throw(v)

    monkeys = sorted(example_monkeys.values(),
                     key=lambda m: m.inspect_count, reverse=True)

    print(monkeys[0].inspect_count * monkeys[1].inspect_count, 2713310158)

    with open("11/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    # It's faster to type this up, than writing a parser...
    test_max_mod = 2 * 7 * 3 * 17 * 11 * 19 * 5 * 13
    test_monkeys = {
        0: Monkey(
            lambda o: o * 5,
            lambda v: 4 if v % 2 == 0 else 3,
            [80],
            test_max_mod
        ),
        1: Monkey(
            lambda o: o + 7,
            lambda v: 5 if v % 7 == 0 else 6,
            [75, 83, 74],
            test_max_mod
        ),
        2: Monkey(
            lambda o: o + 5,
            lambda v: 7 if v % 3 == 0 else 0,
            [86, 67, 61, 96, 52, 63, 73],
            test_max_mod
        ),
        3: Monkey(
            lambda o: o + 8,
            lambda v: 1 if v % 17 == 0 else 5,
            [85, 83, 55, 85, 57, 70, 85, 52],
            test_max_mod
        ),
        4: Monkey(
            lambda o: o + 4,
            lambda v: 3 if v % 11 == 0 else 1,
            [67, 75, 91, 72, 89],
            test_max_mod
        ),
        5: Monkey(
            lambda o: o * 2,
            lambda v: 6 if v % 19 == 0 else 2,
            [66, 64, 68, 92, 68, 77],
            test_max_mod
        ),
        6: Monkey(
            lambda o: o * o,
            lambda v: 2 if v % 5 == 0 else 7,
            [97, 94, 79, 88],
            test_max_mod
        ),
        7: Monkey(
            lambda o: o + 6,
            lambda v: 4 if v % 13 == 0 else 0,
            [77, 85],
            test_max_mod
        )
    }

    for i in range(10000):
        for monkey in test_monkeys.values():
            throws = monkey.get_throws()
            for v, to in throws:
                test_monkeys[to].receive_throw(v)

    monkeys = sorted(test_monkeys.values(),
                     key=lambda m: m.inspect_count, reverse=True)

    print(monkeys[0].inspect_count * monkeys[1].inspect_count)


if __name__ == "__main__":
    main()
