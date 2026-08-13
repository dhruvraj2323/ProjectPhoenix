"""
=================================================
Project Phoenix
Bootstrap Tests
M61.6.3 - Runtime Readiness Integration
=================================================
"""

from unittest.mock import MagicMock

from deployment.bootstrap import (
    Bootstrap,
)


# =========================================================
# Test A
# Healthy Runtime Starts Bootstrap
# =========================================================

def test_bootstrap_start():

    runtime = MagicMock()

    runtime.start.return_value = True

    bootstrap = Bootstrap(
        runtime=runtime,
    )

    assert bootstrap.started is False

    result = bootstrap.start(
        cycles=1,
    )

    assert result is True

    assert bootstrap.started is True

    runtime.start.assert_called_once_with(
        cycles=1,
    )


# =========================================================
# Test B
# Unhealthy Runtime Blocks Bootstrap
# =========================================================

def test_bootstrap_start_blocked():

    runtime = MagicMock()

    runtime.start.return_value = False

    bootstrap = Bootstrap(
        runtime=runtime,
    )

    result = bootstrap.start(
        cycles=1,
    )

    assert result is False

    assert bootstrap.started is False

    runtime.start.assert_called_once_with(
        cycles=1,
    )


# =========================================================
# Test C
# Bootstrap Stop
# =========================================================

def test_bootstrap_stop():

    runtime = MagicMock()

    runtime.start.return_value = True

    bootstrap = Bootstrap(
        runtime=runtime,
    )

    bootstrap.start(
        cycles=1,
    )

    result = bootstrap.stop()

    assert result is True

    assert bootstrap.started is False

    runtime.stop.assert_called_once()


# =========================================================
# Test D
# Stop Before Start
# =========================================================

def test_bootstrap_stop_before_start():

    runtime = MagicMock()

    bootstrap = Bootstrap(
        runtime=runtime,
    )

    result = bootstrap.stop()

    assert result is False

    runtime.stop.assert_not_called()

    assert bootstrap.started is False


# =========================================================
# Test E
# Bootstrap Can Restart After Stop
# =========================================================

def test_bootstrap_restart_flow():

    runtime = MagicMock()

    runtime.start.return_value = True

    bootstrap = Bootstrap(
        runtime=runtime,
    )

    assert (
        bootstrap.start(
            cycles=1,
        )
        is True
    )

    assert bootstrap.started is True

    assert (
        bootstrap.stop()
        is True
    )

    assert bootstrap.started is False

    assert (
        bootstrap.start(
            cycles=1,
        )
        is True
    )

    assert bootstrap.started is True

    assert (
        runtime.start.call_count
        == 2
    )