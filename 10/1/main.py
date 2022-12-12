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
        return self._values.get(v, 0) * v


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

    print(executor.get_at(20), 420)
    print(executor.get_at(60), 1140)
    print(executor.get_at(100), 1800)
    print(executor.get_at(140), 2940)
    print(executor.get_at(180), 2880)
    print(executor.get_at(220), 3960)

    with open("10/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    executor = InstructionExecutor()
    for line in test_input:
        executor.exec_instruction(line)

    print(sum([executor.get_at(v) for v in [20, 60, 100, 140, 180, 220]]))


if __name__ == "__main__":
    main()
