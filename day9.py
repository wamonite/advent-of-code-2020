#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file


def get_sum_set(val_list, target_idx = -1):
    sum_set = set()
    target_val = val_list[target_idx]
    for idx, val in enumerate(val_list):
        if idx == target_idx:
            continue

        if val == target_val:
            continue

        sum_set.add(val + target_val)

    return sum_set


def attack_list(preamble_size):
    def attack_list_inner(val_list):
        val_buffer = [next(val_list) for _ in range(preamble_size)]
        sum_set_buffer = [get_sum_set(val_buffer, idx) for idx in range(preamble_size)]

        for val in val_list:
            if not any([val in sum_set for sum_set in sum_set_buffer]):
                return val

            val_buffer.pop(0)
            val_buffer.append(val)

            sum_set_buffer.pop(0)
            sum_set_buffer.append(get_sum_set(val_buffer))

    return attack_list_inner


def run():
    test_data = map(int, load_file('data/day9_test.txt'))
    data = map(int, load_file('data/day9.txt'))

    print('part1 test', attack_list(5)(test_data))
    print('part1', attack_list(25)(data))


if __name__ == "__main__":
    run()
