#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file
from collections import deque


def parse_input(line_list):
    player_deck = deque()
    player_deck_list = [player_deck]
    for line in line_list:
        if not line:
            player_deck = deque()
            player_deck_list.append(player_deck)

        elif line.endswith(':'):
            pass

        else:
            player_deck.append(int(line))

    return player_deck_list


def play_game_1(player_deck_list):
    while all(player_deck_list):
        card_list = []
        for player_deck in player_deck_list:
            card_list.append(player_deck.popleft())
        winning_player = card_list.index(max(card_list))
        player_deck_list[winning_player].append(card_list.pop(winning_player))
        player_deck_list[winning_player].extend(card_list)


def play_game_2(player_deck_list):
    rounds_played = set()
    while all(player_deck_list):
        decks_key = tuple([tuple(player_deck) for player_deck in player_deck_list])
        if decks_key in rounds_played:
            return 0

        card_list = []
        for player_deck in player_deck_list:
            card_list.append(player_deck.popleft())

        winning_player = card_list.index(max(card_list))

        if all([len(player_deck_list[i]) >= card_list[i] for i in range(len(player_deck_list))]):
            winning_player = play_game_2([deque(list(d)[:card_list[i]]) for i, d in enumerate(player_deck_list)])

        player_deck_list[winning_player].append(card_list.pop(winning_player))
        player_deck_list[winning_player].extend(card_list)

        rounds_played.add(decks_key)

    winning_player = max([i for i, d in enumerate(player_deck_list) if d])
    return winning_player


def calculate_score(player_deck_list):
    return [sum([idx * card for idx, card in enumerate(reversed(player_deck), 1)]) for player_deck in player_deck_list]


def print_results(name, file_name, play_func):
    line_list = load_file(file_name)
    player_deck_list = parse_input(line_list)
    play_func(player_deck_list)
    result_list = calculate_score(player_deck_list)
    print(f'{name} {sum(result_list)}')


def run():
    print_results(f'part1 test 306 =', 'data/day22_test.txt', play_game_1)
    print_results(f'part1', 'data/day22.txt', play_game_1)

    print_results(f'part2 test 291 =', 'data/day22_test.txt', play_game_2)
    print_results(f'part2', 'data/day22.txt', play_game_2)


if __name__ == "__main__":
    run()
