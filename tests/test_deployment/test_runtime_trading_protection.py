"""
=================================================
Project Phoenix
Runtime Trading Protection Tests
M62.4.5 - TradingProtection Integration
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

    protection = TradingProtection()

    runtime = Runtime(
        interval=0,
        configuration_readiness=(
            _ready_configuration()
        ),
        trading_protection=protection,
    )

    runtime.health_monitor = MagicMock()

    runtime.health_monitor.is_healthy.return_value = (
        True
    )

    runtime.continuous_runner = MagicMock()

    return runtime, protection


# =========================================================
# Test A
# Unhealthy Runtime Pauses Trading
# =========================================================

def test_unhealthy_runtime_pauses_trading():

    runtime, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    result = runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    assert result is True

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.DEGRADED
    )

    assert (
        protection.state
        == TradingProtectionState.PAUSED
    )

    assert (
        protection.can_trade()
        is False
    )

    assert (
        protection.is_paused()
        is True
    )


# =========================================================
# Test B
# Healthy Recovery Activates Trading
# =========================================================

def test_healthy_recovery_activates_trading():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    assert (
        protection.state
        == TradingProtectionState.PAUSED
    )

    result = runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    assert result is True

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )

    assert (
        protection.can_trade()
        is True
    )

    assert (
        protection.is_paused()
        is False
    )


# =========================================================
# Test C
# Full Degradation → Recovery Protection Cycle
# =========================================================

def test_full_degradation_recovery_protection_cycle():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.DEGRADED
    )

    assert (
        protection.state
        == TradingProtectionState.PAUSED
    )

    assert (
        protection.can_trade()
        is False
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )

    assert (
        protection.can_trade()
        is True
    )


# =========================================================
# Test D
# Repeated Unhealthy Keeps Protection Paused
# =========================================================

def test_repeated_unhealthy_keeps_protection_paused():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    first_transition = (
        protection.last_transition
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    assert (
        protection.state
        == TradingProtectionState.PAUSED
    )

    assert (
        protection.can_trade()
        is False
    )

    assert (
        protection.last_transition
        is first_transition
    )


# =========================================================
# Test E
# Repeated Healthy Keeps Protection Active
# =========================================================

def test_repeated_healthy_keeps_protection_active():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    first_transition = (
        protection.last_transition
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )

    assert (
        protection.can_trade()
        is True
    )

    assert (
        protection.last_transition
        is first_transition
    )


# =========================================================
# Test F
# Stopped Runtime Does Not Modify Protection
# =========================================================

def test_stopped_runtime_does_not_modify_protection():

    runtime, protection = (
        _create_runtime()
    )

    initial_state = (
        protection.state
    )

    result = runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    assert result is False

    assert (
        protection.state
        == initial_state
    )


# =========================================================
# Test G
# Failed Runtime Does Not Modify Protection
# =========================================================

def test_failed_runtime_does_not_modify_protection():

    runtime, protection = (
        _create_runtime()
    )

    runtime._operational_status = (
        __import__(
            "deployment.runtime_operational_state",
            fromlist=[
                "RuntimeOperationalStatus"
            ],
        ).RuntimeOperationalStatus(
            state=(
                RuntimeOperationalState.FAILED
            ),
            reason=(
                "Runtime execution failed."
            ),
        )
    )

    result = runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    assert result is False

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )


# =========================================================
# Test H
# Recovery From Stopped Runtime Does Not Activate
# =========================================================

def test_recovery_from_stopped_runtime_does_not_activate():

    runtime, protection = (
        _create_runtime()
    )

    result = runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    assert result is False

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )


# =========================================================
# Test I
# Runtime Does Not Directly Execute Trades
# =========================================================

def test_runtime_does_not_directly_execute_trades():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    assert not hasattr(
        runtime,
        "execute_trade",
    )

    assert not hasattr(
        runtime,
        "place_order",
    )


# =========================================================
# Test J
# Runtime Does Not Automatically Stop On Degradation
# =========================================================

def test_runtime_does_not_stop_on_degradation():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.continuous_runner.stop.reset_mock()

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    assert (
        runtime.running
        is True
    )

    runtime.continuous_runner.stop.assert_not_called()


# =========================================================
# Test K
# Runtime Does Not Restart On Recovery
# =========================================================

def test_runtime_does_not_restart_on_recovery():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    runtime.continuous_runner.start.reset_mock()

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    assert (
        runtime.running
        is True
    )

    runtime.continuous_runner.start.assert_not_called()


# =========================================================
# Test L
# Protection Is The Trading Permission Boundary
# =========================================================

def test_protection_is_trading_permission_boundary():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.DEGRADED
    )

    assert (
        protection.can_trade()
        is False
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        protection.can_trade()
        is True
    )


# =========================================================
# Test M
# Protection Transition Is Controlled By Protection
# =========================================================

def test_protection_transition_is_controlled_by_protection():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    protection.update = MagicMock(
        wraps=protection.update,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    protection.update.assert_called_once_with(
        WatchdogHealthState.UNHEALTHY,
    )


# =========================================================
# Test N
# Recovery Calls Protection With Healthy State
# =========================================================

def test_recovery_calls_protection_with_healthy_state():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    protection.update = MagicMock(
        wraps=protection.update,
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    protection.update.assert_called_once_with(
        WatchdogHealthState.HEALTHY,
    )


# =========================================================
# Test O
# Degradation Keeps Runtime Lifecycle Independent
# =========================================================

def test_degradation_keeps_runtime_lifecycle_independent():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    assert (
        runtime.running
        is True
    )

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.DEGRADED
    )

    assert (
        protection.state
        == TradingProtectionState.PAUSED
    )


# =========================================================
# Test P
# Recovery Keeps Runtime Lifecycle Independent
# =========================================================

def test_recovery_keeps_runtime_lifecycle_independent():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    assert (
        runtime.running
        is True
    )

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )


# =========================================================
# Test Q
# Protection State Is Observable After Degradation
# =========================================================

def test_protection_state_is_observable_after_degradation():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    assert (
        protection.state
        == TradingProtectionState.PAUSED
    )

    assert (
        protection.is_paused()
        is True
    )


# =========================================================
# Test R
# Protection State Is Observable After Recovery
# =========================================================

def test_protection_state_is_observable_after_recovery():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )

    assert (
        protection.is_paused()
        is False
    )


# =========================================================
# Test S
# Explicit Runtime Stop Remains Lifecycle Operation
# =========================================================

def test_explicit_runtime_stop_remains_lifecycle_operation():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
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


# =========================================================
# Test T
# Full Runtime + Protection Lifecycle
# =========================================================

def test_full_runtime_and_protection_lifecycle():

    runtime, protection = (
        _create_runtime()
    )

    # Startup
    assert runtime.start(
        cycles=1,
    ) is True

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )

    # Degradation
    assert runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    ) is True

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.DEGRADED
    )

    assert (
        protection.state
        == TradingProtectionState.PAUSED
    )

    assert (
        protection.can_trade()
        is False
    )

    # Recovery
    assert runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    ) is True

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )

    assert (
        protection.can_trade()
        is True
    )

    # Explicit shutdown
    runtime.stop()

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.STOPPED
    )

    assert (
        runtime.running
        is False
    )