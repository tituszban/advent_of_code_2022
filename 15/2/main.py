import re
from typing import Optional

Point = tuple[int, int]


def dist(p1: Point, p2: Point):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class Sensor:
    def __init__(self, position: Point, closest_beacon: Point):
        self._p = position
        self._b = closest_beacon
        self._r = dist(position, closest_beacon)

    def can_have_beacon(self, point: Point):
        return dist(point, self._p) > self._r

    def blank_on_line(self, y) -> Optional[tuple[int, int]]:
        if (y_dist := abs(self._p[1] - y)) > self._r:
            return None
        px = self._p[0]
        dx = self._r - y_dist + 1
        return tuple([px - dx + 1, px + dx])

    @property
    def b(self):
        return self._b

    @property
    def p(self):
        return self._p

    @property
    def r(self):
        return self._r

    def __repr__(self):
        return f"Sensor({self._p},{self._b},{self._r})"


example_input = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""".strip().splitlines()


def parse(lines: list[str]) -> list[Sensor]:
    sensor_re = re.compile(
        r"Sensor at x=(?P<sx>-?\d+), y=(?P<sy>-?\d+): closest beacon is at x=(?P<bx>-?\d+), y=(?P<by>-?\d+)")

    sensors: list[Sensor] = []

    for line in lines:
        if not line:
            continue
        assert (m := sensor_re.match(line))
        sensors.append(Sensor((int(m.group("sx")), int(m.group("sy"))),
                       (int(m.group("bx")), int(m.group("by")))))
    return sensors


def print_area(sensors: list[Sensor], min_x, max_x, min_y, max_y):
    sensor_points = set(sensor.p for sensor in sensors)
    beacon_points = set(sensor.b for sensor in sensors)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            p = (x, y)
            if p in sensor_points:
                print("S", end="")
            elif p in beacon_points:
                print("B", end="")
            elif not all(sensor.can_have_beacon(p) for sensor in sensors):
                print("#", end="")
            else:
                print(".", end="")
        print()


def scan_area(sensors: list[Sensor], min_c: int, max_c: int):
    sorted_sensors = sorted(sensors, key=lambda s: s.p[0])

    for y in range(min_c, max_c + 1):
        ranges = sorted(
            [r for sensor in sorted_sensors if (r := sensor.blank_on_line(y))])

        x = min_c

        for r in ranges:
            if r[0] > x:
                return x * 4000000 + y
            if r[1] > max_c:
                break
            x = max(x, r[1])


def main():

    sensors = parse(example_input)
    print_area(sensors, 0, 21, 0, 21)
    print(scan_area(sensors, 0, 20), 56000011)

    with open("15/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    sensors = parse(test_input)
    print(scan_area(sensors, 0, 4000000))


if __name__ == "__main__":
    main()
