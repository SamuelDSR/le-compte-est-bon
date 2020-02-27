#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import re
from collections import Counter


def add_expression(left_expression, right_expression):
    return left_expression + right_expression


def mul_expression(left_expression, right_expression):
    new_expression = []
    for left in left_expression:
        for right in right_expression:
            new_expression.append(left + "*" + right)
    return new_expression


def sub_expression(left_expression, right_expression):
    new_expression = copy.copy(left_expression)
    for right in right_expression:
        new_expression.append('(-1)*' + right)
    return new_expression


def div_expression(left_expression, right_expression):
    right_expression = '+'.join(right_expression)
    new_expression = []
    for left in left_expression:
        new_expression.append(left + "/(" + right_expression + ")")
    return new_expression


def precedence(op):
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/':
        return 2
    return 0


def multinomial_expand(v1, v2, op):
    if op == '+':
        return add_expression(v1, v2)
    elif op == '*':
        return mul_expression(v1, v2)
    elif op == '-':
        return sub_expression(v1, v2)
    else:
        return div_expression(v1, v2)


def arthmetic_evalue(v1, v2, op):
    if op == '+':
        return v1 + v2
    elif op == '*':
        return v1 * v2
    elif op == '-':
        return v1 - v2
    else:
        return v1 / v2


def is_number(num_str):
    try:
        float(num_str)
    except:
        return False
    else:
        return True


def evaluate_arithmetic_expression(expression, evaluate_number, precedence,
                                   evaluate_op, all_no_commutative=[]):
    value_stack = []
    op_stack = []
    tokens = re.split(r'([^0-9\s\.])', expression)
    print(tokens)
    for token in tokens:
        if token == '' or token.strip() == '':
            continue
        elif is_number(token):
            value_stack.append(evaluate_number(token))
        elif token == "(":
            op_stack.append(token)
        elif token == ")":
            while len(op_stack) != 0 and op_stack[-1] != "(":
                op = op_stack.pop()
                v2, v1 = value_stack.pop(), value_stack.pop()
                value_stack.append(evaluate_op(v1, v2, op))
                if op in '-/':
                    all_no_commutative.append((v1, v2, op))
            op_stack.pop()
        else:
            while len(op_stack) != 0 and precedence(
                    op_stack[-1]) >= precedence(token):
                try:
                    v2, v1 = value_stack.pop(), value_stack.pop()
                except Exception as e:
                    print(token)
                    print(op_stack)
                    raise e
                op = op_stack.pop()
                value_stack.append(evaluate_op(v1, v2, op))
                if op in '-/':
                    all_no_commutative.append((v1, v2, op))
            op_stack.append(token)

    while len(op_stack) != 0:
        v2, v1 = value_stack.pop(), value_stack.pop()
        op = op_stack.pop()
        value_stack.append(evaluate_op(v1, v2, op))
        if op in '-/':
            all_no_commutative.append((v1, v2, op))
    return value_stack[-1]


def is_equivalent(left_expr, right_expr):
    left_com = []
    left_ret = evaluate_arithmetic_expression(left_expr, float, precedence, arthmetic_evalue, left_com)
    left_com = Counter(left_com)

    right_com = []
    right_ret = evaluate_arithmetic_expression(right_expr, float, precedence, arthmetic_evalue, right_com)
    right_com = Counter(right_com)
    print(left_com)
    print(right_com)

    if left_ret != right_ret:
        return False

    for key in left_com:
        if key not in right_com:
            return False
        if left_com[key] != right_com[key]:
            return False
    return True


if __name__ == '__main__':
    expression = '(((((((5*(10*((7*2)-1)))-5)*11- 5)*2)/2)*3)   - 5)'
    all_com = []
    print(evaluate_arithmetic_expression(expression, float, precedence, arthmetic_evalue, all_com))
    print(all_com)
    #  print(evaluate_arithmetic_expression(expression, lambda x: [x.strip()], precedence, multinomial_expand))

    print(is_equivalent("(((10*5)*((7*2)-(1)))-(5))", "(((5)*((10)*((7*2)-(1))))-(5))"))
    print(is_equivalent("7*(5+2*2)", "7*(5+2+ 12)"))
