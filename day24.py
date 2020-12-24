#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file

COORD_OFFSET = {
    'e': (1, 0),
    'ne': (0, 1),
    'se': (1, -1),
    'w': (-1, 0),
    'nw': (-1, 1),
    'sw': (0, -1),
}


def parse_input(line_list):
    tile_dir_list = []
    for line in line_list:
        tile_dir_line = []
        while line:
            c = line[0]
            line = line[1:]
            if c in ['e', 'w']:
                tile_dir_line.append(c)
            else:
                tile_dir_line.append(c + line[0])
                line = line[1:]

        tile_dir_list.append(tile_dir_line)

    return tile_dir_list


def get_coords(tile_dir_line):
    x = 0
    y = 0
    for tile_dir in tile_dir_line:
        coord_offset = COORD_OFFSET[tile_dir]
        x += coord_offset[0]
        y += coord_offset[1]

    return x, y


def print_results(name, file_name):
    line_list = load_file(file_name)
    tile_dir_list = parse_input(line_list)
    coord_set = set()
    for tile_dir_line in tile_dir_list:
        coord = get_coords(tile_dir_line)
        if coord in coord_set:
            coord_set.remove(coord)
        else:
            coord_set.add(coord)

    print(f'{name} {len(coord_set)}')


def run():
    print_results(f'part1 test 10 =', 'data/day24_test.txt')
    print_results(f'part1', 'data/day24.txt')


if __name__ == "__main__":
    run()
