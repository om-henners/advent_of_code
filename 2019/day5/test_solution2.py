"""
Tests for solution 2 day 5
"""
import inspect
import pytest

import solution2


@pytest.mark.parametrize(
    "opcodes,result",
    [([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]), ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]), ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]), ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]), ([1002, 4, 3, 4, 33], [1002, 4, 3, 4, 99]),],
)
class TestOpCodes:
    def test_run_opcodes(self, opcodes: solution2.OpCodes, result: solution2.OpCodes):
        """Ensure opcodes calculate as required"""
        processor = solution2.Processor()
        assert processor(opcodes) == result

    def test_run_opcodes_is_pure(self, opcodes: solution2.OpCodes, result: solution2.OpCodes):
        """Test to make sure that the initial value of opcodes is unmodified"""
        processor = solution2.Processor()
        assert opcodes is not processor(opcodes)


@pytest.mark.parametrize(
    "program, comparison, expected",
    [
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8, 1),  # equal
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 7, 0),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 9, 0),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 8, 0),  # less than
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 7, 1),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 9, 0),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 8, 1),  # equal
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 7, 0),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 9, 0),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 8, 0),  # less than
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 7, 1),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 9, 0),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0, 0,),  # zero if position
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 1, 1,),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0, 0),  # zero if immediate
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 1, 1),
        ([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99,], 7, 999,),
        ([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99,], 8, 1000,),
        ([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99,], 9, 1001,),
    ],
)
def test_jumping(program: solution2.OpCodes, comparison: int, expected: int, monkeypatch):
    """
    Override the input and print functions with monkeypatch to control input and
    output
    """
    monkeypatch.setattr("builtins.input", lambda msg: comparison)
    result_output = []
    monkeypatch.setattr("builtins.print", lambda val: result_output.append(val))

    processor = solution2.Processor()
    processor(program)
    assert result_output[0] == expected


@pytest.mark.parametrize("opcode,num_params", [(1, 3), (2, 3), (3, 1), (4, 1), (1001, 3), (1004, 1)])
def test_get_operation(opcode, num_params):
    """
    Theory is to implement the operations as a class with staticmethods and
    a getitem method that gets the appropriate operation.

    For operations with different opcodes the operations returned should have
    the correct number of parameters.

    Functions are inspected for the number of input parameters and the return
    signature - the total is used to determine parameter numbers.
    """
    processor = solution2.Processor()
    signature = inspect.signature(processor[opcode])
    sig_length = len(signature.parameters)
    if "self" in signature.parameters:
        sig_length -= 1
    if not (signature.return_annotation is None or signature.return_annotation is inspect.Signature.empty):
        sig_length += 1
    assert sig_length == num_params
