from operator import or_
from functools import reduce

import numpy as np
from parse import parse


REGISTER = np.zeros(4, dtype=np.int64)


class Addition:

    @staticmethod
    def addr(input_a, input_b, output):
        """Add register"""
        REGISTER[output] = REGISTER[[input_a, input_b]].sum()

    @staticmethod
    def addi(input_a, input_b, output):
        """Add immediate"""
        REGISTER[output] = REGISTER[input_a] + input_b


class Multiplication:

    @staticmethod
    def mulr(input_a, input_b, output):
        """multiply register"""
        REGISTER[output] = REGISTER[[input_a, input_b]].prod()

    @staticmethod
    def muli(input_a, input_b, output):
        """multiply immediate"""
        REGISTER[output] = REGISTER[input_a] * input_b


class BitwiseAND:

    @staticmethod
    def banr(input_a, input_b, output):
        """bitwise AND register"""
        REGISTER[output] = np.bitwise_and(*REGISTER[[input_a, input_b]])

    @staticmethod
    def bani(input_a, input_b, output):
        """bitwise AND immediate"""
        REGISTER[output] = np.bitwise_and(REGISTER[input_a], input_b)


class BitwiseOR:

    @staticmethod
    def borr(input_a, input_b, output):
        """bitwise OR register"""
        REGISTER[output] = np.bitwise_or(*REGISTER[[input_a, input_b]])

    @staticmethod
    def bori(input_a, input_b, output):
        """bitwise OR immediate"""
        REGISTER[output] = np.bitwise_or(REGISTER[input_a], input_b)


class Assignment:

    @staticmethod
    def setr(input_a, input_b, output):
        """set register"""
        REGISTER[output] = REGISTER[input_a]

    @staticmethod
    def seti(input_a, input_b, output):
        """set immediate"""
        REGISTER[output] = input_a


class GreaterThan:

    @staticmethod
    def gtir(input_a, input_b, output):
        """greater-than immediate/register"""
        REGISTER[output] = 1 if input_a > REGISTER[input_b] else 0

    @staticmethod
    def gtri(input_a, input_b, output):
        """greater-than register/immediate"""
        REGISTER[output] = 1 if REGISTER[input_a] > input_b else 0

    @staticmethod
    def gtrr(input_a, input_b, output):
        """greater=than register/register"""
        REGISTER[output] = 1 if REGISTER[input_a] > REGISTER[input_b] else 0


class Equality:

    @staticmethod
    def eqir(input_a, input_b, output):
        """equal immediate/register"""
        REGISTER[output] = 1 if input_a == REGISTER[input_b] else 0

    @staticmethod
    def eqri(input_a, input_b, output):
        """equal register/immediate"""
        REGISTER[output] = 1 if REGISTER[input_a] == input_b else 0

    @staticmethod
    def eqrr(input_a, input_b, output):
        """equal register/register"""
        REGISTER[output] = 1 if REGISTER[input_a] == REGISTER[input_b] else 0


ALL_METHODS = {
    Addition.addr, Addition.addi,
    Multiplication.mulr, Multiplication.muli,
    BitwiseAND.banr, BitwiseAND.bani,
    BitwiseOR.borr, BitwiseOR.bori,
    Assignment.setr, Assignment.seti,
    GreaterThan.gtir, GreaterThan.gtri, GreaterThan.gtrr,
    Equality.eqir, Equality.eqri, Equality.eqrr
}

OPCODES = {
    i: ALL_METHODS.copy()
    for i in range(16)
}


data = open('input.txt').read()
part_1_data, part_2_data = data.split('\n\n\n\n')

possible_ops = []
for params in part_1_data.split('\n\n'):

    r = parse('Before: [{rb_0:d}, {rb_1:d}, {rb_2:d}, {rb_3:d}]\n{o_i:d} {a_i:d} {b_i:d} {c_i:d}\nAfter:  [{ab_0:d}, {ab_1:d}, {ab_2:d}, {ab_3:d}]', params)

    result = np.array([r['ab_0'], r['ab_1'], r['ab_2'], r['ab_3']])

    successes = set()
    for method in ALL_METHODS:
        REGISTER[:] = r['rb_0'], r['rb_1'], r['rb_2'], r['rb_3']

        method(r['a_i'], r['b_i'], r['c_i'])

        if (REGISTER == result).all():
            successes.add(method)

    possible_ops.append(len(successes))
    OPCODES[r['o_i']] &= successes

print('Solution 1:', np.bincount(possible_ops)[3:].sum())


more_than_one_op = [len(ops) > 1 for ops in OPCODES.values()]
while np.any(more_than_one_op):

    correct_ops = reduce(or_, (ops for ops in OPCODES.values() if len(ops) == 1), set())

    for k in OPCODES:
        if len(OPCODES[k]) > 1:
            OPCODES[k] -= correct_ops

    more_than_one_op = [len(ops) > 1 for ops in OPCODES.values()]


OPCODES = {k: v.pop() for k, v in OPCODES.items()}


REGISTER[:] = [0, 0, 0, 0]

for line in part_2_data.rstrip('\n').split('\n'):
    r = parse('{o:d} {a:d} {b:d} {c:d}', line)
    OPCODES[r['o']](r['a'], r['b'], r['c'])

print('Solution 2:', REGISTER[0])
