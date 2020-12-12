#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file_generator


DIR_LIST = ('N', 'E', 'S', 'W')
DIR_START = DIR_LIST.index('E')


def parse_file(line_list):
    for line in line_list:
        cmd = line[0]
        val = int(line[1:])
        yield cmd, val


class Navigator(object):
    def __init__(self):
        self.dir = DIR_START
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


def execute_commands(cmd_list):
    n = Navigator()
    for cmd, val in cmd_list:
        n.execute(cmd, val)
    x, y = n.pos
    return abs(x) + abs(y)


def run():
    result = execute_commands(parse_file(load_file_generator('data/day12_test.txt')))
    print(f'part1 test 25 = {result}')

    result = execute_commands(parse_file(load_file_generator('data/day12.txt')))
    print(f'part1 = {result}')


if __name__ == "__main__":
    run()
