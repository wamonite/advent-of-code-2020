#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file
from itertools import tee
from collections import Counter
from functools import lru_cache


def parse_file(file_name):
    return sorted([int(adapter) for adapter in load_file(file_name)])


# https://stackoverflow.com/questions/5764782/iterate-through-pairs-of-items-in-a-python-list
def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def walk_adapters_1(adapter_list):
    full_list = [0] + adapter_list + [adapter_list[-1] + 3]
    return Counter([adapter - adapter_last for adapter_last, adapter in pairwise(full_list)])


def print_results_1(name, adapter_list):
    results = walk_adapters_1(adapter_list)
    print(name, results, results[1] * results[3])


# takes insanely long without caching
@lru_cache
def walk_adapters_2(adapter_list, joltage = 0):
    if joltage == adapter_list[-1]:
        return 1

    usable_list = [adapter for adapter in adapter_list if joltage < adapter <= joltage + 3]
    return sum([walk_adapters_2(adapter_list, usable) for usable in usable_list])


def run():
    test1_data = parse_file('data/day10_test1.txt')
    test2_data = parse_file('data/day10_test2.txt')
    data = parse_file('data/day10.txt')

    print_results_1('part1 test1', test1_data)
    print_results_1('part1 test2', test2_data)
    print_results_1('part1', data)

    # convert to tuple so lru_cache can hash it
    print('part2 test1', walk_adapters_2(tuple(test1_data)))
    print('part2 test2', walk_adapters_2(tuple(test2_data)))
    print('part2', walk_adapters_2(tuple(data)))


if __name__ == "__main__":
    run()
