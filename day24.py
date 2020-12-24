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
        x_offset, y_offset = COORD_OFFSET[tile_dir]
        x += x_offset
        y += y_offset

    return x, y


def get_coord_set(tile_dir_list):
    coord_set = set()
    for tile_dir_line in tile_dir_list:
        coord = get_coords(tile_dir_line)
        if coord in coord_set:
            coord_set.remove(coord)

        else:
            coord_set.add(coord)

    return coord_set


def get_limits(coord_set):
    return (
        min([c[0] for c in coord_set]) - 1,
        max([c[0] for c in coord_set]) + 1,
        min([c[1] for c in coord_set]) - 1,
        max([c[1] for c in coord_set]) + 1,
    )


def count_coord_neighbours(coord_set, coord):
    x, y = coord
    return sum([1 if (x + x_offset, y + y_offset) in coord_set else 0 for x_offset, y_offset in COORD_OFFSET.values()])


def next_coord_set(coord_set):
    min_x, max_x, min_y, max_y = get_limits(coord_set)

    new_coord_set = set()
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            test_coord = (x, y)
            coord_count = count_coord_neighbours(coord_set, test_coord)
            if test_coord in coord_set:
                if 1 <= coord_count <= 2:
                    new_coord_set.add(test_coord)

            else:
                if coord_count == 2:
                    new_coord_set.add(test_coord)

    return new_coord_set


def print_results_1(name, file_name):
    line_list = load_file(file_name)
    tile_dir_list = parse_input(line_list)
    coord_set = get_coord_set(tile_dir_list)

    print(f'{name} {len(coord_set)}')


def print_results_2(name, file_name):
    line_list = load_file(file_name)
    tile_dir_list = parse_input(line_list)
    coord_set = get_coord_set(tile_dir_list)
    for _ in range(100):
        coord_set = next_coord_set(coord_set)

    print(f'{name} {len(coord_set)}')


def run():
    print_results_1(f'part1 test 10 =', 'data/day24_test.txt')
    print_results_1(f'part1', 'data/day24.txt')

    print_results_2(f'part2 test 2208 =', 'data/day24_test.txt')
    print_results_2(f'part2', 'data/day24.txt')


if __name__ == "__main__":
    run()
