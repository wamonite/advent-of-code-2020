#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file


def decode(code, select):
    step = 1 << (len(code) - 1)
    val = 0
    for c in code:
        if c == select:
            val += step
        step >>= 1
    # print(code, val)

    return val


def parse_bp(bp):
    return decode(bp[:7], 'B'), decode(bp[7:10], 'R')


def calculate_seat(row, col):
    return row * 8 + col


def find_seat(sorted_seat_list):
    for (seat, expected) in zip(sorted_seat_list, range(sorted_seat_list[0], sorted_seat_list[-1] + 1)):
        if seat != expected:
            return expected


def run():
    print('part1 test', max(map(lambda v: calculate_seat(*v), map(parse_bp, load_file('data/day5_test.txt')))))

    seat_list = sorted(map(lambda v: calculate_seat(*v), map(parse_bp, load_file('data/day5.txt'))))
    print('part1', seat_list[-1])
    print('part2', find_seat(seat_list))


if __name__ == "__main__":
    run()
