#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def is_valid_1(pw_info):
    char_min, char_max, char, pw = pw_info
    char_count = pw.count(char)
    return char_min <= char_count <= char_max


def is_valid_2(pw_info):
    char_min, char_max, char, pw = pw_info
    # ignore IndexError as fixed data set
    return len(list(filter(lambda n: pw[n - 1] == char, [char_min, char_max]))) == 1


def run():
    line_extract = re.compile(r'^(\d+)-(\d+) ([a-z]): ([a-z]+)')

    pw_info_list = []
    with open('data/day02.txt') as file_object:
        for line in file_object.readlines():
            line = line.strip()
            # no error checking as fixed data set
            match = line_extract.match(line)
            entry = (int(match.group(1)), int(match.group(2)), match.group(3), match.group(4))
            pw_info_list.append(entry)

    print(len(list(filter(is_valid_1, pw_info_list))))
    print(len(list(filter(is_valid_2, pw_info_list))))


if __name__ == "__main__":
    run()
