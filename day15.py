#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import timeit


TEST_DATA = [
    ('0,3,6', 436),
    ('1,3,2', 1),
    ('2,1,3', 10),
    ('1,2,3', 27),
    ('2,3,1', 78),
    ('3,2,1', 438),
    ('3,1,2', 1836),
]
DATA = '0,1,4,13,15,12,16'
DEFAULT_STEPS = 2020


def parse_data(input):
    return [int(v) for v in input.split(',')]


@timeit
def generate_numbers(start_list, steps):
    number_lookup = {starting_number: (idx + 1, None) for idx, starting_number in enumerate(start_list)}
    number_spoken = start_list[-1]
    for step_count in range(len(start_list) + 1, steps + 1):
        seen_at_1, seen_at_2 = number_lookup[number_spoken]
        number_spoken = 0 if seen_at_2 is None else seen_at_1 - seen_at_2
        number_spoken_last_seen = number_lookup[number_spoken][0] if number_spoken in number_lookup else None
        number_lookup[number_spoken] = (step_count, number_spoken_last_seen)
        # print(f'{step_count}: {number_spoken=} {seen_at_1=} {seen_at_2} {number_lookup=}')

    return number_spoken


def print_results_1(name, input, steps = DEFAULT_STEPS):
    data = parse_data(input)
    result = generate_numbers(data, steps)
    print(f'{name} {result}')


def run():
    for test_input, test_expected in TEST_DATA:
        print_results_1(f'part1 test {test_expected} =', test_input)
    print_results_1(f'part1', DATA)


if __name__ == "__main__":
    run()
