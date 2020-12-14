#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file
import re
from itertools import product


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
                elif c == '1':
                    one_val |= 1
                elif c == '0':
                    zero_val |= 1

            cmd_list.append((mask_val, one_val, zero_val))

        else:
            match = re.match(r'^mem\[(?P<addr>\d+)\] = (?P<val>\d+)$', line)
            if match:
                match_lookup = match.groupdict()
                cmd_list.append((int(match_lookup['addr']), int(match_lookup['val'])))

    return cmd_list


def invert_mask(mask_val):
    return 0b111111111111111111111111111111111111 ^ mask_val


def execute_commands_1(cmd_list):
    mask_val = 0
    one_val = 0
    zero_val = 0
    memory = {}

    for cmd in cmd_list:
        if len(cmd) == 3:
            mask_val, one_val, zero_val = cmd
            zero_val = invert_mask(zero_val)
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


def generate_bitmasks(mask_val):
    # count bits
    bit_count = 0
    shift_val = mask_val
    for _ in range(36):
        if shift_val & 1:
            bit_count += 1

        shift_val >>= 1

    bit_mask_list = []
    one_val = 1 << 36
    for bit_combination in product(range(2), repeat = bit_count):
        shift_val = mask_val
        bit_idx = 0
        bit_mask = 0
        for _ in range(36):
            if shift_val & 1:
                if bit_combination[bit_idx]:
                    bit_mask |= one_val
                bit_idx += 1
            shift_val >>= 1
            bit_mask >>= 1
        bit_mask_list.append(bit_mask)

    return bit_mask_list


def execute_commands_2(cmd_list):
    mask_val = 0
    mask_list = []
    one_val = 0
    zero_val = 0
    memory = {}

    for cmd in cmd_list:
        if len(cmd) == 3:
            mask_val, one_val, zero_val = cmd
            mask_list = generate_bitmasks(mask_val)
            mask_val = invert_mask(mask_val)
            print(f'mask {mask_val:>036b}')
            print(f' one {one_val:>036b}')
            print(f'zero {zero_val:>036b}')

        else:
            addr, val = cmd
            addr &= zero_val
            addr |= one_val
            addr &= mask_val
            for float_val in mask_list:
                addr_val = addr | float_val
                print(f'addr {addr_val:>036b} [{addr_val:>06}] = {val}')

                memory[addr_val] = val

    return memory


def print_results(name, file_name, execute_func):
    cmd_list = parse_file(file_name)
    memory = execute_func(cmd_list)
    result = sum(memory.values())
    print(f'{name} {result}')


def run():
    print_results('part1 test 165 =', 'data/day14_test1.txt', execute_commands_1)
    print_results('part1', 'data/day14.txt', execute_commands_1)

    print_results('part2 test 208 =', 'data/day14_test2.txt', execute_commands_2)
    print_results('part2', 'data/day14.txt', execute_commands_2)


if __name__ == "__main__":
    run()
