#!/usr/bin/env python
"""
Test for problem 1, day 7

The key in this task will be to use queues for input and output rather than input and print statements. Then in practice we can usse threads to manage the amplifiers.
"""
import pytest

import solution1

@pytest.mark.parametrize(
    "control_sequence, phase_setting, thruster_signal",
    [
        (
            [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0],
            [4, 3, 2, 1, 0],
            43210,
        ),
        (
            [
                3,
                23,
                3,
                24,
                1002,
                24,
                10,
                24,
                1002,
                23,
                -1,
                23,
                101,
                5,
                23,
                23,
                1,
                24,
                23,
                23,
                4,
                23,
                99,
                0,
                0,
            ],
            [0, 1, 2, 3, 4],
            54321,
        ),
        (
            [
                3,
                31,
                3,
                32,
                1002,
                32,
                10,
                32,
                1001,
                31,
                -2,
                31,
                1007,
                31,
                0,
                33,
                1002,
                33,
                7,
                33,
                1,
                33,
                31,
                31,
                1,
                32,
                31,
                31,
                4,
                31,
                99,
                0,
                0,
                0,
            ],
            [1, 0, 4, 3, 2],
            65210,
        ),
    ],
)
class TestThrusters:
    def test_thruster_signal(self, control_sequence, phase_setting, thruster_signal):
        """
        Test given a sequence and phase setting the correct thruster signal is returned
        """

        assert (
            solution1.get_thruster_signal(control_sequence, phase_setting)
            == thruster_signal, phase_setting
        )

    def test_find_max_thruster_signal(self, control_sequence, phase_setting, thruster_signal):

        predicted_phase_setting, predicted_thruster_signal = solution1.find_max_thruster_signal(
            control_sequence
        )

        assert predicted_phase_setting == phase_setting
        assert predicted_thruster_signal == thruster_signal
