from functools import reduce


def rank_bag_duplicates(bags):
    duplicates = [list(reduce(lambda b1, b2: set(b1).intersection(
        set(b2)), bags[i: i+3]))[0] for i in range(0, len(bags), 3)]

    ranks = [o - ord("a") + 1 if (o := ord(d)) > ord("a")
             else o - ord("A") + 27 for d in duplicates]

    return sum(ranks)


def main():
    with open("03/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    print(rank_bag_duplicates(test_input))


if __name__ == "__main__":
    main()
