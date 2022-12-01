
def main():
    with open("01/input.txt") as f:
        elves = [sum(list(map(int, elf.split("\n"))))
                 for elf in f.read().strip().split("\n\n")]

        print(sum(sorted(elves, reverse=True)[:3]))


if __name__ == "__main__":
    main()
