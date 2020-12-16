#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file
import re
from math import prod


def parse_data(file_name):
    line_list = load_file(file_name)
    field_lookup = {}
    ticket_list = []
    for line in line_list:
        if match := re.match('^([^:]+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)', line):
            field_name, *field_values = match.groups()
            field_lookup[field_name] = [int(v) for v in field_values]

        elif line and line.find(':') == -1:
            ticket_list.append([int(v) for v in line.split(',')])

    return field_lookup, ticket_list


def find_ticket_error(field_lookup, ticket):
    for field_value in ticket:
        error_list = [(min1 <= field_value <= max1 or min2 <= field_value <= max2) for min1, max1, min2, max2 in field_lookup.values()]
        if not any(error_list):
            return field_value

    return None


def print_results_1(name, file_name):
    field_lookup, ticket_list = parse_data(file_name)
    ticket_error_list = [find_ticket_error(field_lookup, ticket) for ticket in ticket_list[1:]]
    result = sum([v for v in ticket_error_list if v is not None])
    print(f'{name} {result}')


def get_field_name_options(field_lookup, ticket_list):
    """
    For each value, find a set of valid field names
    """

    field_name_set = set(field_lookup.keys())
    field_name_options_list = []
    for field_idx in range(len(field_name_set)):
        current_set = set(field_name_set)
        for ticket in ticket_list:
            field_value = ticket[field_idx]
            for field_name in field_name_set:
                min1, max1, min2, max2 = field_lookup[field_name]
                if not(min1 <= field_value <= max1 or min2 <= field_value <= max2):
                    current_set.discard(field_name)

        field_name_options_list.append(current_set)

    return field_name_options_list


def get_field_name_order(field_option_list):
    """
    By process of elimination, determine the only possible name for each field
    """

    field_name_list = [None] * len(field_option_list)
    while not all(field_name_list):
        for idx, field_option in enumerate(field_option_list):
            if len(field_option) == 1:
                found_name = field_option.pop()
                field_name_list[idx] = found_name
                for field_set in field_option_list:
                    field_set.discard(found_name)
                break

    return field_name_list


def print_results_2(name, file_name):
    field_lookup, ticket_list = parse_data(file_name)
    valid_ticket_list = [ticket for ticket in ticket_list[1:] if find_ticket_error(field_lookup, ticket) is None]
    field_name_options_list = get_field_name_options(field_lookup, valid_ticket_list)
    field_name_order = get_field_name_order(field_name_options_list)
    result = prod([field_value for field_name, field_value in zip(field_name_order, ticket_list[0]) if field_name.startswith('departure')])
    print(f'{name} {result}')


def run():
    print_results_1(f'part1 test 71 =', 'data/day16_test1.txt')
    print_results_1(f'part1', 'data/day16.txt')

    print_results_2(f'part2', 'data/day16.txt')


if __name__ == "__main__":
    run()
