class NodeABC:
    def size(self) -> int:
        raise NotImplementedError


class Directory(NodeABC):
    def __init__(self, name: str):
        self._children: list[NodeABC] = []
        self._name = name

    def add_child(self, child: NodeABC):
        self._children.append(child)

    def size(self):
        return sum(c.size() for c in self._children)

    def __repr__(self):
        return f"dir {self._name}"

    def __str__(self):
        children = '\n'.join(
            ['\n'.join("  " + l for l in str(c).split("\n"))
             for c in self._children])

        return "{}\n{}".format(self.__repr__(), children)

    def traverse(self):
        yield self
        for c in self._children:
            if isinstance(c, Directory):
                yield from c.traverse()


class File(NodeABC):
    def __init__(self, name: str, size: int) -> None:
        self._name = name
        self._size = size

    def size(self):
        return self._size

    def __repr__(self):
        return f"{self._size} {self._name}"


def build_tree(cmds: list[str]):
    dir_stack: list[Directory] = []

    for line in cmds:
        if line[0] == "$":
            command = line[2:]
            if command == "ls":
                pass
            elif command[:2] == "cd":
                d = command.split()[1]
                if d == "/":
                    dir_stack = [Directory("/")]
                elif d == "..":
                    dir_stack.pop(-1)
                else:
                    new_dir = Directory(d)
                    dir_stack[-1].add_child(new_dir)
                    dir_stack.append(new_dir)
        elif line[:3] == "dir":
            pass
        else:
            size, file_name = line.split()
            dir_stack[-1].add_child(File(file_name, int(size)))
    return dir_stack[0]


def find_dir_to_delete(root: Directory, total_size: int = 70000000, space_needed: int = 30000000):
    space_to_free_up = space_needed - (total_size - (rs := root.size()))
    min_size = rs

    for dir in root.traverse():
        if (s := dir.size()) > space_to_free_up and s < min_size:
            min_size = s
    return min_size


def main():
    example = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
    """.strip()
    example_nodes = build_tree(example.splitlines())
    print(find_dir_to_delete(example_nodes), 24933642)

    with open("07/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))
    nodes = build_tree(test_input)

    print(find_dir_to_delete(nodes))


if __name__ == "__main__":
    main()
