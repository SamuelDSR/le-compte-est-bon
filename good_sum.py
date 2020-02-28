#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import itertools
import pprint
import time
import functools
from eval_stack import signature

ADD_FORMATTER = lambda a, b: '({}+{})'.format(a, b)
MUL_FORMATTER = lambda a, b: '({}*{})'.format(a, b)
SUB1_FORMATTER = lambda a, b: '({}-{})'.format(a, b)
SUB2_FORMATTER = lambda a, b: '({}-{})'.format(b, a)
DIV1_FORMATTER = lambda a, b: '({}/{})'.format(a, b)
DIV2_FORMATTER = lambda a, b: '({}/{})'.format(b, a)


def timeit(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        end = time.time()
        print("Running time of {}: {:.2f} secs".format(
            func.__name__, end - start))
        return ret

    return _wrapper


def partitions(numbers):
    '''
    A generator that yield all 2-partitions of a list numbers.
    Args:
        numbers (list): numbers,  e.g., [1, 2, 3]

    Yield:
        part1, part2 (list): two partitions
    '''
    for i in range(1, len(numbers) // 2 + 1):
        if i == len(numbers) / 2:
            for part1 in itertools.combinations(numbers[:-1], i - 1):
                part2 = copy.copy(numbers[:-1])
                for c in part1:
                    part2.remove(c)
                part1 = list(part1)
                part1.append(numbers[-1])
                yield list(part1), list(part2)
        else:
            for part1 in itertools.combinations(numbers, i):
                part2 = copy.copy(numbers)
                for c in part1:
                    part2.remove(c)
                yield list(part1), list(part2)


def possible_two(a, b, a_rep=None, b_rep=None):
    '''
    Possible result of two numbers using +|-|*|/ operators
    '''
    a_rep = a_rep if a_rep is not None else a
    b_rep = b_rep if b_rep is not None else b

    yield a * b, MUL_FORMATTER
    yield a + b, ADD_FORMATTER
    yield a - b, SUB1_FORMATTER
    yield b - a, SUB2_FORMATTER
    if a != 0:
        yield b / a, DIV2_FORMATTER
    if b != 0:
        yield a / b, DIV1_FORMATTER


def possible_right(target, left):
    '''
    Possible right value of [left +|-|*|/ right = target]
    '''
    yield target - left, ADD_FORMATTER
    if left != 0:
        yield target / left, MUL_FORMATTER
    yield left - target, SUB1_FORMATTER
    yield left + target, SUB2_FORMATTER
    # left/b = target, b can not be zero either.
    if target != 0 and left != 0:
        yield left / target, DIV1_FORMATTER
    # b/left = target, left can not be zero
    if left != 0:
        yield left * target, DIV2_FORMATTER


def possible_ways(numbers, target=None, memory=None):
    """
    Possible ways using numbers, +|-|*|/, and brackets to get target.
    If target is None, return all possible values.

    Examples:
        using [10, 7, 5, 5, 2, 1] to get 645
        ((10*7 - 5)*2 - 1)*5 = 645
    """
    if memory is not None:
        num_key = (tuple(sorted(numbers)), target)
        if num_key in memory:
            return memory[num_key]

    solutions = []

    if len(numbers) == 1 and (numbers[0] == target or target is None):
        solutions = [(numbers[0], '({})'.format(numbers[0]))]
        if memory is not None:
            memory[((numbers[0]), target)] = solutions
        return solutions

    if len(numbers) == 2:
        a, b = numbers
        for op_ret, op_formatter in possible_two(a, b):
            if op_ret == target or target is None:
                solutions.append((op_ret, op_formatter(a, b)))
        if memory is not None:
            num_key = (tuple(sorted(numbers)), target)
            memory[num_key] = solutions
        return solutions

    for part in partitions(numbers):
        left, right = part
        left_ways = possible_ways(left, target=None, memory=memory)

        for left_ret, left_repr in left_ways:
            if target is None:
                right_ways = possible_ways(right, target, memory=memory)
                for right_ret, right_repr in right_ways:
                    for op_ret, op_formatter in possible_two(
                            left_ret, right_ret):
                        solutions.append(
                            (op_ret, op_formatter(left_repr, right_repr)))
            else:
                for right_ret, op_formatter in possible_right(
                        target, left_ret):
                    right_ways = possible_ways(right, right_ret, memory=memory)
                    for right_ret, right_repr in right_ways:
                        solutions.append(
                            (target, op_formatter(left_repr, right_repr)))
    if memory is not None:
        num_key = (tuple(sorted(numbers)), target)
        memory[num_key] = solutions
    return solutions


if __name__ == '__main__':
    # search all solutions without memory
    solutions = timeit(possible_ways)([10, 7, 5, 5, 6, 2, 1], 1694, None)
    pprint.pprint(solutions)

    # search all solutions with memory
    solutions = timeit(possible_ways)([10, 7, 5, 5, 6, 2, 1], 1694, {})
    pprint.pprint(solutions)

    # remove all equivalent solutions
    solutions_dict = dict((signature(s[1]), s[1]) for s in solutions)
    solutions = list(solutions_dict.values())
    pprint.pprint(solutions)
