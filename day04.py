#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import timeit

VALID_FIELD_SET = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
VALID_ECL_SET = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
HCL_MIN = ord('0')
HCL_MAX = ord('f')
PID_MIN = ord('0')
PID_MAX = ord('9')
DEBUG = False


def check_passport_1a(passport_lookup):
    field_list = passport_lookup.keys()
    return all(map(lambda f: f in field_list, VALID_FIELD_SET))


def check_passport_1b(passport_lookup):
    field_set = set(passport_lookup.keys())
    return VALID_FIELD_SET.issubset(field_set)


class ValidationException(Exception):
    pass


def validate(name, test):
    if not test:
        raise ValidationException(name)


def get_int(name, val):
    try:
        return int(val)

    except ValueError:
        raise ValidationException(f'{name} int')


def check_passport_2(passport_lookup):
    try:
        validate('fields', check_passport_1b(passport_lookup))
        validate('byr', 1920 <= get_int('byr', passport_lookup['byr']) <= 2002)
        validate('iyr', 2010 <= get_int('iyr', passport_lookup['iyr']) <= 2020)
        validate('eyr', 2020 <= get_int('eyr', passport_lookup['eyr']) <= 2030)

        hgt = passport_lookup['hgt']
        hgt_val = get_int('hgt', hgt[:-2])
        if hgt.endswith('cm'):
            validate('hgt', 150 <= hgt_val <= 193)

        elif hgt.endswith('in'):
            validate('hgt', 59 <= hgt_val <= 76)

        else:
            raise ValidationException('hgt')

        validate('hcl', passport_lookup['hcl'][0] == '#')
        for c in passport_lookup['hcl'][1:]:
            validate('hcl', HCL_MIN <= ord(c) <= HCL_MAX)

        validate('ecl', passport_lookup['ecl'] in VALID_ECL_SET)

        validate('pid', len(passport_lookup['pid']) == 9)
        for c in passport_lookup['pid']:
            validate('fields', PID_MIN <= ord(c) <= PID_MAX)

    except ValidationException as e:
        if DEBUG:
            print(f'  {e}: {passport_lookup}')
        return False

    return True


@timeit
def count_validated_passports(validate_func, passport_list):
    return len(list(filter(validate_func, passport_list)))


def parse_passports(lines):
    passport_lookup = {}
    for line in map(str.strip, lines):
        if line:
            for field in line.split():
                k, v = field.split(':')
                passport_lookup[k] = v

        else:
            yield passport_lookup
            passport_lookup = {}

    if passport_lookup:
        yield passport_lookup


def load_file(file_name):
    with open(file_name) as file_object:
        return list(parse_passports(file_object.readlines()))


def run():
    passport_list = load_file('data/day04.txt')

    print('part1a', count_validated_passports(check_passport_1a, passport_list))
    print('part1b', count_validated_passports(check_passport_1b, passport_list))

    print('part2 test 4 ==', count_validated_passports(check_passport_2, load_file('data/day04_test.txt')))

    print('part2', count_validated_passports(check_passport_2, passport_list))


if __name__ == "__main__":
    run()
