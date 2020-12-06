#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file


def parse_answers(lines):
    group_set = set()
    for line in lines:
        if line:
            group_set = group_set.union(set(line))

        else:
            yield group_set
            group_set = set()

    if group_set:
        yield group_set


def run():
    print('part1 test', sum(map(len, parse_answers(load_file('data/day6_test.txt')))))

    print('part1', sum(map(len, parse_answers(load_file('data/day6.txt')))))


if __name__ == "__main__":
    run()
