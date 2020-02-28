#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import functools
import itertools
import operator
import pprint
import time

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


def possible_two(a, b, force_integer):
    '''
    Possible result of two numbers using +|-|*|/ operators
    '''
    yield a * b, MUL_FORMATTER
    yield a + b, ADD_FORMATTER
    yield a - b, SUB1_FORMATTER
    yield b - a, SUB2_FORMATTER
    if a != 0 and (not force_integer or int(b / a) == b / a):
        yield b / a, DIV2_FORMATTER
    if b != 0 and (not force_integer or int(a / b) == a / b):
        yield a / b, DIV1_FORMATTER


def possible_right(target, left, force_integer):
    '''
    Possible right value of [left +|-|*|/ right = target]
    '''
    # b/left = target, left can not be zero
    if left != 0:
        yield left * target, DIV2_FORMATTER
    if left != 0 and (not force_integer
                      or int(target / left) == target / left):
        yield target / left, MUL_FORMATTER
    # left/b = target, b can not be zero either.
    if target != 0 and left != 0 and (not force_integer
                                      or int(left / target) == left / target):
        yield left / target, DIV1_FORMATTER
    yield left - target, SUB1_FORMATTER
    yield left + target, SUB2_FORMATTER
    yield target - left, ADD_FORMATTER


def possible_ways(numbers,
                  target=None,
                  memory=None,
                  first_only=False,
                  force_integer=False):
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
    if target is not None and functools.reduce(operator.mul, numbers) < target:
        if memory is not None:
            memory[((numbers[0]), target)] = solutions
        return solutions

    if len(numbers) == 1 and (numbers[0] == target or target is None):
        solutions = [(numbers[0], '({})'.format(numbers[0]))]
        if memory is not None:
            memory[((numbers[0]), target)] = solutions
        return solutions

    if len(numbers) == 2:
        a, b = numbers
        for op_ret, op_formatter in possible_two(a, b, force_integer):
            if target is None or (op_ret == target and not first_only):
                solutions.append((op_ret, op_formatter(a, b)))
            elif op_ret == target and first_only:
                return [(op_ret, op_formatter(a, b))]
            else:
                pass
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
                            left_ret, right_ret, force_integer):
                        solutions.append(
                            (op_ret, op_formatter(left_repr, right_repr)))
            else:
                for right_ret, op_formatter in possible_right(
                        target, left_ret, force_integer):
                    right_ways = possible_ways(right, right_ret, memory=memory)
                    for right_ret, right_repr in right_ways:
                        if first_only:
                            if memory is not None:
                                num_key = (tuple(sorted(numbers)), target)
                                memory[num_key] = solutions
                            return [(target,
                                     op_formatter(left_repr, right_repr))]
                        else:
                            solutions.append(
                                (target, op_formatter(left_repr, right_repr)))
    if memory is not None:
        num_key = (tuple(sorted(numbers)), target)
        memory[num_key] = solutions
    return solutions


if __name__ == '__main__':
    numbers = [10, 7, 5, 5, 2, 1]
    target = 648
    print("========================================================")
    print("Search first solution without memory:")
    pprint.pprint(timeit(possible_ways)(numbers, target, None, first_only=True))

    print("========================================================")
    print("Search first solution with memory:")
    pprint.pprint(timeit(possible_ways)(numbers, target, {}, first_only=True))

    print("========================================================")
    print("Search all solutions with memory:")
    solutions = timeit(possible_ways)(numbers, target, {}, first_only=False)
    pprint.pprint(solutions)

    # remove all equivalent solutions
    solutions_dict = dict((signature(s[1]), s[1]) for s in solutions)
    solutions = list(solutions_dict.values())
    print("========================================================")
    print("Unique solutions:")
    pprint.pprint(solutions)
