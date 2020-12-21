#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file
from itertools import combinations, product
from collections import Counter
from math import prod, sqrt
import attr


@attr.s
class Tile:
    num = attr.ib(validator = attr.validators.instance_of(int))
    line_list = attr.ib(validator = attr.validators.instance_of(list))
    _border_id_list = attr.ib(init = False)

    @_border_id_list.default
    def _calculate_all_list_ids(self):
        tile_line_list = list(self.line_list)
        border_id_list = [
            self._calculate_line_ids(tile_line_list),
            self._calculate_line_ids(self.flip_vertically(tile_line_list)),
        ]
        for _ in range(3):
            tile_line_list = self.rotate_clockwise(tile_line_list)
            border_id_list.append(self._calculate_line_ids(tile_line_list))
            border_id_list.append(self._calculate_line_ids(self.flip_vertically(tile_line_list)))

        return border_id_list

    @staticmethod
    def _calculate_line_id(tile_line):
        tile_val = 0
        for v in tile_line:
            if v == '#':
                tile_val |= 1
            tile_val <<= 1
        return tile_val

    @staticmethod
    def _calculate_line_ids(tile_line_list):
        return [
            Tile._calculate_line_id(tile_line_list[0]),
            Tile._calculate_line_id(tile_line_list[-1]),
            Tile._calculate_line_id([v[0] for v in tile_line_list]),
            Tile._calculate_line_id([v[-1] for v in tile_line_list]),
        ]

    @staticmethod
    def flip_vertically(tile_line_list):
        return tile_line_list[::-1]

    @staticmethod
    def rotate_clockwise(tile_line_list):
        """
        Rotate tile 90 clockwise https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
        """

        return list(zip(*tile_line_list[::-1]))

    def check_connections(self, rhs):
        connection_list = []
        for idx_l, idx_r in product(range(8), repeat = 2):
            if self._border_id_list[idx_l][1] == rhs._border_id_list[idx_r][0]:
                connection_dir = 'above'
            elif self._border_id_list[idx_l][0] == rhs._border_id_list[idx_r][1]:
                connection_dir = 'below'
            elif self._border_id_list[idx_l][3] == rhs._border_id_list[idx_r][2]:
                connection_dir = 'left'
            elif self._border_id_list[idx_l][2] == rhs._border_id_list[idx_r][3]:
                connection_dir = 'right'
            else:
                continue

            connection_list.append((idx_l, idx_r, connection_dir))

        return connection_list

    def print(self):
        if self.num > 0:
            print(self.num)
        for tile_line in self.line_list:
            print(tile_line)
        print()


@attr.s
class TileGrid:
    tile_lookup = attr.ib(validator = attr.validators.instance_of(dict))

    _dimension = attr.ib(init = False)
    _connection_list = attr.ib(init = False)
    _connection_count = attr.ib(init = False)

    @property
    def dimension(self):
        return self._dimension

    @_dimension.default
    def _calculate_map_dimension(self):
        return int(sqrt(len(self.tile_lookup.keys())))

    @_connection_list.default
    def _check_connections(self):
        return [
            (tile_num_l, tile_num_r, tile_connections)
            for tile_num_l, tile_num_r in combinations(self.tile_lookup.keys(), 2)
            if (tile_connections := self.tile_lookup[tile_num_l].check_connections(self.tile_lookup[tile_num_r]))
        ]

    @property
    def connection_count(self):
        return self._connection_count

    @_connection_count.default
    def _count_connections(self):
        tile_connection_count = Counter()
        for tile_num_l, tile_num_r, *_ in self._connection_list:
            tile_connection_count.update((tile_num_l,))
            tile_connection_count.update((tile_num_r,))
        count_lookup = {}
        for num in tile_connection_count:
            count_set = count_lookup.setdefault(tile_connection_count[num], set())
            count_set.add(num)
        return count_lookup

    def _check_map_pos(self, map_list, used_tiles, x, y):
        return map_list

    def get_map(self):
        used_tiles = set(self.tile_lookup.keys())
        for corner_num in self.connection_count[2]:
            used_tiles.remove(corner_num)
            for pos in range(8):
                try:
                    map_list = [None] * self.dimension * self.dimension
                    map_list[0] = (corner_num, pos)
                    return self._check_map_pos(map_list, set(used_tiles), 1, 0)
                except ValueError:
                    pass


def parse_input(line_list):
    tile_lookup = {}
    tile_num = 0
    tile_list = []
    for line in line_list:
        if line.endswith(':'):
            tile_num = int(line[line.find(' ') + 1: -1])

        elif line:
            tile_list.append(line)

        else:
            tile_lookup[tile_num] = Tile(tile_num, tile_list)
            tile_list = []
    if tile_list:
        tile_lookup[tile_num] = Tile(tile_num, tile_list)

    return TileGrid(tile_lookup)


def print_results_1(name, file_name):
    line_list = load_file(file_name)
    tile_grid = parse_input(line_list)
    print(f'{name} {prod(tile_grid.connection_count[2])}')


def print_results_2(name, file_name):
    line_list = load_file(file_name)
    tile_grid = parse_input(line_list)
    result = tile_grid.get_map()
    print(f'{name} {result}')


def run():
    print_results_1(f'part1 test 20899048083289 =', 'data/day20_test.txt')
    print_results_1(f'part1', 'data/day20.txt')

    print_results_2(f'part2 test 273 =', 'data/day20_test.txt')
    print_results_2(f'part2', 'data/day20.txt')


if __name__ == "__main__":
    run()
