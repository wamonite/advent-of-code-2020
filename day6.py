#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file


def parse_answers(lines):
    answer_set_list = []
    for line in lines:
        if line:
            answer_set_list.append(set(line))

        else:
            yield answer_set_list
            answer_set_list = []

    if answer_set_list:
        yield answer_set_list


def count_answers_1(answer_set_list):
    all_answer_set = set()
    for answer_set in answer_set_list:
        all_answer_set |= answer_set

    return len(all_answer_set)


def count_answers_2(answer_set_list):
    all_answer_set = set()
    invalid_answer_set = set()
    for answer_set in answer_set_list:
        answer_set -= invalid_answer_set
        if all_answer_set or invalid_answer_set:
            all_answer_set &= answer_set
        else:
            all_answer_set = answer_set
        invalid_answer_set |= answer_set - all_answer_set

    return len(all_answer_set)


def run():
    test_data = load_file('data/day6_test.txt')
    data = load_file('data/day6.txt')

    print('part1 test', sum(map(count_answers_1, parse_answers(test_data))))
    print('part1', sum(map(count_answers_1, parse_answers(data))))

    print('part2 test', sum(map(count_answers_2, parse_answers(test_data))))
    print('part2', sum(map(count_answers_2, parse_answers(data))))


if __name__ == "__main__":
    run()
