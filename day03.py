#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import prod


def step_y(map_list, step = 1):
    assert(step > 0)
    for idx in range(0, len(map_list), step):
        yield map_list[idx]


def step_x(map_list, step = 0):
    pos = 0
    for map_line in map_list:
        yield map_line[pos]

        pos += step
        pos %= len(map_line)


def count_tree(char):
    return 1 if char == '#' else 0


def count_map(map_list, sx = 0, sy = 1):
    return sum(map(count_tree, step_x(step_y(map_list, sy), sx)))


def run():
    with open('data/day03.txt') as file_object:
        map_list = list(map(lambda s: s.strip(), file_object.readlines()))

    print(count_map(map_list, 3))

    print(prod([
        count_map(map_list, 1, 1),
        count_map(map_list, 3, 1),
        count_map(map_list, 5, 1),
        count_map(map_list, 7, 1),
        count_map(map_list, 1, 2),
    ]))


if __name__ == "__main__":
    run()
