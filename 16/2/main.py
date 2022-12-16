from dataclasses import dataclass, replace
import re
from typing import Optional
from functools import cache


class Valve:
    def __init__(self, name: str, flow_rate: int, neighbours: tuple[str]):
        self._name = name
        self._flow_rate = flow_rate
        self._neighbours = neighbours

    def __repr__(self):
        return f"Valve({self._name}, {self._flow_rate}, {self._neighbours})"

    @property
    def neighbours(self):
        return self._neighbours

    @property
    def flow_rate(self):
        return self._flow_rate


example_input = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""".strip().splitlines()


def parse(lines: list[str]) -> dict[str, Valve]:
    valve_re = re.compile(
        r"Valve (?P<name>\w+) has flow rate=(?P<flow_rate>\d+); tunnels? leads? to valves? (?P<neighbours>.*)")

    valves: dict[str, Valve] = {}
    for line in lines:
        if not line:
            continue
        assert (m := valve_re.match(line))
        valves[m.group("name")] = Valve(m.group("name"), int(
            m.group("flow_rate")), tuple(m.group("neighbours").split(", ")))
    return valves


class PathPlanner:
    def __init__(self, valves: dict[str, Valve]):
        self._valves = valves
        self._paths: dict[tuple[str, str], list[str]] = {}

        for key, valve in valves.items():
            for neighbour in valve.neighbours:
                self._paths[(key, neighbour)] = [neighbour]
                self._paths[(key, key)] = [key]

        any_changed = True
        while any_changed:
            any_changed = False
            paths = list(self._paths.items())
            for start_end, path in paths:
                start, end = start_end
                for neighbour in valves[end].neighbours:
                    if (start, neighbour) in self._paths:
                        continue
                    any_changed = True
                    self._paths[(start, neighbour)] = [*path, neighbour]

    def go_to(self, start: str, goal: str) -> list[str]:
        return self._paths[(start, goal)]

    def distance(self, start: str, end: str) -> int:
        return len(self.go_to(start, end))


def explore(valves: dict[str, Valve], start: str, total_time: int):

    path_planner = PathPlanner(valves)
    relevant_valves = [(key, valve) for key,
                       valve in valves.items() if valve.flow_rate > 0]
    
    @cache
    def exp(p: tuple[str, int], e: tuple[str, int], visited: tuple[str, ...]):  # urgh, this is ugly
        best_result = 0

        for key, valve in relevant_valves:
            if key in visited:
                continue
            new_visited = tuple(sorted([*visited, key]))
            p_loc, p_time = p
            if p_time - (p_d := path_planner.distance(p_loc, key)) >= 1:
                time_left = p_time - p_d - 1
                p_move = exp((key, time_left), e, new_visited) + time_left * valve.flow_rate
                best_result = max(p_move, best_result)
            e_loc, e_time = e
            if e_time - (e_d := path_planner.distance(e_loc, key)) >= 1:
                time_left = e_time - e_d - 1
                e_move = exp(e, (key, time_left), new_visited) + time_left * valve.flow_rate
                best_result = max(e_move, best_result)
        return best_result
    
    return exp((start, total_time), (start, total_time), ())


def main():
    valves = parse(example_input)
    print(explore(valves, "AA", 26), 1707)

    with open("16/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    valves = parse(test_input)
    print(explore(valves, "AA", 26))


if __name__ == "__main__":
    main()
