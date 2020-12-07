#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file


def parse_bag_list(bag_contents_str):
    if bag_contents_str == 'no other bags.':
        return {}

    bag_info_str_list = bag_contents_str.split(', ')
    bag_name_lookup = {}
    for bag_info_str in bag_info_str_list:
        count, *name_list = bag_info_str.split(' ')
        bag_name = ' '.join(name_list[:-1])
        bag_name_lookup[bag_name] = int(count)

    return bag_name_lookup


def parse_rules(lines):
    for line in lines:
        bag_name, bag_contents_str = line.split(' bags contain ')
        bag_info_list = parse_bag_list(bag_contents_str)
        yield bag_name, bag_info_list


def find_bags(bag_lookup, search_name):
    found_name_set = {name for name, contents in bag_lookup.items() if search_name in contents}
    for found_name in list(found_name_set):
        found_name_set |= find_bags(bag_lookup, found_name)

    return found_name_set


def count_bags(bag_lookup, search_name):
    found_sum = 0
    for found_name, found_bags in bag_lookup[search_name].items():
        found_sum += found_bags
        found_count = count_bags(bag_lookup, found_name)
        # print(f'adding {found_name}: {found_bags} * {found_count}')
        found_sum += found_bags * found_count

    return found_sum


def run():
    test_data = dict(parse_rules(load_file('data/day07_test.txt')))
    data = dict(parse_rules(load_file('data/day07.txt')))

    print('part1 test', len(find_bags(test_data, 'shiny gold')))
    print('part1', len(find_bags(data, 'shiny gold')))

    print('part2 test', count_bags(test_data, 'shiny gold'))
    print('part2', count_bags(data, 'shiny gold'))


if __name__ == "__main__":
    run()
