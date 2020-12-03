#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


def run():
    with open('data/day3.txt') as file_object:
        map_list = list(map(lambda s: s.strip(), file_object.readlines()))

    print(sum(map(lambda c: 1 if c == '#' else 0, step_x(step_y(map_list), 3))))


if __name__ == "__main__":
    run()
