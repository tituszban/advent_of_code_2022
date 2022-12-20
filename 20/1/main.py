from collections import deque

example_input = """
1
2
-3
3
-2
0
4
""".strip().splitlines()


def reorganise_nodes(values: list[str], sample_points=(1000, 2000, 3000)):
    q = deque(list(map(int, values)))
    index = deque(range(0, (l := len(values))))

    for v in range(l):
        p = index.index(v)

        q.rotate(-p)
        index.rotate(-p)

        q_val = q.popleft()
        i_val = index.popleft()

        q.rotate(-q_val)
        index.rotate(-q_val)

        q.append(q_val)
        index.append(i_val)

    print(q)
    zero = q.index(0)
    return sum([q[(zero + s) % l] for s in sample_points])


def main():
    print(reorganise_nodes(example_input), 3)

    with open("20/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    print(reorganise_nodes(test_input))


if __name__ == "__main__":
    main()
