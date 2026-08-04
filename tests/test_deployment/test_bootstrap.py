"""
=================================================
Project Phoenix
Bootstrap Test
M58
=================================================
"""

from deployment.bootstrap import (
    Bootstrap,
)


def test_bootstrap():

    bootstrap = Bootstrap()

    assert bootstrap.started is False

    bootstrap.started = True

    bootstrap.stop()

    assert bootstrap.started is False