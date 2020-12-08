#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file

ACC = 0
JMP = 1
NOP = 2
CMD_LIST = [
    'acc',
    'jmp',
    'nop',
]


def parse_cmds(lines):
    for line in lines:
        cmd, val = line.split(' ')
        yield CMD_LIST.index(cmd), int(val)


class InfiniteLoopException(Exception):
    pass


def run_cmds(cmd_list):
    acc = 0
    cmd_set = set()
    ip = 0
    while True:
        if ip in cmd_set:
            raise InfiniteLoopException(f'ip = {ip}, acc = {acc}')

        cmd_set.add(ip)

        cmd, val = cmd_list[ip]
        # print(f'[{ip:04}] {CMD_LIST[cmd]} {val:>4} = {acc}')

        if cmd == ACC:
            acc += val

        ip += val if cmd == JMP else 1


def handle_run(name, cmd_list):
    try:
        print(name, run_cmds(cmd_list))
    except InfiniteLoopException as e:
        print(name, 'InfiniteLoopException', e)


def run():
    test_data = list(parse_cmds(load_file('data/day8_test.txt')))
    data = list(parse_cmds(load_file('data/day8.txt')))

    handle_run('part1 test', test_data)
    handle_run('part1', data)


if __name__ == "__main__":
    run()
