#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file
from functools import reduce


def parse_data(file_name):
    line_list = load_file(file_name)
    z = 0
    cube_list = []
    for y, line in enumerate(line_list):
        for x, c in enumerate(line):
            if c == '#':
                cube_list.append((x, y, z))

    return tuple(cube_list)


def get_limits(limits, coord):
    try:
        minx, miny, minz, maxx, maxy, maxz = limits

    except ValueError:
        minx, miny, minz = limits
        maxx, maxy, maxz = limits

    x, y, z = coord
    return (
        x if x < minx else minx,
        y if y < miny else miny,
        z if z < minz else minz,
        x if x > maxx else maxx,
        y if y > maxy else maxy,
        z if z > maxz else maxz,
    )


# adding @lru_cache actually makes this slower
def get_at(cube_list, coord):
    return coord in cube_list


def print_cube(cube_list):
    minx, miny, minz, maxx, maxy, maxz = reduce(get_limits, cube_list)
    for z in range(minz - 1, maxz + 2):
        print(f'{z=}')
        for y in range(miny - 1, maxy + 2):
            for x in range(minx - 1, maxx + 2):
                print('#' if get_at(cube_list, (x, y, z)) else '.', end = '')
            print()


def next_generation(cube_list):
    minx, miny, minz, maxx, maxy, maxz = reduce(get_limits, cube_list)
    new_cube_set = set()
    for z in range(minz - 1, maxz + 2):
        for y in range(miny - 1, maxy + 2):
            for x in range(minx - 1, maxx + 2):
                active = get_at(cube_list, (x, y, z))
                neighbour_count = 0
                for zd in range(-1, 2):
                    for yd in range(-1, 2):
                        for xd in range(-1, 2):
                            if xd == 0 and yd == 0 and zd == 0:
                                continue
                            if get_at(cube_list, (x + xd, y + yd, z + zd)):
                                neighbour_count += 1

                if active and neighbour_count == 2 or neighbour_count == 3:
                    new_cube_set.add((x, y, z))

                if not active and neighbour_count == 3:
                    new_cube_set.add((x, y, z))

    return tuple(new_cube_set)


def print_results_1(name, file_name):
    cube_list = parse_data(file_name)
    for _ in range(6):
        cube_list = next_generation(cube_list)
    print(f'{name} {len(cube_list)}')


def run():
    print_results_1(f'part1 test 112 =', 'data/day17_test.txt')
    print_results_1(f'part1', 'data/day17.txt')


if __name__ == "__main__":
    run()
