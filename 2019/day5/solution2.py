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
import types
from typing import List, Callable


OpCodes = List[int]


class Processor:
    """
    Storage enumerator for operations

    Operation inputs and outputs are counted to ensure the sequences
    advance at the correct pace
    """
    pointer = 0

    @staticmethod
    def add(a: int, b: int) -> int:

        return a + b

    @staticmethod
    def mul(a: int, b: int) -> int:

        return a * b

    @staticmethod
    def input() -> int:

        return int(input('Please enter input '))

    @staticmethod
    def output(val: int) -> None:
        print(val)

    def jump_if_true(self, a: int, b: int) -> None:
        """Not a super fan of gotos..."""
        if a:
            self.pointer = b  # compensate for later pointer movement
            return True

    def jump_if_false(self, a: int, b: int) -> None:
        if not a:
            self.pointer = b
            return True

    @staticmethod
    def less_than(a: int, b:int) -> int:
        if a < b:
            return 1
        return 0

    @staticmethod
    def equals(a: int, b:int) -> int:
        if a == b:
            return 1
        return 0

    def __getitem__(self, key: int) -> Callable:
        """The operation reference is always the last digit. So mod
        the key by 10, and return the matching callable.
        """
        lookup = {
            1: self.add,
            2: self.mul,
            3: self.input,
            4: self.output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals
        }
        idx = key % 100  # opcodes are last two digets. Might be more later in the comp...

        return lookup[idx]

    def __call__(self, opcodes: OpCodes) -> OpCodes:
        # first, guarantee pointer is at zero
        self.pointer = 0
        opcodes = opcodes.copy()  # ensure we don't overwrite the original

        while self.pointer < len(opcodes):

            advance_position = 1  # always advance position by at least one

            if opcodes[self.pointer] == 99:
                break

            op = self[opcodes[self.pointer]]
            signature = inspect.signature(op)

            params = {}  # to store operation arguments as keywords

            param_names = list(signature.parameters)
            # if param_names and param_names[0] == 'self':  # don't count the self parameter
            #     param_names = param_names[1:]

            for j, param in enumerate(param_names, start=1):

                mode = (opcodes[self.pointer] // 10 ** (j + 1)) % 10  # get last digit as an integer after removing the actual operation code

                if mode == 0:  # positional mode
                    params[param] = opcodes[opcodes[self.pointer + j]]
                elif mode == 1:  # immediate mode
                    params[param] = opcodes[self.pointer + j]
                else:
                    raise ValueError(f'Mode {mode} not recognised')

            advance_position += len(param_names)

            result = op(**params)
            if signature.return_annotation:  # TODO: make sure return annotation is None when required

                opcodes[opcodes[self.pointer + len(param_names) + 1]] = result
                advance_position += 1

            if isinstance(op, types.MethodType) and result:
                continue
            # finally, make sure the loop advances
            self.pointer += advance_position

        return opcodes


def main():
    """Main operations"""
    opcodes = [int(i) for i in open('input').read().split(',')]

    processor = Processor()
    processor(opcodes)


if __name__ == '__main__':
    main()
