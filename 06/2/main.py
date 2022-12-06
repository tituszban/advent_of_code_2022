def find_start_of_packet(chrs: str, n: int = 14):
    for i in range(len(chrs) - n):
        if len(set(chrs[i:i+n])) == n:
            return i + n


def main():
    with open("06/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    print(find_start_of_packet("mjqjpqmgbljsphdztnvjfqwrcgsmlb"), 19)
    print(find_start_of_packet("bvwbjplbgvbhsrlpgdmjqwftvncz"), 23)
    print(find_start_of_packet("nppdvjthqldpwncqszvftbrmjlhg"), 23)
    print(find_start_of_packet("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"), 29)
    print(find_start_of_packet("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"), 26)
    print(find_start_of_packet(test_input[0]))


if __name__ == "__main__":
    main()
