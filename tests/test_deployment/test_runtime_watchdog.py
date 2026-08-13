"""
=================================================
Project Phoenix
Runtime Health Watchdog Tests
M61.8.1 - Runtime Health Watchdog Foundation
=================================================
"""

from unittest.mock import MagicMock

from deployment.runtime_watchdog import (
    HealthTransition,
    RuntimeWatchdog,
    WatchdogHealthState,
)


# =========================================================
# Test A
# Default State
# =========================================================

def test_runtime_watchdog_default_state():

    monitor = MagicMock()

    monitor.is_healthy.return_value = True

    watchdog = RuntimeWatchdog(
        health_monitor=monitor,
    )

    assert (
        watchdog.state
        == WatchdogHealthState.HEALTHY
    )

    assert (
        watchdog.last_transition
        is None
    )


# =========================================================
# Test B
# Healthy Check
# =========================================================

def test_runtime_watchdog_healthy_check():

    monitor = MagicMock()

    monitor.is_healthy.return_value = True

    watchdog = RuntimeWatchdog(
        health_monitor=monitor,
    )

    result = watchdog.check()

    assert (
        result
        == WatchdogHealthState.HEALTHY
    )

    assert (
        watchdog.has_transitioned()
        is False
    )

    assert (
        watchdog.has_recovered()
        is False
    )

    monitor.is_healthy.assert_called_once()


# =========================================================
# Test C
# Healthy → Unhealthy
# =========================================================

def test_runtime_watchdog_detects_unhealthy_transition():

    monitor = MagicMock()

    monitor.is_healthy.return_value = False

    watchdog = RuntimeWatchdog(
        health_monitor=monitor,
    )

    result = watchdog.check()

    assert (
        result
        == WatchdogHealthState.UNHEALTHY
    )

    assert (
        watchdog.state
        == WatchdogHealthState.UNHEALTHY
    )

    assert (
        watchdog.has_transitioned()
        is True
    )

    assert (
        watchdog.last_transition
        == HealthTransition(
            previous_state=(
                WatchdogHealthState.HEALTHY
            ),
            current_state=(
                WatchdogHealthState.UNHEALTHY
            ),
        )
    )

    assert (
        watchdog.has_recovered()
        is False
    )


# =========================================================
# Test D
# Unhealthy → Healthy Recovery
# =========================================================

def test_runtime_watchdog_detects_recovery():

    monitor = MagicMock()

    monitor.is_healthy.side_effect = [
        False,
        True,
    ]

    watchdog = RuntimeWatchdog(
        health_monitor=monitor,
    )

    first = watchdog.check()

    assert (
        first
        == WatchdogHealthState.UNHEALTHY
    )

    assert (
        watchdog.has_transitioned()
        is True
    )

    watchdog.clear_transition()

    assert (
        watchdog.has_transitioned()
        is False
    )

    second = watchdog.check()

    assert (
        second
        == WatchdogHealthState.HEALTHY
    )

    assert (
        watchdog.has_transitioned()
        is True
    )

    assert (
        watchdog.has_recovered()
        is True
    )

    assert (
        watchdog.last_transition
        == HealthTransition(
            previous_state=(
                WatchdogHealthState.UNHEALTHY
            ),
            current_state=(
                WatchdogHealthState.HEALTHY
            ),
        )
    )


# =========================================================
# Test E
# Repeated Unhealthy State Is Not a Transition
# =========================================================

def test_runtime_watchdog_repeated_unhealthy_is_not_new_transition():

    monitor = MagicMock()

    monitor.is_healthy.return_value = False

    watchdog = RuntimeWatchdog(
        health_monitor=monitor,
    )

    first = watchdog.check()

    assert (
        first
        == WatchdogHealthState.UNHEALTHY
    )

    first_transition = (
        watchdog.last_transition
    )

    second = watchdog.check()

    assert (
        second
        == WatchdogHealthState.UNHEALTHY
    )

    assert (
        watchdog.last_transition
        is first_transition
    )

    assert (
        watchdog.has_recovered()
        is False
    )

    assert (
        monitor.is_healthy.call_count
        == 2
    )


# =========================================================
# Test F
# Current State Reads HealthMonitor
# =========================================================

def test_runtime_watchdog_current_state():

    monitor = MagicMock()

    monitor.is_healthy.return_value = True

    watchdog = RuntimeWatchdog(
        health_monitor=monitor,
    )

    assert (
        watchdog.current_state()
        == WatchdogHealthState.HEALTHY
    )

    monitor.is_healthy.return_value = False

    assert (
        watchdog.current_state()
        == WatchdogHealthState.UNHEALTHY
    )


# =========================================================
# Test G
# Clear Transition Does Not Change State
# =========================================================

def test_runtime_watchdog_clear_transition():

    monitor = MagicMock()

    monitor.is_healthy.return_value = False

    watchdog = RuntimeWatchdog(
        health_monitor=monitor,
    )

    watchdog.check()

    assert (
        watchdog.state
        == WatchdogHealthState.UNHEALTHY
    )

    assert (
        watchdog.last_transition
        is not None
    )

    watchdog.clear_transition()

    assert (
        watchdog.last_transition
        is None
    )

    assert (
        watchdog.state
        == WatchdogHealthState.UNHEALTHY
    )