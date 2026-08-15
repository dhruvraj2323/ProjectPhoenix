"""
=================================================
Project Phoenix
Runtime Watchdog Integration Tests
M62.5 - Runtime Watchdog Integration
=================================================
"""

from unittest.mock import MagicMock

from config.configuration_readiness_models import (
    ConfigurationReadinessResult,
)

from deployment.runtime import Runtime

from deployment.runtime_operational_state import (
    RuntimeOperationalState,
)

from deployment.runtime_watchdog import (
    RuntimeWatchdog,
    WatchdogHealthState,
)

from deployment.trading_protection import (
    TradingProtection,
    TradingProtectionState,
)


def _ready_configuration():
    return ConfigurationReadinessResult(
        ready=True,
        environment_ready=True,
        mt5_ready=True,
        runtime_ready=True,
        secrets_safe=True,
    )


def _create_runtime():
    """
    Create Runtime with a mocked HealthMonitor and
    an integrated RuntimeWatchdog.

    The Runtime and RuntimeWatchdog intentionally
    share the exact same HealthMonitor instance.
    """

    protection = TradingProtection()

    runtime = Runtime(
        interval=0,
        configuration_readiness=(
            _ready_configuration()
        ),
        trading_protection=protection,
    )

    monitor = MagicMock()

    monitor.is_healthy.return_value = True

    runtime.health_monitor = monitor

    watchdog = RuntimeWatchdog(
        health_monitor=monitor,
    )

    runtime.watchdog = watchdog

    return (
        runtime,
        watchdog,
        monitor,
        protection,
    )


# =========================================================
# Test 1
# Runtime Has Watchdog
# =========================================================

def test_runtime_has_watchdog():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    assert runtime.watchdog is watchdog


# =========================================================
# Test 2
# Watchdog Uses Runtime Health Monitor
# =========================================================

def test_watchdog_uses_runtime_health_monitor():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    assert (
        watchdog.health_monitor
        is runtime.health_monitor
    )


# =========================================================
# Test 3
# Healthy Watchdog Check Does Not Degrade Runtime
# =========================================================

def test_healthy_watchdog_check_keeps_runtime_running():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    result = runtime.check_watchdog()

    assert (
        result
        == WatchdogHealthState.HEALTHY
    )

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )


# =========================================================
# Test 4
# Watchdog Detects Unhealthy Runtime
# =========================================================

def test_watchdog_detects_unhealthy_runtime():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    monitor.is_healthy.return_value = False

    result = runtime.check_watchdog()

    assert (
        result
        == WatchdogHealthState.UNHEALTHY
    )

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.DEGRADED
    )


# =========================================================
# Test 5
# Unhealthy Watchdog Pauses Trading Protection
# =========================================================

def test_unhealthy_watchdog_pauses_trading_protection():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    monitor.is_healthy.return_value = False

    runtime.check_watchdog()

    assert (
        protection.state
        == TradingProtectionState.PAUSED
    )

    assert (
        protection.can_trade()
        is False
    )


# =========================================================
# Test 6
# Watchdog Recovery Restores Runtime
# =========================================================

def test_watchdog_recovery_restores_runtime():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    monitor.is_healthy.return_value = False

    runtime.check_watchdog()

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.DEGRADED
    )

    monitor.is_healthy.return_value = True

    runtime.check_watchdog()

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )


# =========================================================
# Test 7
# Watchdog Recovery Activates Trading Protection
# =========================================================

def test_watchdog_recovery_activates_trading_protection():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    monitor.is_healthy.return_value = False

    runtime.check_watchdog()

    assert (
        protection.state
        == TradingProtectionState.PAUSED
    )

    monitor.is_healthy.return_value = True

    runtime.check_watchdog()

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )

    assert (
        protection.can_trade()
        is True
    )


# =========================================================
# Test 8
# Repeated Unhealthy Does Not Reapply Transition
# =========================================================

def test_repeated_unhealthy_does_not_reapply_transition():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    monitor.is_healthy.return_value = False

    runtime.check_watchdog()

    update_mock = MagicMock(
        wraps=protection.update,
    )

    protection.update = update_mock

    runtime.check_watchdog()

    update_mock.assert_not_called()


# =========================================================
# Test 9
# Repeated Healthy Does Not Reapply Recovery
# =========================================================

