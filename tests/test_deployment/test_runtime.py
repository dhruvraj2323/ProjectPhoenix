"""
=================================================
Project Phoenix
Runtime Test
M58
=================================================
"""

from deployment.runtime import (
    Runtime,
)


def test_runtime():

    runtime = Runtime()

    assert runtime.running is False

    runtime.start()

    assert runtime.running is True

    runtime.stop()

    assert runtime.running is False