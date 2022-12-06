import re


class Stacks:
    def __init__(self, initial_layout: list[tuple[str]]):
        stack_count = max([len(row) for row in initial_layout])

        self._stacks = [
            [
                row[i]
                for row in reversed(initial_layout)
                if len(row) > i and row[i].strip()
            ]

            for i in range(stack_count)
        ]

    def move(self, count, stack_from, stack_to):
        self._stacks[stack_to - 1].extend(self._stacks[stack_from-1][-count:])
        self._stacks[stack_from-1] = self._stacks[stack_from-1][:-count]

    def get_top(self):
        return ''.join(s[-1] for s in self._stacks)


def main():
    with open("05/input.txt") as f:
        layout, actions = list(map(lambda s: list(
            map(lambda l: l.strip("\n"), s.split("\n"))), f.read().split("\n\n")))

    actions_re = re.compile(r"move (\d+) from (\d+) to (\d+)")

    parsed_layout = [[line[i * 4 + 1]
                      for i in range(len(line) // 4 + 1)] for line in layout[:-1]]

    stacks = Stacks(parsed_layout)

    parsed_actions = [list(map(int, actions_re.match(line).groups()))
                      for line in actions if line]

    for c, f, t in parsed_actions:
        stacks.move(c, f, t)

    print(stacks.get_top())


if __name__ == "__main__":
    main()
