#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file, timeitc


def parse_bp(bp):
    val = 0
    for c in bp:
        val <<= 1
        if c in ('B', 'R'):
            val |= 1
    # print(bp, val)

    return val


def find_seat(sorted_seat_list):
    for (seat, expected) in zip(sorted_seat_list, range(sorted_seat_list[0], sorted_seat_list[-1] + 1)):
        if seat != expected:
            return expected


def run():
    print('part1 test', max(map(parse_bp, load_file('data/day05_test.txt'))))

    with timeitc():
        seat_list = sorted(map(parse_bp, load_file('data/day05.txt')))
    print('part1', seat_list[-1])
    print('part2', find_seat(seat_list))


if __name__ == "__main__":
    run()
