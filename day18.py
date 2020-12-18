#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file
from operator import add, mul

OPERATOR_LOOKUP = {
    '+': add,
    '*': mul,
}


def parse_line(line):
    tokens = line.split(' ')
    token_list = []
    token_stack = [token_list]

    while tokens:
        token = tokens.pop(0)
        next_token_list = None

        bracket_before = token.split('(')
        for _ in range(len(bracket_before) - 1):
            token_stack.append([])
            token_list.append(token_stack[-1])
            token_list = token_stack[-1]

            token = bracket_before[-1]

        bracket_after = token.split(')')
        for _ in range(len(bracket_after) - 1):
            token_stack.pop()
            next_token_list = token_stack[-1]

            token = bracket_after[0]

        if token not in OPERATOR_LOOKUP.keys():
            token = int(token)

        token_list.append(token)

        if next_token_list:
            token_list = next_token_list

    return token_list


def calculate_line_1(token_list):
    if isinstance(token_list, int):
        return token_list

    if len(token_list) >= 3:
        op = token_list[-2]
        op_func = OPERATOR_LOOKUP[op]
        return op_func(calculate_line_1(token_list[:-2]), calculate_line_1(token_list[-1]))

    return calculate_line_1(token_list[0])


def calculate_line_2(token_list):
    if isinstance(token_list, int):
        return token_list

    try:
        token_found = token_list.index('*')
        return calculate_line_2(token_list[:token_found]) * calculate_line_2(token_list[token_found + 1:])
    except ValueError:
        pass

    try:
        token_found = token_list.index('+')
        return calculate_line_2(token_list[:token_found]) + calculate_line_2(token_list[token_found + 1:])
    except ValueError:
        pass

    return calculate_line_2(token_list[0])


def print_results(name, file_name, calc_func):
    line_list = load_file(file_name)
    line_data = [parse_line(line) for line in line_list]
    line_results = [calc_func(line) for line in line_data]
    print(f'{name} {sum(line_results)}')


def run():
    print_results(f'part1 test 26386 =', 'data/day18_test.txt', calculate_line_1)
    print_results(f'part1', 'data/day18.txt', calculate_line_1)

    print_results(f'part2 test 693942 =', 'data/day18_test.txt', calculate_line_2)
    print_results(f'part2', 'data/day18.txt', calculate_line_2)


if __name__ == "__main__":
    run()
