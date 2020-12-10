#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file


def parse_file(file_name):
    return sorted([int(adapter) for adapter in load_file(file_name)])


def walk_adapters_1(adapter_list):
    last_voltage = 0
    step_count = {}
    for adapter in adapter_list:
        step = adapter - last_voltage
        step_count.setdefault(step, 0)
        step_count[step] += 1
        last_voltage = adapter

    step_count[3] += 1
    return step_count


def print_results_1(name, adapter_list):
    results = walk_adapters_1(adapter_list)
    print(name, results, results[1] * results[3])


def run():
    test1_data = parse_file('data/day10_test1.txt')
    test2_data = parse_file('data/day10_test2.txt')
    data = parse_file('data/day10.txt')

    print_results_1('part1 test1', test1_data)
    print_results_1('part1 test2', test2_data)
    print_results_1('part1', data)


if __name__ == "__main__":
    run()
