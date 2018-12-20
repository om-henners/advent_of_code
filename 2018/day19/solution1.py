import numpy as np
from parse import parse


REGISTER = np.zeros(6, dtype=np.int64)


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
    method.__name__: method
    for method in ALL_METHODS
}


with open('input.txt') as data:
    r = parse('#ip {pointer:d}', data.readline().strip())
    pointer = r['pointer']

    lines = data.readlines()

idx = 0
# solution 2
REGISTER[0] = 1
try:
    while True:
        line = lines[idx].strip()
        r = parse('{fn} {a:d} {b:d} {c:d}', line)
        REGISTER[pointer] = idx

        OPCODES[r['fn']](r['a'], r['b'], r['c'])

        idx = REGISTER[pointer] + 1

        print(REGISTER)

except IndexError:
    print(REGISTER)