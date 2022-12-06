def find_start_of_packet(chrs: str):
    for i in range(len(chrs) - 4):
        if len(set(chrs[i:i+4])) == 4:
            return i + 4


def main():
    with open("06/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    print(find_start_of_packet("mjqjpqmgbljsphdztnvjfqwrcgsmlb"), 7)
    print(find_start_of_packet("bvwbjplbgvbhsrlpgdmjqwftvncz"), 5)
    print(find_start_of_packet("nppdvjthqldpwncqszvftbrmjlhg"), 6)
    print(find_start_of_packet("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"), 10)
    print(find_start_of_packet("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"), 11)
    print(find_start_of_packet(test_input[0]))


if __name__ == "__main__":
    main()
