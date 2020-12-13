#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file, timeit


def parse_file(file_name):
    data = load_file(file_name)
    ts = int(data[0])
    bus_id_list = [(idx, int(val)) for idx, val in enumerate(data[1].split(',')) if val != 'x']
    return ts, bus_id_list


def print_results_1(name, file_name):
    ts, bus_id_list = parse_file(file_name)
    bus_id, wait = min(map(lambda bi: (bi[1] - (ts % bi[1]), bi[1]), bus_id_list))
    print(f'{name} {bus_id} * {wait} = {bus_id * wait}')


def find_step(ts, step, offset, bus_id):
    step_start = None
    while True:
        # print(f'{step_start=} {ts=} {offset=} {bus_id=} {step=}')
        if (ts + offset) % bus_id == 0:
            if step_start is None:
                step_start = ts
            else:
                return step_start, ts - step_start

        ts += step


@timeit
def find_first(bus_id_list):
    _, step = bus_id_list.pop(0)
    ts = 0
    for offset, bus_id in bus_id_list:
        ts, step = find_step(ts, step, offset, bus_id)

    return ts


def print_results_2(name, file_name):
    _, bus_id_list = parse_file(file_name)
    result = find_first(bus_id_list)
    print(f'{name} {result}')


def run():
    print_results_1('part1 test 295 =', 'data/day13_test.txt')
    print_results_1('part1', 'data/day13.txt')

    print_results_2('part2 test 1068781 =', 'data/day13_test.txt')
    print_results_2('part2', 'data/day13.txt')


if __name__ == "__main__":
    run()
