"""
To complete the gravity assist, you need to determine what pair of inputs
produces the output 19690720."

The inputs should still be provided to the program by replacing the values at
addresses 1 and 2, just like before. In this program, the value placed in
address 1 is called the noun, and the value placed in address 2 is called the
verb. Each of the two input values will be between 0 and 99, inclusive.

Once the program has halted, its output is available at address 0, also just
like before. Each time you try a pair of inputs, make sure you first reset the
computer's memory to the values in the program (your puzzle input) - in other
words, don't reuse memory from a previous attempt.

Find the input noun and verb that cause the program to produce the output
19690720. What is 100 * noun + verb? (For example, if noun=12 and verb=2, the
answer would be 1202.)
"""
from itertools import product
import operator
from typing import List, Iterator

import pytest


OpCodes = List[int]


def run_opcodes(opcodes: OpCodes) -> OpCodes:
    """Calculate opcodes as per above"""
    opcodes = opcodes.copy()  # ensure we don't overwrite the original
    for i in range(0, len(opcodes), 4):
        if opcodes[i] == 99:
            break
        elif opcodes[i] == 1:
            op = operator.add
        elif opcodes[i] == 2:
            op = operator.mul
        else:
            raise ValueError(f"OpCode {opcodes[i]} is unknown")

        pos_a = opcodes[i + 1]
        pos_b = opcodes[i + 2]
        pos_out = opcodes[i + 3]

        opcodes[pos_out] = op(opcodes[pos_a], opcodes[pos_b])

    return opcodes


def initialise_opcodes() -> Iterator[OpCodes]:
    """Generator to get the next OpCode"""
    opcodes = [int(i) for i in open("input").read().split(",")]
    for noun, verb in product(range(100), repeat=2):
        opcodes[1] = noun
        opcodes[2] = verb

        yield opcodes


@pytest.mark.parametrize(
    "opcodes,result",
    [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ],
)
class TestOpCodes:
    def test_run_opcodes(self, opcodes: OpCodes, result: OpCodes):
        """Ensure opcodes calculate as required"""
        assert run_opcodes(opcodes) == result

    def test_run_opcodes_is_pure(self, opcodes: OpCodes, result: OpCodes):
        """Test to make sure that the initial value of opcodes is unmodified"""
        assert opcodes is not run_opcodes(opcodes)


def test_getting_opcode():
    assert isinstance(next(initialise_opcodes()), list)


def main():
    """Main operations"""
    for opcodes in initialise_opcodes():
        output_opcodes = run_opcodes(opcodes)
        if output_opcodes[0] == 19690720:
            print(100 * opcodes[1] + opcodes[2])
            break


if __name__ == "__main__":
    main()