def test_repeated_healthy_does_not_reapply_recovery():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    monitor.is_healthy.return_value = False

    runtime.check_watchdog()

    monitor.is_healthy.return_value = True

    runtime.check_watchdog()

    update_mock = MagicMock(
        wraps=protection.update,
    )

    protection.update = update_mock

    runtime.check_watchdog()

    update_mock.assert_not_called()


# =========================================================
# Test 10
# Watchdog Does Not Start Runtime
# =========================================================

def test_watchdog_does_not_start_runtime():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    monitor.is_healthy.return_value = False

    result = runtime.check_watchdog()

    assert (
        result
        == WatchdogHealthState.UNHEALTHY
    )

    assert (
        runtime.running
        is False
    )


# =========================================================
# Test 11
# Watchdog Does Not Stop Runtime
# =========================================================

def test_watchdog_does_not_stop_runtime():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    monitor.is_healthy.return_value = False

    runtime.check_watchdog()

    assert (
        runtime.running
        is True
    )


# =========================================================
# Test 12
# Watchdog Does Not Directly Control Protection
# =========================================================

def test_watchdog_does_not_directly_control_protection():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    monitor.is_healthy.return_value = False

    watchdog.check()

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )


# =========================================================
# Test 13
# Runtime Processes Watchdog Transition
# =========================================================

def test_runtime_processes_watchdog_transition():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    monitor.is_healthy.return_value = False

    runtime.check_watchdog()

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.DEGRADED
    )

    assert (
        protection.state
        == TradingProtectionState.PAUSED
    )


# =========================================================
# Test 14
# Runtime Clears Processed Watchdog Transition
# =========================================================

def test_runtime_clears_processed_watchdog_transition():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    monitor.is_healthy.return_value = False

    runtime.check_watchdog()

    assert (
        watchdog.has_transitioned()
        is False
    )


# =========================================================
# Test 15
# Runtime Clears Processed Recovery Transition
# =========================================================

def test_runtime_clears_processed_recovery_transition():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    monitor.is_healthy.return_value = False

    runtime.check_watchdog()

    monitor.is_healthy.return_value = True

    runtime.check_watchdog()

    assert (
        watchdog.has_transitioned()
        is False
    )


# =========================================================
# Test 16
# Watchdog Check Returns Current Health State
# =========================================================

def test_check_watchdog_returns_current_health_state():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    monitor.is_healthy.return_value = False

    result = runtime.check_watchdog()

    assert (
        result
        == WatchdogHealthState.UNHEALTHY
    )

    monitor.is_healthy.return_value = True

    result = runtime.check_watchdog()

    assert (
        result
        == WatchdogHealthState.HEALTHY
    )


# =========================================================
# Test 17
# Stopped Runtime Does Not Enter Degraded State
# =========================================================

def test_stopped_runtime_does_not_enter_degraded_state():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    monitor.is_healthy.return_value = False

    runtime.check_watchdog()

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.STOPPED
    )

    assert (
        runtime.running
        is False
    )


# =========================================================
# Test 18
# Failed Runtime Does Not Recover Through Watchdog
# =========================================================

def test_failed_runtime_does_not_recover_through_watchdog():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    runtime._operational_status = (
        type(runtime._operational_status)(
            state=(
                RuntimeOperationalState.FAILED
            ),
            reason=(
                "Runtime execution failed."
            ),
        )
    )

    runtime.running = False

    monitor.is_healthy.return_value = True

    result = runtime.check_watchdog()

    assert (
        result
        == WatchdogHealthState.HEALTHY
    )

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.FAILED
    )


# =========================================================
# Test 19
# Full Watchdog Degradation → Recovery Cycle
# =========================================================

def test_full_watchdog_degradation_recovery_cycle():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )

    monitor.is_healthy.return_value = False

    runtime.check_watchdog()

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.DEGRADED
    )

    assert (
        protection.state
        == TradingProtectionState.PAUSED
    )

    monitor.is_healthy.return_value = True

    runtime.check_watchdog()

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )


# =========================================================
# Test 20
# Watchdog Integration Preserves Runtime Lifecycle
# =========================================================

def test_watchdog_integration_preserves_runtime_lifecycle():

    runtime, watchdog, monitor, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    monitor.is_healthy.return_value = False

    runtime.check_watchdog()

    assert (
        runtime.running
        is True
    )

    monitor.is_healthy.return_value = True

    runtime.check_watchdog()

    assert (
        runtime.running
        is True
    )

    runtime.stop()

    assert (
        runtime.running
        is False
    )

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.STOPPED
    )