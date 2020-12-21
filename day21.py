#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aocutil import load_file
from random import sample


def parse_input(line_list):
    ingredient_list = []
    for line in line_list:
        ingredient_str, allergens_str = line.split(' (contains ')
        ingredient = set(ingredient_str.split(' ')), set(allergens_str[:-1].split(', '))
        ingredient_list.append(ingredient)

    return ingredient_list


def get_all_elements(ingredient_list):
    all_ingredients = set()
    all_allergens = set()
    for ingredients, allergens in ingredient_list:
        all_ingredients |= ingredients
        all_allergens |= allergens

    return all_ingredients, all_allergens


def search_allergens(ingredient_list):
    all_ingredients, all_allergens = get_all_elements(ingredient_list)
    allergen_lookup = {}
    allergen_free = set()
    while all_allergens:
        search_ingredient_set = None
        found_ingredient = None
        found_allergen = None
        for search_allergen in sample(list(all_allergens), 1):
            for test_ingredients, test_allergens in ingredient_list:
                if search_allergen in test_allergens:
                    if search_ingredient_set is None:
                        search_ingredient_set = set(test_ingredients)
                    else:
                        search_ingredient_set &= test_ingredients

            if len(search_ingredient_set) == 1:
                found_allergen = search_allergen
                found_ingredient = search_ingredient_set.pop()
                break

        if found_allergen:
            all_allergens.remove(found_allergen)
            allergen_lookup[found_allergen] = found_ingredient
            updated_ingredients = []
            for test_ingredients, test_allergens in ingredient_list:
                if found_ingredient in test_ingredients:
                    test_ingredients.remove(found_ingredient)
                if found_allergen in test_allergens:
                    test_allergens.remove(found_allergen)

                if test_ingredients and test_allergens:
                    updated_ingredients.append((test_ingredients, test_allergens))
                elif test_ingredients:
                    allergen_free.update(set(test_ingredients))

    return allergen_lookup, allergen_free


def print_results_1(name, file_name):
    line_list = load_file(file_name)
    ingredient_list = parse_input(line_list)
    allergen_lookup, allergen_free = search_allergens(ingredient_list)
    ingredient_count = 0
    for ingredients, _ in ingredient_list:
        ingredient_count += len(ingredients & allergen_free)
    print(f'{name} {ingredient_count}')


def run():
    print_results_1(f'part1 test 5 =', 'data/day21_test.txt')
    print_results_1(f'part1', 'data/day21.txt')


if __name__ == "__main__":
    run()
