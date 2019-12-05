"""
Tests for solution 1 day 5
"""
import inspect
import pytest

import solution1


@pytest.mark.parametrize(
    "opcodes,result",
    [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
        ([1002, 4, 3, 4, 33], [1002, 4, 3, 4, 99]),
    ],
)
class TestOpCodes:
    def test_run_opcodes(self, opcodes: solution1.OpCodes, result: solution1.OpCodes):
        """Ensure opcodes calculate as required"""
        assert solution1.run_opcodes(opcodes) == result

    def test_run_opcodes_is_pure(
        self, opcodes: solution1.OpCodes, result: solution1.OpCodes
    ):
        """Test to make sure that the initial value of opcodes is unmodified"""
        assert opcodes is not solution1.run_opcodes(opcodes)


@pytest.mark.parametrize(
    "opcode,num_params",
    [
        (1, 3),
        (2, 3),
        (3, 1),
        (4, 1),
        (1001, 3),
        (1004, 1)
    ]
)
def test_get_operation(opcode, num_params):
    """
    Theory is to implement the operations as a class with staticmethods and
    a getitem method that gets the appropriate operation.

    For operations with different opcodes the operations returned should have
    the correct number of parameters.

    Functions are inspected for the number of input parameters and the return
    signature - the total is used to determine parameter numbers.
    """
    signature = inspect.signature(
        solution1.OperationEnum()[opcode]
    )
    sig_length = len(signature.parameters)
    if not (signature.return_annotation is None or
            signature.return_annotation is inspect.Signature.empty):
        sig_length += 1
    assert sig_length == num_params
