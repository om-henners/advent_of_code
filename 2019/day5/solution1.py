"""The Thermal Environment Supervision Terminal (TEST) starts by running
a diagnostic program (your puzzle input). The TEST diagnostic program
will run on your existing Intcode computer after a few modifications:

First, you'll need to add two new instructions:

- Opcode 3 takes a single integer as input and saves it to the
  position given by its only parameter. For example, the instruction
  3,50 would take an input value and store it at address 50.
- Opcode 4 outputs the value of its only parameter. For example, the
  instruction 4,50 would output the value at address 50.

Programs that use these instructions will come with documentation that
explains what should be connected to the input and output. The program
3,0,4,0,99 outputs whatever it gets as input, then halts.

Second, you'll need to add support for parameter modes:

Each parameter of an instruction is handled based on its parameter
mode. Right now, your ship computer already understands parameter mode
0, position mode, which causes the parameter to be interpreted as a
position - if the parameter is 50, its value is the value stored at
address 50 in memory. Until now, all parameters have been in position
mode.

Now, your ship computer will also need to handle parameters in mode 1,
immediate mode. In immediate mode, a parameter is interpreted as a
value - if the parameter is 50, its value is simply 50.

Parameter modes are stored in the same value as the instruction's
opcode. The opcode is a two-digit number based only on the ones and
tens digit of the value, that is, the opcode is the rightmost two
digits of the first value in an instruction. Parameter modes are
single digits, one per parameter, read right-to-left from the opcode:
the first parameter's mode is in the hundreds digit, the second
parameter's mode is in the thousands digit, the third parameter's mode
is in the ten-thousands digit, and so on. Any missing modes are 0.
"""
import inspect
from typing import List, Callable


OpCodes = List[int]


class OperationEnum:
    """
    Storage enumerator for operations

    Operation inputs and outputs are counted to ensure the sequences
    advance at the correct pace
    """

    @staticmethod
    def add(a: int, b: int) -> int:

        return a + b

    @staticmethod
    def mul(a: int, b: int) -> int:

        return a * b

    @staticmethod
    def input() -> int:

        return int(input('Please enter input'))

    @staticmethod
    def output(val: int) -> None:
        print(val)

    def __getitem__(self, key: int) -> Callable:
        """The operation reference is always the last digit. So mod
        the key by 10, and return the matching callable.
        """
        lookup = {
            1: self.add,
            2: self.mul,
            3: self.input,
            4: self.output
        }
        idx = key % 100  # opcodes are last two digets. Might be more later in the comp...

        return lookup[idx]


def run_opcodes(opcodes: OpCodes) -> OpCodes:
    """Calculate opcodes as per above"""
    opcodes = opcodes.copy()  # ensure we don't overwrite the original
    i = 0

    operations = OperationEnum()

    while i < len(opcodes):

        advance_position = 1

        if opcodes[i] == 99:
            break

        op = operations[opcodes[i]]
        signature = inspect.signature(op)

        params = {}  # to store operation arguments as keywords

        for j, param in enumerate(signature.parameters, start=1):

            mode = (opcodes[i] // 10 ** (j + 1)) % 10

            if mode == 0:
                params[param] = opcodes[opcodes[i + j]]
            elif mode == 1:
                params[param] = opcodes[i + j]
            else:
                raise ValueError(f'Mode {mode} not recognised')

        advance_position += len(signature.parameters)

        result = op(**params)
        if signature.return_annotation:  # make sure return annotation is None when required

            opcodes[opcodes[i + len(signature.parameters) + 1]] = result
            advance_position += 1

        # finally, make sure the loop advaances
        i += advance_position

    return opcodes


def main():
    """Main operations"""
    opcodes = [int(i) for i in open('input').read().split(',')]

    output_opcodes = run_opcodes(opcodes)


if __name__ == '__main__':
    main()
