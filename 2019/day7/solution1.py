#!/usr/bin/env python
"""Solution to part 1

There are five amplifiers connected in series; each one receives an input signal and produces an output signal. They are connected such that the first amplifier's output leads to the second amplifier's input, the second amplifier's output leads to the third amplifier's input, and so on. The first amplifier's input value is 0, and the last amplifier's output leads to your ship's thrusters.
"""
import concurrent.futures
import inspect
import itertools
import logging
import threading
from typing import List, Callable, Tuple
from queue import SimpleQueue


OpCodes = List[int]


logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)


class Processor:
    """
    Storage enumerator for operations

    Operation inputs and outputs are counted to ensure the sequences
    advance at the correct pace
    """

    def __init__(self, opcodes: OpCodes, input_queue: SimpleQueue, output_queue: SimpleQueue):
        self.opcodes = opcodes.copy()
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.pointer = 0

    @staticmethod
    def add(a: int, b: int) -> int:

        return a + b

    @staticmethod
    def mul(a: int, b: int) -> int:

        return a * b

    def input(self) -> int:
        """Wait for and get back a value from the input queue"""
        thread_name = threading.current_thread().getName()
        logging.debug(f'Waiting on signal in thread {thread_name}')
        signal = self.input_queue.get()
        logging.debug(f'Signal received in process {thread_name} ({signal})')
        return signal

    def output(self, val: int) -> None:
        """Output the value into the output queue"""
        thread_name = threading.current_thread().getName()
        logging.debug(f'{thread_name} writing to output queue')
        self.output_queue.put(val)

    def jump_if_true(self, a: int, b: int) -> bool:
        """Not a super fan of gotos..."""
        if a:
            self.pointer = b  # compensate for later pointer movement
            return True
        return False

    def jump_if_false(self, a: int, b: int) -> bool:
        if not a:
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
        }
        idx = (
            key % 100
        )  # opcodes are last two digets. Might be more later in the comp...

        return lookup[idx]

    def __call__(self) -> OpCodes:

        while self.pointer < len(self.opcodes):
            logging.debug(self.opcodes)

            advance_position = 1  # always advance position by at least one

            if self.opcodes[self.pointer] == 99:
                break

            op = self[self.opcodes[self.pointer]]
            signature = inspect.signature(op)

            params = {}  # to store operation arguments as keywords

            param_names = list(signature.parameters)
            logging.debug(param_names)
            # if param_names and param_names[0] == 'self':  # don't count the self parameter
            #     param_names = param_names[1:]

            for j, param in enumerate(param_names, start=1):

                mode = (self.opcodes[self.pointer] // 10 ** (j + 1)) % 10  # get last digit as an integer after removing the actual operation code

                if mode == 0:  # positional mode
                    params[param] = self.opcodes[self.opcodes[self.pointer + j]]
                elif mode == 1:  # immediate mode
                    params[param] = self.opcodes[self.pointer + j]
                else:
                    raise ValueError(f'Mode {mode} not recognised')

            advance_position += len(param_names)

            logging.debug(params)
            result = op(**params)
            logging.debug(f'result {result}')
            if signature.return_annotation:  # TODO: make sure return annotation is None when required

                self.opcodes[self.opcodes[self.pointer + len(param_names) + 1]] = result
                advance_position += 1

            if result and op in (self.jump_if_false, self.jump_if_true):
                # don't advance pointer if the gotos worked
                continue

            # finally, make sure the loop advances
            self.pointer += advance_position

        return self.opcodes


def get_thruster_signal(control_sequence: OpCodes, phase_setting: OpCodes) -> int:
    """
    Create the amplifiers and link them together with input and output queues
    """
    communication_queues = [
        SimpleQueue() for _ in range(len(phase_setting) + 1)
    ]
    threads = []
    for i, phase in enumerate(phase_setting):
        input_queue = communication_queues[i]
        output_queue = communication_queues[i + 1]
        input_queue.put(phase)

        processor = Processor(control_sequence, input_queue, output_queue)
        amplifier = threading.Thread(target=processor)
        threads.append(amplifier)
        amplifier.start()

    communication_queues[0].put(0)  # manually enter the first signal

    signal = communication_queues[-1].get()
    return signal


def find_max_thruster_signal(control_sequence: OpCodes) -> Tuple[OpCodes, int]:
    """
    Trial all the possible phase settings and determine the best
    """
    signal_settings = {}

    for phase_setting in itertools.permutations(range(5), 5):
        signal = get_thruster_signal(control_sequence, phase_setting)
        signal_settings[signal] = list(phase_setting)

    best_signal = max(signal_settings)
    return signal_settings[best_signal], best_signal


def main():
    """Main operations"""

    opcodes = [int(i) for i in open('input').read().split(',')]

    phase_setting, signal = find_max_thruster_signal(opcodes)
    logging.info(phase_setting)
    logging.info(signal)


if __name__ == '__main__':
    main()
