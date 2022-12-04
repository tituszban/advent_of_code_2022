
def rank_bag_duplicates(bags):
    duplicates = [list((set(l[:len(l) // 2]).intersection(set(l[len(l) // 2:]))))[0]
                  for l in bags]

    ranks = [o - ord("a") + 1 if (o := ord(d)) > ord("a")
             else o - ord("A") + 27 for d in duplicates]

    return sum(ranks)


def main():
    with open("03/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    print(rank_bag_duplicates(test_input))


if __name__ == "__main__":
    main()
