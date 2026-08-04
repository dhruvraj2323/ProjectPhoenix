"""
=================================================
Project Phoenix
Continuous Runner Test
M58
=================================================
"""

from deployment.continuous_runner import (
    ContinuousRunner,
)


def test_continuous_runner():

    runner = ContinuousRunner(
        interval=1,
    )

    assert runner.running is False

    runner.start(
        cycles=1,
    )

    assert runner.running is False

    assert runner.run_once() is True