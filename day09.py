#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file


def parse_file(file_name):
    return map(int, load_file(file_name))


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


def attack_list_1(preamble_size, val_list):
    val_buffer = [next(val_list) for _ in range(preamble_size)]
    sum_set_buffer = [get_sum_set(val_buffer, idx) for idx in range(preamble_size)]

    for val in val_list:
        if not any([val in sum_set for sum_set in sum_set_buffer]):
            return val

        val_buffer.pop(0)
        val_buffer.append(val)

        sum_set_buffer.pop(0)
        sum_set_buffer.append(get_sum_set(val_buffer))


def attack_list_2(target_val, val_list):
    val_buffer = []
    test_buffer = []
    test_sum = 0
    try:
        while True:
            # ensure the value buffer is at least minimum length
            while len(val_buffer) < 2:
                val_buffer.append(next(val_list))

            # prime the empty test buffer
            if not test_buffer:
                test_buffer = val_buffer[:2]
                test_sum = test_buffer[0] + test_buffer[1]

            # print(test_sum, len(val_buffer), test_buffer)
            if test_sum == target_val:
                # target value found
                return min(test_buffer) + max(test_buffer)

            elif test_sum > target_val:
                # target value exceeded, reset test buffer and start from next element in the value buffer
                test_buffer = []
                test_sum = 0
                val_buffer.pop(0)

            else:
                # ensure value buffer is longer than test buffer
                test_buffer_len = len(test_buffer)
                if len(val_buffer) == test_buffer_len:
                    val_buffer.append(next(val_list))

                # add a value to the test buffer from the value buffer
                next_val = val_buffer[test_buffer_len]
                test_buffer.append(next_val)
                test_sum += next_val

    except StopIteration:
        pass


def run():
    print('part1 test', test_target_val := attack_list_1(5, parse_file('data/day09_test.txt')))
    print('part1', target_val := attack_list_1(25, parse_file('data/day09.txt')))

    print('part2 test', attack_list_2(test_target_val, parse_file('data/day09_test.txt')))
    print('part2', attack_list_2(target_val, parse_file('data/day09.txt')))


if __name__ == "__main__":
    run()
