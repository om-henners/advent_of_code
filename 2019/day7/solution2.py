#!/usr/bin/env python
"""Solution to part 1

There are five amplifiers connected in series; each one receives an input signal and produces an output signal. They are connected such that the first amplifier's output leads to the second amplifier's input, the second amplifier's output leads to the third amplifier's input, and so on. The first amplifier's input value is 0, and the last amplifier's output leads to your ship's thrusters.
"""
from collections import deque
import concurrent.futures
from functools import partial
import inspect
import itertools
import logging
import threading
import string
from typing import List, Callable, Tuple
from queue import SimpleQueue


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
        self, opcodes: OpCodes, input_queue: SimpleQueue, output_queue: SimpleQueue
    ):
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

        while True:
            opcodes = self.opcodes
            #self.pointer = 0
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

                    opcodes[opcodes[self.pointer + len(param_names) + 1]] = result
                    advance_position += 1

                # finally, make sure the loop advances
                self.pointer += advance_position


def get_thruster_signal(control_sequence: OpCodes, phase_setting: OpCodes) -> int:
    """
    Create the amplifiers and link them together with input and output queues
    """
    communication_queues = deque([SimpleQueue() for _ in range(len(phase_setting))])
    threads = []
    for i, phase in enumerate(phase_setting):
        input_queue = communication_queues[0]
        communication_queues.rotate(-1)  # move onto the next communication channel
        output_queue = communication_queues[0]
        input_queue.put(phase)

        processor = Processor(control_sequence, input_queue, output_queue)
        amplifier = threading.Thread(
            target=processor,
            name="Amplifier-{}".format(string.ascii_uppercase[i]),
            daemon=True,
        )
        threads.append(amplifier)
        amplifier.start()

    communication_queues[0].put(0)  # manually enter the first signal

    threads[-1].join(timeout=10)
    if threads[-1].is_alive():
        logging.error(threads)
        raise RuntimeError("Thread did not terminate")

    # output queue for last amplifier is the input for queue A
    signal = communication_queues[0].get()
    return signal, phase_setting


def find_max_thruster_signal(control_sequence: OpCodes) -> Tuple[OpCodes, int]:
    """
    Trial all the possible phase settings and determine the best
    """
    # signal_settings = {}

    # for phase_setting in itertools.permutations(range(5, 10), 5):
    #     logging.debug(phase_setting)
    #     signal = get_thruster_signal(control_sequence, phase_setting)
    #     signal_settings[signal] = list(phase_setting)

    thruster_signal = partial(get_thruster_signal, control_sequence)

    ex = concurrent.futures.ThreadPoolExecutor()
    results = ex.map(thruster_signal, itertools.permutations(range(5, 10), 5))

    signal_settings = dict(results)
    best_signal = max(signal_settings)

    return signal_settings[best_signal], best_signal


def main():
    """Main operations"""

    opcodes = [int(i) for i in open("input").read().split(",")]
    phase_setting, signal = find_max_thruster_signal(opcodes)
    logging.info(phase_setting)
    logging.info(signal)


if __name__ == "__main__":
    main()
