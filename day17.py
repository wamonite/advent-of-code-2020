#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file, timeit
from functools import reduce
from itertools import product, count
import attr


def parse_data(file_name, dimensions):
    line_list = load_file(file_name)
    cube_list = []
    for y, line in enumerate(line_list):
        for x, c in enumerate(line):
            if c == '#':
                v = [0] * dimensions
                v[0] = x
                v[1] = y
                cube_list.append(tuple(v))

    return tuple(cube_list)


@attr.s
class PocketDimension(object):
    FIELD_NAMES = ['x', 'y', 'z', 'w']

    cube_list = attr.ib(init = False)
    dimensions = attr.ib(init = False)
    cache = attr.ib(init = False)

    @classmethod
    def from_list(cls, cube_list):
        c = cls()
        c.cube_list = cube_list
        c.dimensions = len(cube_list[0])
        c._seed_cache()
        return c

    @property
    def field_names(self):
        return self.FIELD_NAMES[:self.dimensions] + [f'd{v}' for v in range(len(self.FIELD_NAMES), self.dimensions)]

    def get_limits(self):
        return reduce(self._get_limits, self.cube_list)

    def print(self):
        min_vec, max_vec = self.get_limits()
        minx, miny, *min_extra = min_vec
        maxx, maxy, *max_extra = max_vec
        range_list = [range(min_v - 1, max_v + 2) for min_v, max_v in zip(min_extra, max_extra)]
        for extra_dim_val in product(*range_list):
            print(', '.join([f'{self.field_names[idx]} = {extra_dim_val[idx - 2]}' for idx in range(2, self.dimensions)]))
            for y in range(miny - 1, maxy + 2):
                for x in range(minx - 1, maxx + 2):
                    print('#' if self.get_at((x, y) + extra_dim_val) else '.', end = '')
                print()

    @staticmethod
    def _get_limits(limits, coord):
        try:
            min_val, max_val = limits

        except ValueError:
            min_val = limits
            max_val = limits

        return (
            tuple([v if v < min_v else min_v for min_v, v in zip(min_val, coord)]),
            tuple([v if v > max_v else max_v for max_v, v in zip(max_val, coord)]),
        )

    def _seed_cache(self):
        self.cache = {}

        for coord in self.cube_list:
            cache = self.cache
            for v in coord[:-1]:
                cache = cache.setdefault(v, {})
            cache[coord[-1]] = True

    def get_at(self, coord):
        cache = self.cache
        for v in coord:
            if v in cache and isinstance(cache[v], dict):
                cache = cache[v]
            else:
                return v in cache

        return False

    @timeit
    def next(self):
        min_val, max_val = self.get_limits()
        range_list = [range(min_v - 1, max_v + 2) for min_v, max_v in zip(min_val, max_val)]
        new_cube_set = set()
        for coord in product(*range_list):
            active = self.get_at(coord)
            neighbour_range_list = [range(v - 1 , v + 2) for v in coord]
            neighbour_count = 0
            for neighbour_coord in product(*neighbour_range_list):
                if neighbour_coord == coord:
                    continue
                if self.get_at(neighbour_coord):
                    neighbour_count += 1

            if active and neighbour_count == 2 or neighbour_count == 3:
                new_cube_set.add(coord)

            if not active and neighbour_count == 3:
                new_cube_set.add(coord)

        self.cube_list = tuple(new_cube_set)
        self._seed_cache()

    @property
    def cube_count(self):
        return len(self.cube_list)


def print_results(name, file_name, dimensions):
    cube_list = parse_data(file_name, dimensions)
    p = PocketDimension.from_list(cube_list)
    for _ in range(6):
        p.next()
    print(f'{name} {p.cube_count}')


def run():
    print_results(f'part1 test 112 =', 'data/day17_test.txt', 3)
    print_results(f'part1', 'data/day17.txt', 3)

    print_results(f'part2 test 848 =', 'data/day17_test.txt', 4)
    print_results(f'part2', 'data/day17.txt', 4)


if __name__ == "__main__":
    run()
