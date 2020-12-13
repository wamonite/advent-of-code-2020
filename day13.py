#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file


def parse_file(file_name):
    data = load_file(file_name)
    ts = int(data[0])
    bus_id_list = [int(v) for v in data[1].split(',') if v != 'x']
    return ts, bus_id_list


def print_results_1(name, file_name):
    ts, bus_id_list = parse_file(file_name)
    bus_id, wait = min(map(lambda bi: (bi - (ts % bi), bi), bus_id_list))
    print(f'{name} {bus_id} * {wait} = {bus_id * wait}')


def run():
    print_results_1('part1 test 295 = ', 'data/day13_test.txt')
    print_results_1('part1', 'data/day13.txt')


if __name__ == "__main__":
    run()
