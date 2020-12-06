#!/usr/bin/env python
# -*- coding: utf-8 -*-

def count_answers_1(answer_set_list):
    return len(set.union(*answer_set_list))


def count_answers_2(answer_set_list):
    # oh dear, my first implementation of this was soooo complicated
    return len(set.intersection(*answer_set_list))


def load_and_parse(file_name):
    with open(file_name) as file_object:
        return [[set(v) for v in s.splitlines()] for s in file_object.read().strip().split('\n\n')]


def run():
    test_data = load_and_parse('data/day06_test.txt')
    data = load_and_parse('data/day06.txt')

    print('part1 test', sum(map(count_answers_1, test_data)))
    print('part1', sum(map(count_answers_1, data)))

    print('part2 test', sum(map(count_answers_2, test_data)))
    print('part2', sum(map(count_answers_2, data)))


if __name__ == "__main__":
    run()
