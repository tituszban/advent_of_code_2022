from dataclasses import dataclass
import re
from typing import Optional


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


StateKey = tuple[str, tuple[tuple[str, bool], ...]]


@dataclass(frozen=True)
class State:
    valves_open: tuple[tuple[str, bool], ...]
    position: str
    sum_flow_rate: int
    time: int
    flow_rate: int
    visited: tuple[str, ...]
    remaining_potential: int

    @property
    def valves(self):
        return {valve: state for valve, state in self.valves_open}

    @property
    def score(self):
        return self.sum_flow_rate + self.remaining_potential

    @property
    def key(self) -> StateKey:
        return tuple([self.position, self.valves_open])

    def run_to(self, t: int):
        assert t >= self.time, "No time travel"
        return State(
            valves_open=self.valves_open,
            position=self.position,
            sum_flow_rate=self.sum_flow_rate +
            (t - self.time) * self.flow_rate,
            time=t,
            flow_rate=self.flow_rate,
            visited=self.visited,
            remaining_potential=0
        )

    def go_and_open(self, path: list[str], valve_to_open: str, added_flow_rate: int, potential: int):
        assert not self.valves[valve_to_open], "Valve already open"
        dt = len(path) + 1
        return State(
            valves_open=tuple((key, state or key == valve_to_open)
                              for key, state in self.valves_open),
            position=valve_to_open,
            sum_flow_rate=self.sum_flow_rate + self.flow_rate * dt,
            time=self.time + dt,
            flow_rate=self.flow_rate + added_flow_rate,
            visited=tuple([*self.visited, *path, valve_to_open]),
            remaining_potential=potential
        )


class Frontier:
    def __init__(self, *values: State):
        self._sorted: list[State] = sorted(
            values, key=lambda p: p.score)
        self._lookup: dict[StateKey, State] = {
            value.key: value for value in values}

    def any(self):
        return any(self._sorted)

    def add(self, value: State):
        if value.key in self._lookup:
            if self._lookup[value.key].score >= value.score:
                return
            p = self._lookup[value.key]
            self._sorted.remove(p)
        self._lookup[value.key] = value

        i = 0
        while i < len(self._sorted) and value.score > self._sorted[i].score:
            i += 1

        self._sorted.insert(i, value)

    def pop(self) -> State:
        p = self._sorted.pop(-1)
        del self._lookup[p.key]
        return p

    def has(self, p: State) -> bool:
        return p in self._lookup


class PathPlanner:
    def __init__(self, valves: dict[str, Valve]):
        self._valves = valves
        self._paths: dict[tuple[str, str], list[str]] = {}

        for key, valve in valves.items():
            for neighbour in valve.neighbours:
                self._paths[(key, neighbour)] = [neighbour]

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


def explore(valves: dict[str, Valve], start: str, total_time: int):
    def _potential(valves_to_open: list[str], remaining_time: int, base_flow: int):
        flows = sorted(
            [valves[valve].flow_rate for valve in valves_to_open], reverse=True)
        potential_flow = 0
        total_flow = base_flow
        while any(flows) and remaining_time >= 0:
            potential_flow += total_flow
            total_flow += flows.pop(0)
            remaining_time -= 1
            if remaining_time <= 0:
                break
        return potential_flow + total_flow * max(remaining_time, 0)

    path_planner = PathPlanner(valves)
    initial_state = State(tuple(
        (key, False) for key, valve in valves.items() if valve.flow_rate > 0),
        start, 0, 0, 0, [], _potential(valves.keys(), total_time, 0))

    frontier = Frontier(initial_state)

    while frontier.any():
        state = frontier.pop()

        if state.time >= total_time or all(state.valves.values()):
            final_state = state.run_to(total_time)
            return final_state.sum_flow_rate

        valves_to_visit = [key for key,
                           value in state.valves.items() if not value]

        for valve_to_visit in valves_to_visit:
            path = path_planner.go_to(state.position, valve_to_visit)
            next_state = state.go_and_open(
                path, valve_to_visit, valves[valve_to_visit].flow_rate,
                _potential(valves_to_visit, total_time - (state.time + len(path)), state.flow_rate))
            if next_state.time <= total_time:
                frontier.add(next_state)


def main():
    valves = parse(example_input)
    print(explore(valves, "AA", 30), 1651)

    with open("16/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    valves = parse(test_input)
    print(explore(valves, "AA", 30))


if __name__ == "__main__":
    main()
