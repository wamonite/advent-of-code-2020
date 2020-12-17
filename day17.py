#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file, timeit
from functools import reduce, lru_cache
from itertools import product


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


def get_limits(limits, coord):
    try:
        min_val, max_val = limits

    except ValueError:
        min_val = limits
        max_val = limits

    return (
        tuple([v if v < min_v else min_v for min_v, v in zip(min_val, coord)]),
        tuple([v if v > max_v else max_v for max_v, v in zip(max_val, coord)]),
    )


@lru_cache(maxsize = 1000)
def get_at(cube_list, coord):
    return coord in cube_list


def print_cube_3(cube_list):
    (minx, miny, minz), (maxx, maxy, maxz) = reduce(get_limits, cube_list)
    for z in range(minz - 1, maxz + 2):
        print(f'{z=}')
        for y in range(miny - 1, maxy + 2):
            for x in range(minx - 1, maxx + 2):
                print('#' if get_at(cube_list, (x, y, z)) else '.', end = '')
            print()


def print_cube_4(cube_list):
    (minx, miny, minz, minw), (maxx, maxy, maxz, maxw) = reduce(get_limits, cube_list)
    for w in range(minw - 1, maxw + 2):
        for z in range(minz - 1, maxz + 2):
            print(f'{z=} {w=}')
            for y in range(miny - 1, maxy + 2):
                for x in range(minx - 1, maxx + 2):
                    print('#' if get_at(cube_list, (x, y, z, w)) else '.', end = '')
                print()


@timeit
def next_generation(cube_list):
    min_val, max_val = reduce(get_limits, cube_list)
    range_list = [range(min_v - 1, max_v + 2) for min_v, max_v in zip(min_val, max_val)]
    new_cube_set = set()
    for coord in product(*range_list):
        active = get_at(cube_list, coord)
        neighbour_range_list = [range(v - 1 , v + 2) for v in coord]
        neighbour_count = 0
        for neighbour_coord in product(*neighbour_range_list):
            if neighbour_coord == coord:
                continue
            if get_at(cube_list, neighbour_coord):
                neighbour_count += 1

        if active and neighbour_count == 2 or neighbour_count == 3:
            new_cube_set.add(coord)

        if not active and neighbour_count == 3:
            new_cube_set.add(coord)

    return tuple(new_cube_set)


def print_results(name, file_name, dimensions):
    cube_list = parse_data(file_name, dimensions)
    for _ in range(6):
        cube_list = next_generation(cube_list)
    print(f'{name} {len(cube_list)}')


def run():
    print_results(f'part1 test 112 =', 'data/day17_test.txt', 3)
    print_results(f'part1', 'data/day17.txt', 3)

    print_results(f'part2 test 848 =', 'data/day17_test.txt', 4)
    print_results(f'part2', 'data/day17.txt', 4)


if __name__ == "__main__":
    run()
