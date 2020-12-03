#!/usr/bin/env python
"""
Solution to day 13 part 2

Robot painting time
"""
import inspect
import logging
import threading
from typing import List, Callable
from queue import SimpleQueue

from defaultlist import defaultlist


OpCodes = List[int]


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] (%(threadName)-10s) %(message)s"
)


class Processor:
    """
    Storage enumerator for operations

    Operation inputs and outputs are counted to ensure the sequences
    advance at the correct pace
    """

    def __init__(
        self, input_queue: SimpleQueue, output_queue: SimpleQueue
    ):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.pointer = 0
        self.relative_base = 0

    @staticmethod
    def add(a: int, b: int) -> int:

        return a + b

    @staticmethod
    def mul(a: int, b: int) -> int:

        return a * b

    def input(self) -> int:
        """Wait for and get back a value from the input queue"""
        thread_name = threading.current_thread().getName()
        logging.debug(f"Waiting on signal in thread {thread_name}")
        signal = self.input_queue.get()
        logging.debug(f"Signal received in process {thread_name} ({signal})")
        return signal

    def output(self, val: int) -> None:
        """Output the value into the output queue"""
        thread_name = threading.current_thread().getName()
        logging.debug(f"{thread_name} writing to output queue ({val})")
        self.output_queue.put(val)

    def jump_if_true(self, a: int, b: int) -> bool:
        """Not a super fan of gotos..."""
        if a:
            logging.debug(f'jumping to {b}')
            self.pointer = b  # compensate for later pointer movement
            return True
        return False

    def jump_if_false(self, a: int, b: int) -> bool:
        if not a:
            logging.debug(f'jumping to {b}')
            self.pointer = b
            return True
        return False

    @staticmethod
    def less_than(a: int, b: int) -> int:
        if a < b:
            return 1
        return 0

    @staticmethod
    def equals(a: int, b: int) -> int:
        if a == b:
            return 1
        return 0

    def adjust_relaative_base(self, val: int) -> None:
        """Move the relative base"""
        self.relative_base += val


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
            8: self.equals,
            9: self.adjust_relaative_base,
        }
        idx = (
            key % 100
        )  # opcodes are last two digets. Might be more later in the comp...

        return lookup[idx]

    def __call__(self, ops: OpCodes) -> OpCodes:

        opcodes = defaultlist(lambda: 0)
        opcodes.extend(ops)

        while True:

            while self.pointer < len(opcodes):
                logging.debug(opcodes)
                logging.debug(f'pointer {self.pointer}')

                advance_position = 1  # always advance position by at least one

                if opcodes[self.pointer] == 99:

                    return opcodes

                logging.debug(f'opcode {opcodes[self.pointer]}')

                op = self[opcodes[self.pointer]]
                logging.debug(f'op {op}')
                signature = inspect.signature(op)

                params = {}  # to store operation arguments as keywords

                param_names = list(signature.parameters)
                logging.debug(param_names)

                for j, param in enumerate(param_names, start=1):
                    # get last digit as an integer after removing the actual operation code
                    mode = (opcodes[self.pointer] // 10 ** (j + 1)) % 10

                    if mode == 0:  # positional mode
                        params[param] = opcodes[opcodes[self.pointer + j]]
                    elif mode == 1:  # immediate mode
                        params[param] = opcodes[self.pointer + j]
                    elif mode == 2:  # relative mode
                        params[param] = opcodes[opcodes[self.pointer + j] + self.relative_base]
                    else:
                        raise ValueError(f"Mode {mode} not recognised")

                advance_position += len(param_names)

                logging.debug(f'params {params}')
                result = op(**params)
                logging.debug(f"result {result}")
                if result and op in (self.jump_if_false, self.jump_if_true):
                    logging.debug("don't jump")
                    # don't advance pointer if the gotos worked
                    continue

                # TODO: make sure return annotation is None when required
                if signature.return_annotation and op not in (self.jump_if_false, self.jump_if_true):
                    mode = (opcodes[self.pointer] // 10 ** (len(param_names) + 2)) % 10
                    if mode == 0:
                        opcodes[opcodes[self.pointer + len(param_names) + 1]] = result
                    elif mode == 2:
                        opcodes[opcodes[self.pointer + len(param_names) + 1] + self.relative_base] = result
                    else:
                        raise ValueError("Output position not recognised")

                    advance_position += 1

                # finally, make sure the loop advances
                self.pointer += advance_position


def maze_solver(opcodes: OpCodes) -> int:
    """
    Find the location of the repair point (return signal 2)

    Return the shortest path trough the network to thaat point.
    """
    input_queue = SimpleQueue()
    output_queue = SimpleQueue()
    processor = Processor(input_queue, output_queue)




def main():
    """Main operations"""

    opcodes = [int(i) for i in open("input").read().split(",")]


if __name__ == "__main__":
    main()
