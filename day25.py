#!/usr/bin/env python
# -*- coding: utf-8 -*-

TEST_INPUT = """5764801
17807724"""
PUZZLE_INPUT = """16915772
18447943"""


def parse_input(input_str):
    return list(map(int, input_str.splitlines()))


def transform(subject_number):
    val = 1
    while True:
        val *= subject_number
        val %= 20201227
        yield val


def transform_loop(subject_number, loop_size):
    val = subject_number
    transformer = transform(subject_number)
    for _ in range(loop_size):
        val = next(transformer)
    return val


def find_loop_size(subject_number, target_value):
    for loop_val, result in enumerate(transform(subject_number), 1):
        if result == target_value:
            return loop_val


def get_encryption_key(card_public_key, door_public_key):
    initial_value = 7
    card_loop_size = find_loop_size(initial_value, card_public_key)
    door_loop_size = find_loop_size(initial_value, door_public_key)
    card_encryption_key = transform_loop(door_public_key, card_loop_size)
    door_encryption_key = transform_loop(card_public_key, door_loop_size)
    assert(card_encryption_key == door_encryption_key)
    return card_encryption_key


def print_results_1(name, input_str):
    encryption_key = get_encryption_key(*parse_input(input_str))
    print(f'{name} {encryption_key}')


def run():
    print_results_1(f'part1 test 14897079 =', TEST_INPUT)
    print_results_1(f'part1', PUZZLE_INPUT)


if __name__ == "__main__":
    run()
