#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file
from itertools import combinations, product
from collections import Counter
from math import prod


def parse_input(line_list):
    tile_lookup = {}
    tile_num = 0
    tile_list = []
    for line in line_list:
        if line.endswith(':'):
            tile_num = int(line[line.find(' ') + 1: -1])

        elif line:
            tile_list.append([1 if c == '#' else 0 for c in line])

        else:
            tile_lookup[tile_num] = tile_list
            tile_list = []
    if tile_list:
        tile_lookup[tile_num] = tile_list

    return tile_lookup


def print_tile(tile_line_list, tile_num = None):
    if tile_num is not None:
        print(tile_num)
    for tile_line in tile_line_list:
        print(''.join(['#' if v else '.' for v in tile_line]))
    print()


def rotate_tile(tile_line_list):
    """
    Rotate tile 90 clockwise https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
    """

    return list(zip(*tile_line_list[::-1]))


def flip_tile_vertical(tile_line_list):
    return tile_line_list[::-1]


def get_line_id(tile_line):
    tile_val = 0
    for v in tile_line:
        if v:
            tile_val |= 1
        tile_val <<= 1
    return tile_val


def get_tile_id(tile_line_list):
    return [
        get_line_id(tile_line_list[0]),
        get_line_id(tile_line_list[-1]),
        get_line_id([v[0] for v in tile_line_list]),
        get_line_id([v[-1] for v in tile_line_list]),
    ]


def get_tile_id_lookup(tile_lookup):
    tile_id_lookup = {}
    for tile_num, tile_line_list in tile_lookup.items():
        tile_id_list = [
            get_tile_id(tile_line_list),
            get_tile_id(flip_tile_vertical(tile_line_list)),
        ]
        for _ in range(3):
            tile_line_list = rotate_tile(tile_line_list)
            tile_id_list.append(get_tile_id(tile_line_list))
            tile_id_list.append(get_tile_id(flip_tile_vertical(tile_line_list)))
        tile_id_lookup[tile_num] = tile_id_list
    return tile_id_lookup


def match_tiles(tile_id_list_l, tile_id_list_r):
    return [
        (idx_l, idx_r, tile_dir)
        for idx_l, idx_r in product(range(len(tile_id_list_l)), repeat = 2)
        if (
            tile_dir :=
            ('above' if tile_id_list_l[idx_l][1] == tile_id_list_r[idx_r][0] else '') +
            ('below' if tile_id_list_l[idx_l][0] == tile_id_list_r[idx_r][1] else '') +
            ('left' if tile_id_list_l[idx_l][3] == tile_id_list_r[idx_r][2] else '') +
            ('right' if tile_id_list_l[idx_l][2] == tile_id_list_r[idx_r][3] else '')
        )
    ]


def get_tile_match_list(tile_id_lookup):
    return [
        (tile_num_l, tile_num_r, tile_matches)
        for tile_num_l, tile_num_r in combinations(tile_id_lookup.keys(), 2)
        if (tile_matches := match_tiles(tile_id_lookup[tile_num_l], tile_id_lookup[tile_num_r]))
    ]


def find_corner_tiles(tile_match_list):
    tile_count = Counter()
    for tile_num_l, tile_num_r, *_ in tile_match_list:
        tile_count.update((tile_num_l,))
        tile_count.update((tile_num_r,))
    return [tile_num for tile_num in tile_count if tile_count[tile_num] == 2]


def print_results(name, file_name):
    line_list = load_file(file_name)
    tile_lookup = parse_input(line_list)
    tile_id_lookup = get_tile_id_lookup(tile_lookup)
    tile_match_list = get_tile_match_list(tile_id_lookup)
    tile_corner_list = find_corner_tiles(tile_match_list)
    print(f'{name} {prod(tile_corner_list)}')


def run():
    print_results(f'part1 test 20899048083289 =', 'data/day20_test.txt')
    print_results(f'part1', 'data/day20.txt')


if __name__ == "__main__":
    run()
