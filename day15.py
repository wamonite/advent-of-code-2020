#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import timeit


TEST_DATA = [
    ('0,3,6', 436, 175594),
    ('1,3,2', 1, 2578),
    ('2,1,3', 10, 3544142),
    ('1,2,3', 27, 261214),
    ('2,3,1', 78, 6895259),
    ('3,2,1', 438, 18),
    ('3,1,2', 1836, 362),
]
DATA = '0,1,4,13,15,12,16'
STEPS = (2020, 30000000)


def parse_data(input):
    return [int(v) for v in input.split(',')]


@timeit
def generate_numbers(start_list, steps):
    number_lookup = {starting_number: (idx, None) for idx, starting_number in enumerate(start_list)}
    number_spoken = start_list[-1]
    for step_count in range(len(start_list), steps):
        seen_at_1, seen_at_2 = number_lookup[number_spoken]
        number_spoken = 0 if seen_at_2 is None else seen_at_1 - seen_at_2
        number_spoken_last_seen = number_lookup[number_spoken][0] if number_spoken in number_lookup else None
        number_lookup[number_spoken] = (step_count, number_spoken_last_seen)
        # print(f'{step_count}: {number_spoken=} {seen_at_1=} {seen_at_2} {number_lookup=}')

    return number_spoken


def print_results(name, input, steps):
    data = parse_data(input)
    result = generate_numbers(data, steps)
    print(f'{name} {result}')


def run():
    for part in range(2):
        for test_input, *test_expected in TEST_DATA:
            print_results(f'part{part + 1} test {test_expected[part]} =', test_input, STEPS[part])
        print_results(f'part{part + 1}', DATA, STEPS[part])


if __name__ == "__main__":
    run()
