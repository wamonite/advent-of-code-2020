#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file, timeit
import re


def parse_file(file_name):
    line_list = load_file(file_name)
    cmd_list = []
    for line in line_list:
        if line.startswith('mask = '):
            mask_str = line[7:]
            mask_val = 0
            one_val = 0
            zero_val = 0
            for c in mask_str:
                mask_val <<= 1
                one_val <<= 1
                zero_val <<= 1

                if c == 'X':
                    mask_val |= 1
                    zero_val |= 1
                elif c == '1':
                    one_val |= 1
                    zero_val |= 1

            cmd_list.append((mask_val, one_val, zero_val))

        else:
            match = re.match(r'^mem\[(?P<addr>\d+)\] = (?P<val>\d+)$', line)
            if match:
                match_lookup = match.groupdict()
                cmd_list.append((int(match_lookup['addr']), int(match_lookup['val'])))

    return cmd_list


def execute_commands(cmd_list):
    mask_val = 0
    one_val = 0
    zero_val = 0
    memory = {}

    for cmd in cmd_list:
        if len(cmd) == 3:
            mask_val, one_val, zero_val = cmd
            print(f'mask {mask_val:>036b}')
            print(f' one {one_val:>036b}')
            print(f'zero {zero_val:>036b}')

        else:
            addr, val = cmd
            val &= mask_val
            val |= one_val
            val &= zero_val
            print(f' val {val:>036b} [{addr:>06}] = {val}')
            memory[addr] = val

    return memory


def print_results_1(name, file_name):
    cmd_list = parse_file(file_name)
    memory = execute_commands(cmd_list)
    result = sum(memory.values())
    print(f'{name} {result}')


def run():
    print_results_1('part1 test 165 =', 'data/day14_test.txt')
    print_results_1('part1', 'data/day14.txt')


if __name__ == "__main__":
    run()
