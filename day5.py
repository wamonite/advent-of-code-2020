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


def run():
    print(max(map(lambda v: calculate_seat(*v), map(parse_bp, load_file('data/day5_test.txt')))))
    print(max(map(lambda v: calculate_seat(*v), map(parse_bp, load_file('data/day5.txt')))))


if __name__ == "__main__":
    run()
