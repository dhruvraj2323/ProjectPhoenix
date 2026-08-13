"""
=================================================
Project Phoenix
Runtime Tests
M61.6.2 - Deployment Readiness Gate
=================================================
"""

from unittest.mock import MagicMock

from deployment.runtime import (
    Runtime,
)


# =========================================================
# Test A
# Healthy Runtime Starts
# =========================================================

def test_runtime_start():

    runtime = Runtime(
        interval=0,
    )

    runtime.health_monitor = (
        MagicMock()
    )

    runtime.health_monitor.is_healthy.return_value = (
        True
    )

    runtime.continuous_runner = (
        MagicMock()
    )

    result = runtime.start(
        cycles=1,
    )

    assert result is True

    assert (
        runtime.health_monitor.is_healthy.call_count
        == 1
    )

    runtime.continuous_runner.start.assert_called_once_with(
        cycles=1,
    )

    assert runtime.running is True


# =========================================================
# Test B
# Unhealthy Runtime Is Blocked
# =========================================================

def test_runtime_start_blocked_when_unhealthy():

    runtime = Runtime(
        interval=0,
    )

    runtime.health_monitor = (
        MagicMock()
    )

    runtime.health_monitor.is_healthy.return_value = (
        False
    )

    runtime.continuous_runner = (
        MagicMock()
    )

    result = runtime.start(
        cycles=1,
    )

    assert result is False

    assert (
        runtime.health_monitor.is_healthy.call_count
        == 1
    )

    runtime.continuous_runner.start.assert_not_called()

    assert runtime.running is False


# =========================================================
# Test C
# Readiness Helper
# =========================================================

def test_runtime_is_ready():

    runtime = Runtime(
        interval=0,
    )

    runtime.health_monitor = (
        MagicMock()
    )

    runtime.health_monitor.is_healthy.return_value = (
        True
    )

    assert (
        runtime.is_ready()
        is True
    )

    runtime.health_monitor.is_healthy.return_value = (
        False
    )

    assert (
        runtime.is_ready()
        is False
    )


# =========================================================
# Test D
# Stop Runtime
# =========================================================

def test_runtime_stop():

    runtime = Runtime(
        interval=0,
    )

    runtime.running = True

    runtime.continuous_runner = (
        MagicMock()
    )

    runtime.stop()

    assert runtime.running is False

    runtime.continuous_runner.stop.assert_called_once()


# =========================================================
# Test E
# Runner Exception Still Resets Runtime State
# =========================================================

def test_runtime_runner_exception_resets_state():

    runtime = Runtime(
        interval=0,
    )

    runtime.health_monitor = (
        MagicMock()
    )

    runtime.health_monitor.is_healthy.return_value = (
        True
    )

    runtime.continuous_runner = (
        MagicMock()
    )

    runtime.continuous_runner.start.side_effect = (
        RuntimeError(
            "Simulated runner failure."
        )
    )

    try:

        runtime.start(
            cycles=1,
        )

    except RuntimeError:

        pass

    assert runtime.running is False