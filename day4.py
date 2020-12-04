#!/usr/bin/env python
# -*- coding: utf-8 -*-


def run():
    passport_list = []
    field_lookup = {}
    with open('data/day4.txt') as file_object:
        for line in file_object.readlines():
            line = line.strip()
            if line:
                for field in line.split():
                    k, v = field.split(':')
                    field_lookup[k] = v

            else:
                passport_list.append(field_lookup)
                field_lookup = {}

    print(passport_list)


if __name__ == "__main__":
    run()
