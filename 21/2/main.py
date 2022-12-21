from fractions import Fraction
from typing import Optional


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
    def __init__(self, line: str):
        self.idx, expr = line.split(": ")
        try:
            val = int(expr)
        except:
            val = None
        self._val = val

        sp = expr.split(" ")
        self.left_node = sp[0] if val is None else None
        self.right_node = sp[2] if val is None else None
        self.op = sp[1] if val is None else None
        self.parent = None

    def add_parent(self, parent: Optional[str], values: dict[str, "Node"]):
        self.parent = parent
        if self._val is not None:
            return
        values[self.left_node].add_parent(self.idx, values)
        values[self.right_node].add_parent(self.idx, values)

    def get(self, values: dict[str, "Node"]) -> int:
        if self._val is not None:
            return Fraction(self._val)
        l = values[self.left_node].get(values)
        r = values[self.right_node].get(values)

        if self.op == "+":
            return l + r
        elif self.op == "-":
            return l - r
        elif self.op == "*":
            return l * r
        elif self.op == "/":
            return l / r
        assert False

    def get_rev(self, child: str, values: dict[str, "Node"]):
        other_node, ls = (self.left_node, True) if child != self.left_node else (
            self.right_node, False)
        if self.idx == "root":
            return values[other_node].get(values)
        assert self.parent is not None
        parent_val = values[self.parent].get_rev(self.idx, values)

        if self.op == "-":
            if ls:
                return values[other_node].get(values) - parent_val
            else:
                return parent_val + values[other_node].get(values)
        if self.op == "/":
            if ls:
                return values[other_node].get(values) / parent_val
            else:
                return parent_val * values[other_node].get(values)
        if self.op == "*":
            return parent_val / values[other_node].get(values)
        if self.op == "+":
            return parent_val - values[other_node].get(values)
        assert False


def main():
    nodes = {s[0]: Node(line)
             for line in example_input if line and (s := line.split(": "))}
    nodes["root"].add_parent(None, nodes)

    print(nodes[nodes["humn"].parent].get_rev("humn", nodes), 301)

    with open("21/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    nodes = {s[0]: Node(line)
             for line in test_input if line and (s := line.split(": "))}

    nodes["root"].add_parent(None, nodes)

    print(nodes[nodes["humn"].parent].get_rev("humn", nodes))


if __name__ == "__main__":
    main()
