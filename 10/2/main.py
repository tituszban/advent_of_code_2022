class InstructionExecutor:
    def __init__(self):
        self._cycle = 1
        self._value = 1
        self._values: dict[int, int] = {1: 1}

    def exec_instruction(self, inst: str):
        if inst == "noop":
            self._cycle += 1
            self._values[self._cycle] = self._value
        else:
            cmd, val = inst.split(" ")
            assert cmd == "addx"
            val = int(val)
            self._cycle += 1
            self._values[self._cycle] = self._value
            self._value += val
            self._cycle += 1
            self._values[self._cycle] = self._value

    def get_at(self, v: int):
        return self._values.get(v, 0)


def main():
    example_input = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
    """.strip().splitlines()

    executor = InstructionExecutor()
    for line in example_input:
        executor.exec_instruction(line)

    for i in range(6):
        for j in range(1, 41):
            p = i * 40 + j
            v = executor.get_at(p)
            if v <= j and v + 3 > j:
                print("#", end="")
            else:
                print(".", end="")
        print()

    with open("10/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    executor = InstructionExecutor()
    for line in test_input:
        executor.exec_instruction(line)

    for i in range(6):
        for j in range(1, 41):
            p = i * 40 + j
            v = executor.get_at(p)
            if v <= j and v + 3 > j:
                print("#", end="")
            else:
                print(".", end="")
        print()


if __name__ == "__main__":
    main()
