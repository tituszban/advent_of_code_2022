from dataclasses import dataclass
import re
from functools import reduce
from operator import mul


class Res:
    def __init__(self, *a: int):
        self.a = tuple(a)

    def __iter__(self):
        return iter(self.a)

    def __lt__(self, t: "Res"):
        return self.a < t.a

    def __eq__(self, t: "Res"):
        return self.a == t.a

    def __add__(self, t: "Res"):
        return Res(*[a+b for a, b in zip(self, t)])

    def __sub__(self, t: "Res"):
        return Res(*[a-b for a, b in zip(self, t)])

    def __hash__(self) -> int:
        return hash(self.a)

    def __repr__(self) -> str:
        return f"R{self.a}"

    def __getitem__(self, index: int) -> int:
        return self.a[index]


@dataclass(frozen=True)
class Robot:
    produces: Res
    costs: Res

    @classmethod
    def f(cls, produces: str, costs: tuple[int, int, int]):
        return cls(
            Res(
                1 if produces == "geode" else 0,
                1 if produces == "obsidian" else 0,
                1 if produces == "clay" else 0,
                1 if produces == "ore" else 0,
            ),
            Res(
                0, *costs
            )
        )


@dataclass
class State:
    production: Res
    resources: Res


class Blueprint:
    blueprint_re = re.compile(
        r"Blueprint (?P<id>\d+):\s(?P<robots>(Each\s\w+\srobot costs.*\.\s?)+)")
    robot_re = re.compile(
        r"Each (?P<type>\w+) robot costs (?P<cost1>\d+) (?P<res1>\w+)( and (?P<cost2>\d+) (?P<res2>\w+))?")

    def __init__(self, description: str):
        assert (blp_m := self.blueprint_re.match(description))
        self._id = int(blp_m.group("id"))
        self._robots = [
            Robot.f(str(r_m.group("type")), (
                int(r_m.group("cost1")) if r_m.group("res1") == "obsidian" else (
                    int(r_m.group("cost2")) if r_m.group("res2") == "obsidian" else 0),
                int(r_m.group("cost1")) if r_m.group("res1") == "clay" else (
                    int(r_m.group("cost2")) if r_m.group("res2") == "clay" else 0),
                int(r_m.group("cost1")) if r_m.group("res1") == "ore" else (
                    int(r_m.group("cost2")) if r_m.group("res2") == "ore" else 0),
            ))
            for r in blp_m.group("robots").split(".")
            if (r_m := self.robot_re.match(r.strip()))]

    def get_max_production(self, steps: int = 32):
        frontier = [State(resources=Res(0, 0, 0, 0),
                          production=Res(0, 0, 0, 1))]

        for _ in range(steps):
            _frontier: list[State] = []

            for s in frontier:
                for robot in self._robots:
                    if all(h >= c for h,c in zip(s.resources, robot.costs)):
                        _frontier.append(
                            State(
                                resources=s.resources + s.production - robot.costs,
                                production=s.production + robot.produces
                            ))
                _frontier.append(
                    State(
                        resources=s.resources + s.production,
                        production=s.production
                    ))
            frontier = sorted(
                _frontier, key=lambda s: s.resources + s.production)[-4000:]

        best_state = max(frontier, key=lambda s: s.resources[0])
        return best_state.resources[0]


example_input = """
Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian.

Blueprint 2:
  Each ore robot costs 2 ore.
  Each clay robot costs 3 ore.
  Each obsidian robot costs 3 ore and 8 clay.
  Each geode robot costs 3 ore and 12 obsidian.
""".strip().replace("\n  ", " ").replace("\n\n", "\n").splitlines()


def main():
    blueprints = [Blueprint(line) for line in example_input if line]

    print(reduce(mul, [b.get_max_production() for b in blueprints[:3]]), 62 * 56)

    with open("19/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    blueprints = [Blueprint(line) for line in test_input if line]

    print(reduce(mul, [b.get_max_production() for b in blueprints[:3]]))


if __name__ == "__main__":
    main()
