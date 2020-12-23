#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import timeit
import numpy
import attr
from math import prod


@attr.s
class Cups:
    _cups = attr.ib(init = False)
    _max = attr.ib(init = False)
    _current = attr.ib(init = False)

    @classmethod
    def from_str(cls, text, extended_max = None):
        c = cls()
        if extended_max is not None:
            c._max = extended_max
        else:
            c._max = len(text)

        c._cups = numpy.arange(1, c._max + 2, dtype = int)

        # zero index is never used
        c._cups[0] = -1

        # head
        c._current = int(text[0])

        last_val = c._current
        for char in text[1:]:
            val = int(char)
            c._cups[last_val] = val
            last_val = val

        # do we point the end of the data at the head or on to extended values?
        if c._max == len(text):
            # point tail at head
            c._cups[last_val] = c._current

        else:
            # point tail onto next value
            c._cups[last_val] = len(text) + 1

            # point extended tail at head
            c._cups[c._max] = c._current

        return c

    def _insert(self, val, after):
        next_val = self._cups[after]
        self._cups[val] = next_val
        self._cups[after] = val

    def _pick(self):
        next_val = self._cups[self._current]
        next_idx = self._cups[next_val]
        self._cups[self._current] = next_idx
        self._cups[next_val] = -1
        return next_val

    def play_round(self):
        picked = [self._pick() for _ in range(3)]

        dest_val = self._current - 1
        while True:
            if dest_val == 0:
                dest_val = self._max

            if dest_val in picked:
                dest_val -= 1

            else:
                break

        while picked:
            val = picked.pop(0)
            self._insert(val, dest_val)
            dest_val = val

        self._current = self._cups[self._current]

    def print_cups(self):
        # print(' '.join([f'{i}:({v})' if v == self._current else f'{i}:{v}' for i, v in enumerate(self._cups)]))

        val_list = [f'({self._current})']
        idx = self._cups[self._current]
        while idx != self._current:
            val_list.append(str(idx))
            idx = self._cups[idx]

        print(' '.join(val_list))

    def get_result_1(self):
        result = ''
        idx = self._cups[1]
        while idx != 1:
            result += str(idx)
            idx = self._cups[idx]

        return result

    def get_result_2(self):
        idx = self._cups[1]
        return idx, self._cups[idx]


def print_results_1(name, text):
    cups = Cups.from_str(text)
    for _ in range(100):
        cups.play_round()
    print(f'{name} {cups.get_result_1()}')


@timeit
def print_results_2(name, text):
    cups = Cups.from_str(text, 1000000)
    for _ in range(10000000):
        cups.play_round()
    results = cups.get_result_2()
    print(f'{name} {prod(results)}')


def run():
    print_results_1(f'part1 test 67384529 =', '389125467')
    print_results_1(f'part1', '463528179')

    print_results_2(f'part2 test 934001 * 159792 = 149245887792 :', '389125467')
    print_results_2(f'part2', '463528179')


if __name__ == "__main__":
    run()
