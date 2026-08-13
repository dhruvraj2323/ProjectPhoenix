"""
=================================================
Project Phoenix
Runtime Manager Tests
M61.6.3 - Runtime Readiness Integration
=================================================
"""

from unittest.mock import MagicMock

from deployment.runtime_manager import (
    RuntimeManager,
)


# =========================================================
# Test A
# Runtime Manager Starts Healthy Runtime
# =========================================================

def test_runtime_manager_start():

    runtime = MagicMock()

    runtime.start.return_value = True

    runtime.running = False

    manager = RuntimeManager(
        runtime=runtime,
    )

    result = manager.start(
        cycles=1,
    )

    assert result is True

    runtime.start.assert_called_once_with(
        cycles=1,
    )

    assert manager.running is False


# =========================================================
# Test B
# Readiness Failure Blocks Manager
# =========================================================

def test_runtime_manager_start_blocked():

    runtime = MagicMock()

    runtime.start.return_value = False

    runtime.running = False

    manager = RuntimeManager(
        runtime=runtime,
    )

    result = manager.start(
        cycles=1,
    )

    assert result is False

    runtime.start.assert_called_once_with(
        cycles=1,
    )

    assert manager.running is False


# =========================================================
# Test C
# Runtime Running State Is Reflected
# =========================================================

def test_runtime_manager_running_state():

    runtime = MagicMock()

    runtime.start.return_value = True

    runtime.running = True

    manager = RuntimeManager(
        runtime=runtime,
    )

    result = manager.start(
        cycles=1,
    )

    assert result is True

    assert manager.running is True

    assert manager.status() is True


# =========================================================
# Test D
# Stop
# =========================================================

def test_runtime_manager_stop():

    runtime = MagicMock()

    runtime.running = True

    manager = RuntimeManager(
        runtime=runtime,
    )

    result = manager.stop()

    assert result is True

    runtime.stop.assert_called_once()

    assert manager.running is True


# =========================================================
# Test E
# Restart
# =========================================================

def test_runtime_manager_restart():

    runtime = MagicMock()

    runtime.start.return_value = True

    runtime.running = False

    manager = RuntimeManager(
        runtime=runtime,
    )

    result = manager.restart(
        cycles=1,
    )

    assert result is True

    runtime.stop.assert_called_once()

    runtime.start.assert_called_once_with(
        cycles=1,
    )