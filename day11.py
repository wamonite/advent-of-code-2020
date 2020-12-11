#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file
from collections import Counter
from hashlib import sha256


def get_cell(grid_list, x, y):
    if y < 0 or y >= len(grid_list):
        return '.'
    if x < 0 or x >= len(grid_list[0]):
        return '.'
    return grid_list[y][x]


def grid_next_1(grid_list):
    new_grid_list = []
    for y in range(len(grid_list)):
        grid_line = ''
        for x in range(len(grid_list[0])):
            cell_val = get_cell(grid_list, x, y)
            if cell_val != '.':
                cell_count = Counter()
                cell_count.update(get_cell(grid_list, x - 1, y - 1))
                cell_count.update(get_cell(grid_list, x, y - 1))
                cell_count.update(get_cell(grid_list, x + 1, y - 1))
                cell_count.update(get_cell(grid_list, x - 1, y))
                cell_count.update(get_cell(grid_list, x + 1, y))
                cell_count.update(get_cell(grid_list, x - 1, y + 1))
                cell_count.update(get_cell(grid_list, x, y + 1))
                cell_count.update(get_cell(grid_list, x + 1, y + 1))

                if cell_val == 'L' and cell_count.get('#', 0) == 0:
                    cell_val = '#'
                elif cell_val == '#' and cell_count.get('#', 0) >= 4:
                    cell_val = 'L'

            grid_line += cell_val
        new_grid_list.append(grid_line)

    return new_grid_list


def walk_grid(grid_list, x, y, xd, yd):
    xt = x + xd
    yt = y + yd
    while 0 <= xt < len(grid_list[0]) and 0 <= yt < len(grid_list):
        cell_val = get_cell(grid_list, xt, yt)
        # print(f'{x=} {y=} {xd=} {yd=} {xt=} {yt=} {cell_val=}')
        if cell_val != '.':
            return cell_val
        xt += xd
        yt += yd

    return '.'


def grid_next_2(grid_list):
    new_grid_list = []
    for y in range(len(grid_list)):
        grid_line = ''
        for x in range(len(grid_list[0])):
            cell_val = get_cell(grid_list, x, y)
            if cell_val != '.':
                cell_count = Counter()
                cell_count.update(walk_grid(grid_list, x, y, -1, -1))
                cell_count.update(walk_grid(grid_list, x, y, 0, -1))
                cell_count.update(walk_grid(grid_list, x, y, 1, -1))
                cell_count.update(walk_grid(grid_list, x, y, -1, 0))
                cell_count.update(walk_grid(grid_list, x, y, 1, 0))
                cell_count.update(walk_grid(grid_list, x, y, -1, 1))
                cell_count.update(walk_grid(grid_list, x, y, 0, 1))
                cell_count.update(walk_grid(grid_list, x, y, 1, 1))

                if cell_val == 'L' and cell_count.get('#', 0) == 0:
                    cell_val = '#'
                elif cell_val == '#' and cell_count.get('#', 0) >= 5:
                    cell_val = 'L'

            grid_line += cell_val
        new_grid_list.append(grid_line)

    return new_grid_list


def grid_crc(grid_list):
    m = sha256()
    for grid_line in grid_list:
        m.update(grid_line.encode('utf-8'))
    return m.hexdigest()


def grid_print(grid_list):
    for grid_line in grid_list:
        print(grid_line)


def grid_count(grid_list):
    cell_count = Counter()
    for grid_line in grid_list:
        for cell_val in grid_line:
            cell_count.update(cell_val)

    return cell_count


def iterate_grid(grid_list, grid_next_func):
    crc_val = 0
    while True:
        grid_list = grid_next_func(grid_list)
        # grid_print(grid_tuple)
        new_crc_val = grid_crc(grid_list)
        # print(new_crc_val)

        if crc_val == new_crc_val:
            break

        crc_val = new_crc_val

    return grid_count(grid_list)


def run():
    test_data = load_file('data/day11_test.txt')
    data = load_file('data/day11.txt')

    result = iterate_grid(test_data, grid_next_1)
    print('part1 test', result.get('#', 0))

    result = iterate_grid(data, grid_next_1)
    print('part1', result.get('#', 0))

    result = iterate_grid(test_data, grid_next_2)
    print('part2 test', result.get('#', 0))

    result = iterate_grid(data, grid_next_2)
    print('part2', result.get('#', 0))


if __name__ == "__main__":
    run()
