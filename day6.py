#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file


def parse_answers_1(lines):
    answer_set = set()
    for line in lines:
        if line:
            answer_set = answer_set | set(line)

        else:
            yield len(answer_set)
            answer_set = set()

    if answer_set:
        yield len(answer_set)


def parse_answers_2(lines):
    all_answer_set = set()
    invalid_answer_set = set()
    for line in lines:
        if line:
            answer_set = set(line) - invalid_answer_set
            if all_answer_set or invalid_answer_set:
                all_answer_set &= answer_set
            else:
                all_answer_set = answer_set
            invalid_answer_set |= answer_set - all_answer_set

        else:
            yield len(all_answer_set)
            all_answer_set = set()
            invalid_answer_set = set()

    if all_answer_set:
        yield len(all_answer_set)


def run():
    print('part1 test', sum(parse_answers_1(load_file('data/day6_test.txt'))))
    print('part1', sum(parse_answers_1(load_file('data/day6.txt'))))

    print('part2 test', sum(parse_answers_2(load_file('data/day6_test.txt'))))
    print('part2', sum(parse_answers_2(load_file('data/day6.txt'))))


if __name__ == "__main__":
    run()
