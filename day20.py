#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file
from itertools import combinations, product
from collections import Counter
from math import prod, sqrt
import attr


POS_MAX = 8
MONSTER_IMAGE = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """


@attr.s
class Tile:
    num = attr.ib(validator = attr.validators.instance_of(int))
    image_lines = attr.ib(validator = attr.validators.instance_of(list))
    border_value_list = attr.ib(init = False)

    def __attrs_post_init__(self):
        image_lines = list(self.image_lines)
        self.border_value_list = [
            self._calculate_border_values(image_lines),
            self._calculate_border_values(self.flip_vertically(image_lines)),
        ]
        for _ in range(3):
            image_lines = self.rotate_clockwise(image_lines)
            self.border_value_list.append(self._calculate_border_values(image_lines))
            self.border_value_list.append(self._calculate_border_values(self.flip_vertically(image_lines)))

    @staticmethod
    def _calculate_border_values(image_lines):
        return [
            get_line_as_int(image_lines[0]),
            get_line_as_int(image_lines[-1]),
            get_line_as_int([v[0] for v in image_lines]),
            get_line_as_int([v[-1] for v in image_lines]),
        ]

    @staticmethod
    def flip_vertically(image_lines):
        return image_lines[::-1]

    @staticmethod
    def rotate_clockwise(image_lines):
        """
        Rotate tile 90 clockwise https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
        """

        return [''.join(t) for t in zip(*image_lines[::-1])]

    def check_connections(self, rhs):
        connection_list = []
        for idx_l, idx_r in product(range(POS_MAX), repeat = 2):
            if self.border_value_list[idx_l][1] == rhs.border_value_list[idx_r][0]:
                connection_dir = 'above'
            elif self.border_value_list[idx_l][0] == rhs.border_value_list[idx_r][1]:
                connection_dir = 'below'
            elif self.border_value_list[idx_l][3] == rhs.border_value_list[idx_r][2]:
                connection_dir = 'left'
            elif self.border_value_list[idx_l][2] == rhs.border_value_list[idx_r][3]:
                connection_dir = 'right'
            else:
                continue

            connection_list.append((idx_l, idx_r, connection_dir))

        return connection_list

    def get_tile(self, pos):
        image_lines = list(self.image_lines)
        for current_pos in range(0, POS_MAX, 2):
            if pos == current_pos:
                return image_lines
            elif pos == current_pos + 1:
                return self.flip_vertically(image_lines)
            image_lines = self.rotate_clockwise(image_lines)

    def get_borderless_tile(self, pos):
        return [line[1:-1] for line in self.get_tile(pos)][1:-1]

    def print(self):
        if self.num > 0:
            print(self.num)
        for tile_line in self.image_lines:
            print(tile_line)
        print()


@attr.s
class TileGrid:
    tile_lookup = attr.ib(validator = attr.validators.instance_of(dict))

    _dimension = attr.ib(init = False)
    _connection_list = attr.ib(init = False)
    _connection_count = attr.ib(init = False)

    def __attrs_post_init__(self):
        self._dimension = int(sqrt(len(self.tile_lookup.keys())))

        self._connection_list = [
            (tile_num_l, tile_num_r, tile_connections)
            for tile_num_l, tile_num_r in combinations(self.tile_lookup.keys(), 2)
            if (tile_connections := self.tile_lookup[tile_num_l].check_connections(self.tile_lookup[tile_num_r]))
        ]

        tile_connection_count = Counter()
        for tile_num_l, tile_num_r, *_ in self._connection_list:
            tile_connection_count.update((tile_num_l,))
            tile_connection_count.update((tile_num_r,))
        self._connection_count = {}
        for num in tile_connection_count:
            count_set = self._connection_count.setdefault(tile_connection_count[num], set())
            count_set.add(num)

    @property
    def dimension(self):
        return self._dimension

    @property
    def connection_count(self):
        return self._connection_count

    def _check_tile(self, tile_info_l, check_dir, tile_info_r):
        tile_num_l, tile_pos_l = tile_info_l
        tile_num_r, tile_pos_r = tile_info_r
        for conn_l_num, conn_r_num, conn_list in self._connection_list:
            if conn_l_num == tile_num_l and conn_r_num == tile_num_r:
                for conn_pos_l, conn_pos_r, conn_dir in conn_list:
                    if tile_pos_l == conn_pos_l and tile_pos_r == conn_pos_r and check_dir == conn_dir:
                        return True

        return False

    def _check_map_pos(self, map_list, free_tiles, x, y):
        if (x == 0 or x == self.dimension - 1) and (y == 0 or y == self.dimension - 1):
            coord_connections = 2
        elif x == 0 or x == self.dimension - 1 or y == 0 or y == self.dimension - 1:
            coord_connections = 3
        else:
            coord_connections = 4

        for selected_num in [num for num in self.connection_count[coord_connections] if num in free_tiles]:
            new_free_tiles = set(free_tiles)
            new_free_tiles.remove(selected_num)
            tile_info_above = None if y == 0 else map_list[x + (y - 1) * self.dimension]
            tile_info_left = None if x == 0 else map_list[(x - 1) + y * self.dimension]
            for pos in range(POS_MAX):
                selected_tile_info = (selected_num, pos)
                try:
                    if tile_info_above:
                        if not (
                            self._check_tile(tile_info_above, 'above', selected_tile_info) or
                            self._check_tile(selected_tile_info, 'below', tile_info_above)
                        ):
                            raise ValueError(f'tile above not found {x} {y}')

                    if tile_info_left:
                        if not (
                            self._check_tile(tile_info_left, 'left', selected_tile_info) or
                            self._check_tile(selected_tile_info, 'right', tile_info_left)
                        ):
                            raise ValueError(f'tile left not found {x} {y}')

                    new_map = list(map_list)
                    new_map[x + y * self.dimension] = selected_tile_info
                    new_x = 0 if x == self.dimension - 1 else x + 1
                    new_y = y + 1 if x == self.dimension - 1 else y

                    if new_y == self.dimension:
                        return new_map

                    return self._check_map_pos(new_map, new_free_tiles, new_x, new_y)

                except ValueError:
                    pass

        raise ValueError(f'no valid selection for {x}, {y}')

    def get_map_solutions(self):
        map_solutions = []
        for corner_num in self.connection_count[2]:
            free_tiles = set(self.tile_lookup.keys())
            free_tiles.remove(corner_num)
            for pos in range(POS_MAX):
                try:
                    map_list = [None] * self.dimension * self.dimension
                    map_list[0] = (corner_num, pos)
                    map_solutions.append(self._check_map_pos(map_list, free_tiles, 1, 0))

                except ValueError:
                    pass

        return map_solutions

    def print_map(self, map_list):
        line_tile_info_list = []
        for idx, map_tile_info in enumerate(map_list):
            x = idx % self.dimension
            line_tile_info_list.append(map_tile_info)
            if x == self.dimension - 1:
                line_tiles_image_lines = []
                for tile_info in line_tile_info_list:
                    tile_num, tile_pos = tile_info
                    tile = self.tile_lookup[tile_num]
                    line_tiles_image_lines.append(tile.get_tile(tile_pos))

                    print(f'{tile.num:<5}{tile_pos:<6}', end = '')
                print()

                for y in range(len(line_tiles_image_lines[0])):
                    print(' '.join([
                        f'{line_tile_image_lines[y]}'
                        for line_tile_image_lines in line_tiles_image_lines
                    ]))
                print()

                line_tile_info_list = []

    def build_image(self, map_list):
        map_image = []
        line_tile_info_list = []
        for idx, map_tile_info in enumerate(map_list):
            x = idx % self.dimension
            line_tile_info_list.append(map_tile_info)
            if x == self.dimension - 1:
                line_tiles_image_lines = []
                for tile_info in line_tile_info_list:
                    tile_num, tile_pos = tile_info
                    tile = self.tile_lookup[tile_num]
                    line_tiles_image_lines.append(tile.get_borderless_tile(tile_pos))

                for y in range(len(line_tiles_image_lines[0])):
                    map_image.append(''.join([
                        f'{line_tile_image_lines[y]}'
                        for line_tile_image_lines in line_tiles_image_lines
                    ]))

                line_tile_info_list = []

        return map_image


def get_line_as_int(line):
    line_val = 0
    for c in line:
        if c == '#':
            line_val |= 1
        line_val <<= 1
    return line_val


def get_pixel_count(line):
    return sum([1 if c == '#' else 0 for c in line])


def find_monster(map_image):
    mon_image_lines = MONSTER_IMAGE.splitlines()
    mon_mask = [get_line_as_int(line) for line in mon_image_lines]
    map_width = len(map_image[0])
    map_height = len(map_image)
    mon_width = len(mon_image_lines[0])
    mon_height = len(mon_image_lines)
    found_list = []
    for y in range(map_height - mon_height):
        for x in range(map_width - mon_width):
            found = True
            for mon_y in range(mon_height):
                map_image_line = map_image[y + mon_y][x:x + mon_width]
                l_val = get_line_as_int(map_image_line)
                m_val = mon_mask[mon_y]
                if m_val & l_val != m_val:
                    found = False
                    break

            if found:
                found_list.append((x, y))

    return found_list


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
    map_solutions = tile_grid.get_map_solutions()
    result = 0
    for map_solution in map_solutions:
        map_image = tile_grid.build_image(map_solution)
        found_list = find_monster(map_image)
        if found_list:
            found_count = len(found_list)
            pixel_count = get_pixel_count(''.join(map_image))
            monster_pixel_count = get_pixel_count(MONSTER_IMAGE) * found_count
            result = pixel_count - monster_pixel_count
            break

    print(f'{name} {result}')


def run():
    print_results_1(f'part1 test 20899048083289 =', 'data/day20_test.txt')
    print_results_1(f'part1', 'data/day20.txt')

    print_results_2(f'part2 test 273 =', 'data/day20_test.txt')
    print_results_2(f'part2', 'data/day20.txt')


if __name__ == "__main__":
    run()
