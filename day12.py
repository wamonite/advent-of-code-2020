#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file_generator


def parse_file(line_list):
    for line in line_list:
        cmd = line[0]
        val = int(line[1:])
        yield cmd, val


class Navigator(object):
    DIR_LIST = ('N', 'E', 'S', 'W')
    DIR_START = DIR_LIST.index('E')

    def __init__(self):
        self.dir = self.DIR_START
        self.x = 0
        self.y = 0

    @property
    def pos(self):
        return self.x, self.y

    def turn(self, val):
        step = val // 90
        self.dir = (self.dir + step) % 4

    def forward(self, val):
        if self.dir == 0:
            self.y += val
        elif self.dir == 1:
            self.x += val
        elif self.dir == 2:
            self.y -= val
        else:
            self.x -= val

    def execute(self, cmd, val):
        if cmd == 'F':
            self.forward(val)
        elif cmd == 'L':
            self.turn(-val)
        elif cmd == 'R':
            self.turn(val)
        elif cmd == 'N':
            self.y += val
        elif cmd == 'S':
            self.y -= val
        elif cmd == 'E':
            self.x += val
        elif cmd == 'W':
            self.x -= val
        else:
            raise KeyError(cmd)

        # print(f'{cmd} {val} => {self.dir=} {self.x=} {self.y=}')


class WayPointNavigator(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.wx = 10
        self.wy = 1

    @property
    def pos(self):
        return self.x, self.y

    def rotate(self, val):
        step = val // 90
        for _ in range(abs(step)):
            self.wx, self.wy = (self.wy, -self.wx) if step > 0 else (-self.wy, self.wx)

    def execute(self, cmd, val):
        if cmd == 'F':
            self.x += val * self.wx
            self.y += val * self.wy
        elif cmd == 'L':
            self.rotate(-val)
        elif cmd == 'R':
            self.rotate(val)
        elif cmd == 'N':
            self.wy += val
        elif cmd == 'S':
            self.wy -= val
        elif cmd == 'E':
            self.wx += val
        elif cmd == 'W':
            self.wx -= val
        else:
            raise KeyError(cmd)

        # print(f'{cmd} {val} => {self.wx=} {self.wy=} {self.x=} {self.y=}')


def execute_commands(cmd_list, navigator):
    for cmd, val in cmd_list:
        navigator.execute(cmd, val)
    x, y = navigator.pos
    return abs(x) + abs(y)


def run():
    result = execute_commands(parse_file(load_file_generator('data/day12_test.txt')), Navigator())
    print(f'part1 test 25 = {result}')

    result = execute_commands(parse_file(load_file_generator('data/day12.txt')), Navigator())
    print(f'part1 = {result}')

    result = execute_commands(parse_file(load_file_generator('data/day12_test.txt')), WayPointNavigator())
    print(f'part2 test 286 = {result}')

    result = execute_commands(parse_file(load_file_generator('data/day12.txt')), WayPointNavigator())
    print(f'part2 = {result}')


if __name__ == "__main__":
    run()
