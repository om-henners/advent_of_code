#!/usr/bin/env python
"""Test for solution part 1
"""
from queue import SimpleQueue

import pytest

import solution1


@pytest.fixture
def create_processor():
    """Create a new processor with associated queues"""
    input_queue = SimpleQueue()
    output_queue = SimpleQueue()

    processor = solution1.Processor(input_queue, output_queue)
    return processor, input_queue, output_queue


def test_first_opcode(create_processor):
    """Test the opcodess that returns itself"""
    opcodes = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]

    processor, input_queue, output_queue = create_processor

    output = processor(opcodes)

    q_results = []

    while not output_queue.empty():
        q_results.append(output_queue.get())

    assert opcodes is not output
    assert opcodes == q_results


def test_second_opcode(create_processor):
    """Test the second opcode returns a 16 digit number"""
    opcodes = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]

    processor, input_queue, output_queue = create_processor

    processor(opcodes)

    response = output_queue.get()

    assert response >= 1_000_000_000_000_000


def test_third_opcode(create_processor):
    opcodes = [104, 1125899906842624, 99]

    processor, input_queue, output_queue = create_processor

    processor(opcodes)

    response = output_queue.get()

    assert response == opcodes[1]
