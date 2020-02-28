#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import re


def add_expression(left_expression, right_expression):
    left_numerator = left_expression[0]
    left_denominator = left_expression[1]

    right_numerator = right_expression[0]
    right_denominator = right_expression[1]

    if len(left_denominator) == 0 and len(right_denominator) == 0:
        new_numerator = left_numerator + right_numerator
        return [new_numerator, []]

    new_numerator_p1 = mul_expression([left_numerator, []],
                                      [right_denominator, []])
    new_numerator_p2 = mul_expression([left_denominator, []],
                                      [right_numerator, []])

    new_numerator = add_expression(new_numerator_p1, new_numerator_p2)
    new_numerator = new_numerator[0]
    new_denominator = mul_expression([left_denominator, []],
                                     [right_denominator, []])
    new_denominator = new_denominator[0]
    return [new_numerator, new_denominator]


def mul_expression(left_expression, right_expression):
    left_numerator = left_expression[0]
    left_denominator = left_expression[1]

    right_numerator = right_expression[0]
    right_denominator = right_expression[1]

    new_numerator = []
    if len(left_numerator) != 0 and len(right_numerator) != 0:
        for l in left_numerator:
            for r in right_numerator:
                new_numerator.append(l + "*" + r)
    elif len(left_numerator) == 0:
        new_numerator = copy.copy(right_numerator)
    elif len(right_numerator) == 0:
        new_numerator = copy.copy(left_numerator)
    else:
        pass

    new_denominator = []
    if len(left_denominator) != 0 and len(right_denominator) != 0:
        for l in left_denominator:
            for r in right_denominator:
                new_denominator.append(l + "*" + r)
    elif len(left_denominator) == 0:
        new_denominator = copy.copy(right_denominator)
    elif len(right_denominator) == 0:
        new_denominator = copy.copy(left_denominator)
    else:
        pass

    return [new_numerator, new_denominator]


def sub_expression(left_expression, right_expression):
    right_numerator = right_expression[0]
    new_right_numerator = ['(-1)*' + rn for rn in right_numerator]
    return add_expression(left_expression,
                          [new_right_numerator, right_expression[1]])


def div_expression(left_expression, right_expression):
    return mul_expression(left_expression,
                          [right_expression[1], right_expression[0]])


def precedence(op):
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/':
        return 2
    return 0


def multinomial_expand(v1, v2, op):
    if isinstance(v1, str):
        v1 = [[v1], []]
    if isinstance(v2, str):
        v2 = [[v2], []]
    #  print("----------------------------------------------------------")
    #  print(v1)
    #  print(v2)
    #  print(op)
    #  print("----------------------------------------------------------")
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
                                   evaluate_op):
    value_stack = []
    op_stack = []
    tokens = re.split(r'([^0-9\s\.])', expression)
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
            op_stack.pop()
        else:
            while len(op_stack) != 0 and precedence(
                    op_stack[-1]) >= precedence(token):
                v2, v1 = value_stack.pop(), value_stack.pop()
                op = op_stack.pop()
                value_stack.append(evaluate_op(v1, v2, op))
            op_stack.append(token)

    while len(op_stack) != 0:
        v2, v1 = value_stack.pop(), value_stack.pop()
        op = op_stack.pop()
        value_stack.append(evaluate_op(v1, v2, op))
    return value_stack[-1]


def sort_basic_element(elem):
    tokens = elem.split("*")
    # normalize -1 in mul
    no_minus1_tokens = [x for x in tokens if x != '(-1)']
    minus1_cnt = len(tokens) - len(no_minus1_tokens)
    if minus1_cnt % 2 == 1:
        no_minus1_tokens.append('(-1)')
    tokens = sorted(no_minus1_tokens, key=lambda x: -eval(x))
    return "*".join(tokens)


def signature(expression):
    expansion = evaluate_arithmetic_expression(expression, lambda x: x.strip(),
                                               precedence, multinomial_expand)

    numerator_expansion = [sort_basic_element(x) for x in expansion[0]]
    numerator_expansion = sorted(
        numerator_expansion,
        key=lambda x: str(len(x.split("*"))) + str(eval(x)))
    numerator_expansion = "|".join(numerator_expansion)

    denominator_expansion = [sort_basic_element(x) for x in expansion[1]]
    denominator_expansion = sorted(
        denominator_expansion,
        key=lambda x: str(len(x.split("*"))) + str(eval(x)))
    denominator_expansion = "|".join(denominator_expansion)

    return numerator_expansion + "/" + denominator_expansion


def test_multinomial_expand():
    left_expr = [['3*5', '3*2*4', '(-1)*7*10'], ['2', '2*2']]
    right_expr = [['2*4', '3', '4*(-1)'], ['10', '5*5', '5']]

    print(add_expression(left_expr, right_expr))
    print(mul_expression(left_expr, right_expr))
    print(sub_expression(left_expr, right_expr))
    print(div_expression(left_expr, right_expr))

    expression = '(((((((5*(10*((7*2)-1)))-5)*11- 5)*2)/2)*3)   - 5)'
    expansion = evaluate_arithmetic_expression(expression, lambda x: x.strip(),
                                               precedence, multinomial_expand)
    print(expansion)
    print(signature(expression))

    equi_expr_a = '(((10*5)*((7*2)-(1)))-(5))'
    equi_expr_b = '(((5)*((10)*((7*2)-(1))))-(5))'
    diff_expr_c = '((2+1)*((5)*((10*5)-(7))))'
    diff_expr_d = '((10*7 - 5) *2 - 1) * 5'

    print(signature(equi_expr_a))
    print(signature(equi_expr_b))
    print(signature(diff_expr_c))
    print(signature(diff_expr_d))


if __name__ == '__main__':
    #  test_multinomial_expand()
    print(signature('7*(5+2*2)'))
    print(signature('7*(5+2+2)'))
