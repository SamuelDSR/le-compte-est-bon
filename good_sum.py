#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import itertools


def partitions(numbers):
    for i in range(1, len(numbers) // 2 + 1):
        for comb in itertools.combinations(numbers, i):
            numbers_copy = copy.copy(numbers)
            p1 = comb
            for c in comb:
                numbers_copy.remove(c)
            yield list(p1), list(numbers_copy)


def possible_two(numbers, solution=False):
    sums = []
    a, b = numbers
    if solution:
        sums.append((a + b, [a, "+", b]))
        sums.append((a * b, [a, "*", b]))
        sums.append((a - b, [a, "-", b]))
        sums.append((b - a, [b, "-", a]))
    else:
        sums.append(a + b)
        sums.append(a * b)
        sums.append(a - b)
        sums.append(b - a)
    if a != 0:
        if solution:
            sums.append((b / a, [b, "/", a]))
        else:
            sums.append(b / a)
    if b != 0:
        if solution:
            sums.append((a / b, [a, "/", b]))
        else:
            sums.append(a / b)
    return sums


def possible(numbers):
    possible_sums = []
    if len(numbers) == 1: return [numbers[0]]
    if len(numbers) == 2: return possible_two(numbers)
    for part in partitions(numbers):
        p1, p2 = part
        for poss1 in possible(p1):
            for poss2 in possible(p2):
                possible_sums.extend(possible_two([poss1, poss2]))
    return possible_sums


#  print(list(partitions([4, 2, 3, 1])))
#  sums = possible([10, 7, 5, 5, 2, 1])
#  print(len(sums))
#  print(sums)
#  print(645 in sums)

def possible_ways(numbers, target=None):
    solutions = []
    if len(numbers) == 1 and (numbers[0] == target or target is None):
        return [(numbers[0], '({})'.format(numbers[0]))]
    if len(numbers) == 2:
        a, b = numbers
        if a * b == target or target is None:
            solutions.append((a * b, '({}*{})'.format(a, b)))
        if a + b == target or target is None:
            solutions.append((a + b, '({}+{})'.format(a, b)))
        if a - b == target or target is None:
            solutions.append((a - b, '({}-{})'.format(a, b)))
        if b - a == target or target is None:
            solutions.append((b - a, '({}-{})'.format(b, a)))
        if a != 0 and (b / a == target or target is None):
            solutions.append((b / a, '({}/{})'.format(b, a)))
        if b != 0 and (a / b == target or target is None):
            solutions.append((a / b, '({}/{})'.format(a, b)))
        return solutions

    for part in partitions(numbers):
        p1, p2 = part
        p1_ways = possible_ways(p1, target=None)
        for ways in p1_ways:
            somme = ways[0]
            representation = ways[1]

            p2_ways = possible_ways(p2, target - somme if target is not None else None)
            for w in p2_ways:
                solutions.append(
                    (somme + w[0], "({}+{})".format(representation, w[1])))

            p2_ways = possible_ways(p2, target + somme if target is not None else None)
            for w in p2_ways:
                solutions.append(
                    (w[0] - somme, "({}-{})".format(w[1], representation)))

            if somme != 0:
                p2_ways = possible_ways(p2, target / somme if target is not None else None)
                for w in p2_ways:
                    solutions.append(
                        (somme*w[0], "({}*{})".format(representation, w[1])))

            p2_ways = possible_ways(p2, somme - target if target is not None else None)
            for w in p2_ways:
                solutions.append(
                    (somme-w[0], "({}-{})".format(representation, w[1])))

            if target != 0:
                p2_ways = possible_ways(p2, somme / target if target is not None else None)
                for w in p2_ways:
                    if w[0] != 0:
                        solutions.append(
                            (somme/w[0], "({}/{})".format(representation, w[1])))

            if somme != 0:
                p2_ways = possible_ways(p2, somme * target if target is not None else None)
                for w in p2_ways:
                    solutions.append(
                        (w[0]/somme, "({}/{})".format(w[1], representation)))
    return solutions


#  print(possible_ways([50, 23, 4, 7, 10, 3, 2], 943))
print(possible_ways([10, 7, 5, 5, 2, 1], 645))
