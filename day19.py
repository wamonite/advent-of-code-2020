#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file


MODIFY_LOOKUP = {
    '8': '42 | 42 8',
    '11': '42 31 | 42 11 31',
}


def parse_input(line_list, modify):
    rule_lookup = {}
    message_list = []

    for line in line_list:
        if ':' in line:
            rule_num_str, rule_str = line.split(': ')
            if modify:
                if rule_num_str in MODIFY_LOOKUP:
                    rule_str = MODIFY_LOOKUP[rule_num_str]

            current_rule_list = []
            rule_list = []
            rule_token_list = rule_str.split(' ')
            for rule_token in rule_token_list:
                if rule_token == '|':
                    rule_list.append(tuple(current_rule_list))
                    current_rule_list = []

                elif rule_token.isdigit():
                    current_rule_list.append(int(rule_token))

                else:
                    current_rule_list.append(rule_token[1:-1])

            if current_rule_list:
                rule_list.append(tuple(current_rule_list))

            rule_lookup[int(rule_num_str)] = tuple(rule_list)

        elif line:
            message_list.append(line)

    return rule_lookup, message_list


def match_rule(rule_lookup, rule_num, message, step = 0):
    # print(f'{rule_num=} {message=}')
    if not message:
        # print(f'failed empty message')
        return ''

    matched_message = ''
    rule_option_list = rule_lookup[rule_num]
    if len(rule_option_list) == 1:
        rule_list = rule_option_list[0]
        if len(rule_list) == 1 and isinstance(rule_list[0], str):
            char_test = message[0] if message[0] == rule_list[0] else ''
            # print(f'failed {message[0]} != {rule_list[0]}' if not char_test else f'found {message[0]}')
            return char_test

        # try a few more rule 8's if we previously failed on rule 11
        if step:
            rule_list = tuple([8] * step) + rule_list

        for rule in rule_list:
            rule_result = match_rule(rule_lookup, rule, message[len(matched_message):])
            if not rule_result:
                # print(f'not all rules met {rule_num=} {rule_list=} {message[len(matched_message):]}')

                # failed on rule 11, so try again with another rule 8 before
                if rule_num == 0 and rule == 11 and len(rule_lookup[8]) > 1:
                    return match_rule(rule_lookup, 0, message, step + 1)

                return ''

            matched_message += rule_result

    else:
        for rule_list in rule_option_list:
            result = ''
            for rule in rule_list:
                rule_result = match_rule(rule_lookup, rule, message[len(result):])
                if not rule_result:
                    # print(f'optional rule not met {rule=} {message[len(result):]}')
                    result = ''
                    break
                result += rule_result

            if result:
                # print(f'{rule_num=} {result=}')
                return result

        # print(f'all optional rules not met {rule_num=} {message=}')
        return ''

    # print(f'{rule_num=} {matched_message=}')
    return matched_message


def print_results(name, file_name, modify = False):
    line_list = load_file(file_name)
    rule_lookup, message_list = parse_input(line_list, modify)
    result_list = [match_rule(rule_lookup, 0, message) == message for message in message_list]
    result = sum(result_list)
    print(f'{name} {result}')


def run():
    print_results(f'part1 test 2 =', 'data/day19_test1.txt')
    print_results(f'part1', 'data/day19.txt')

    print_results(f'part2 test 3 =', 'data/day19_test2.txt')
    print_results(f'part2 test 12 =', 'data/day19_test2.txt', True)
    print_results(f'part2', 'data/day19.txt', True)


if __name__ == "__main__":
    run()
