#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import timeit
from itertools import combinations
from math import prod


def print_result(method):
    def print_result_inner(*args, **kwargs):
        result = method(*args, **kwargs)
        print(f'{" + ".join(map(str, result))} = {sum(result)}')
        print(f'{" * ".join(map(str, result))} = {prod(result)}')

    return print_result_inner


@print_result
@timeit
def find_sum_2(value_list, target_sum):
    list_length = len(value_list)

    for x in range(list_length):
        if value_list[x] >= target_sum:
            continue

        for y in range(list_length):
            if x == y:
                continue

            if value_list[x] + value_list[y] == target_sum:
                return value_list[x], value_list[y]


@print_result
@timeit
def find_sum_3(value_list, target_sum):
    list_length = len(value_list)

    for x in range(list_length):
        if x >= target_sum:
            continue

        for y in range(list_length):
            if x == y:
                continue

            if value_list[x] + value_list[y] >= target_sum:
                continue

            for z in range(list_length):
                if x == z or y == z:
                    continue

                if value_list[x] + value_list[y] + value_list[z] == target_sum:
                    return value_list[x], value_list[y], value_list[z]


@print_result
@timeit
def find_sum(value_list, target_sum, terms = 2):
    combination_list = combinations(value_list, r = terms)
    for combination in combination_list:
        if sum(combination) == target_sum:
            return combination


def run():
    expense_list = []
    with open('data/day01.txt') as file_object:
        for line in file_object.readlines():
            line = line.strip()
            expense_list.append(int(line))

    expense_list.sort()

    find_sum_2(expense_list, 2020)
    find_sum_3(expense_list, 2020)

    find_sum(expense_list, 2020, 2)
    find_sum(expense_list, 2020, 3)


if __name__ == "__main__":
    run()
