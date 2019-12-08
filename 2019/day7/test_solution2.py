#!/usr/bin/env python
"""
Test for problem 2, day 7

The key in this task will be to use queues for input and output rather than input and print statements. Then in practice we can usse threads to manage the amplifiers.
"""
import pytest

import solution2


@pytest.mark.parametrize(
    "control_sequence, phase_setting, thruster_signal",
    [
        (
            [
                3,
                26,
                1001,
                26,
                -4,
                26,
                3,
                27,
                1002,
                27,
                2,
                27,
                1,
                27,
                26,
                27,
                4,
                27,
                1001,
                28,
                -1,
                28,
                1005,
                28,
                6,
                99,
                0,
                0,
                5,
            ],
            [9, 8, 7, 6, 5],
            139629729,
        ),
        (
            [
                3,
                52,
                1001,
                52,
                -5,
                52,
                3,
                53,
                1,
                52,
                56,
                54,
                1007,
                54,
                5,
                55,
                1005,
                55,
                26,
                1001,
                54,
                -5,
                54,
                1105,
                1,
                12,
                1,
                53,
                54,
                53,
                1008,
                54,
                0,
                55,
                1001,
                55,
                1,
                55,
                2,
                53,
                55,
                53,
                4,
                53,
                1001,
                56,
                -1,
                56,
                1005,
                56,
                6,
                99,
                0,
                0,
                0,
                0,
                10,
            ],
            [9, 7, 8, 5, 6],
            18216,
        ),
    ],
)
class TestThrusters:
    def test_thruster_signal(self, control_sequence, phase_setting, thruster_signal):
        """
        Test given a sequence and phase setting the correct thruster signal is returned
        """

        assert (
            solution2.get_thruster_signal(control_sequence, phase_setting)
            == thruster_signal, phase_setting
        )

    def test_find_max_thruster_signal(
        self, control_sequence, phase_setting, thruster_signal
    ):

        predicted_phase_setting, predicted_thruster_signal = solution2.find_max_thruster_signal(
            control_sequence
        )

        assert list(predicted_phase_setting) == phase_setting
        assert predicted_thruster_signal == thruster_signal
