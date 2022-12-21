from fractions import Fraction

example_input = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
""".strip().splitlines()


class Node:
    def __init__(self, expr: str):
        try:
            val = int(expr)
        except:
            val = None
        self._val = val

        self._expr = expr.split(" ")
        self._cache = None

    def get(self, values: dict[str, "Node"]) -> int:
        if self._val is not None:
            return Fraction(self._val)
        v1 = values[self._expr[0]].get(values)
        v2 = values[self._expr[2]].get(values)

        op = self._expr[1]
        if op == "+":
            return v1 + v2
        elif op == "-":
            return v1 - v2
        elif op == "*":
            return v1 * v2
        elif op == "/":
            return v1 / v2

        assert False


def main():
    lines = {s[0]: Node(s[1])
             for line in example_input if line and (s := line.split(": "))}

    print(lines["root"].get(lines), 152)

    with open("21/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    lines = {s[0]: Node(s[1])
             for line in test_input if line and (s := line.split(": "))}

    print(lines["root"].get(lines))


if __name__ == "__main__":
    main()
