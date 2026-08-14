"""
=================================================
Project Phoenix
Runtime Degradation Tests
M62.4.3 - Runtime → DEGRADED Integration
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

from deployment.runtime_status import (
    RuntimeStatus,
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
# Running Runtime Can Become Degraded
# =========================================================

def test_running_runtime_can_become_degraded():

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

    status = runtime.status_snapshot()

    assert (
        status.operational_state
        == RuntimeOperationalState.DEGRADED
    )

    assert (
        status.runtime_running
        is True
    )


# =========================================================
# Test B
# Degraded Runtime Remains Running
# =========================================================

def test_degraded_runtime_remains_running():

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

    status = runtime.status_snapshot()

    assert (
        status.runtime_running
        is True
    )


# =========================================================
# Test C
# Degradation Does Not Stop Runner
# =========================================================

def test_degradation_does_not_stop_runner():

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

    runtime.continuous_runner.stop.assert_not_called()


# =========================================================
# Test D
# Degradation Does Not Restart Runner
# =========================================================

def test_degradation_does_not_restart_runner():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.continuous_runner.start.reset_mock()

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    runtime.continuous_runner.start.assert_not_called()


# =========================================================
# Test E
# Degradation Pauses Trading Protection
# =========================================================

def test_degradation_pauses_trading_protection():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    protection.update(
        WatchdogHealthState.UNHEALTHY,
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
        protection.is_paused()
        is True
    )


# =========================================================
# Test F
# Degradation Policy Is Reflected In Runtime State
# =========================================================

def test_degradation_policy_is_reflected_in_runtime_state():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    operational = (
        runtime.operational_state()
    )

    assert (
        operational.state
        == RuntimeOperationalState.DEGRADED
    )

    assert (
        "degraded"
        in operational.reason.lower()
    )


# =========================================================
# Test G
# Degraded Status Is Structured
# =========================================================

def test_degraded_status_is_structured():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    status = runtime.status_snapshot()

    assert isinstance(
        status,
        RuntimeStatus,
    )

    assert (
        status.operational_state
        == RuntimeOperationalState.DEGRADED
    )


# =========================================================
# Test H
# Degraded Status Does Not Grant Trading Permission
# =========================================================

def test_degraded_status_does_not_expose_trading_permission():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    status = runtime.status_snapshot()

    assert (
        status.operational_state
        == RuntimeOperationalState.DEGRADED
    )

    assert not hasattr(
        status,
        "can_trade",
    )

    assert not hasattr(
        status,
        "live_approved",
    )

    assert not hasattr(
        status,
        "trading_permission",
    )


# =========================================================
# Test I
# Degraded Status Does Not Expose Secrets
# =========================================================

def test_degraded_status_does_not_expose_secrets():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    status = runtime.status_snapshot()

    assert not hasattr(
        status,
        "password",
    )

    assert not hasattr(
        status,
        "bot_token",
    )

    assert not hasattr(
        status,
        "api_key",
    )


# =========================================================
# Test J
# Healthy State Does Not Degrade Runtime
# =========================================================

def test_healthy_state_keeps_runtime_running():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    result = runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    assert result is True

    status = runtime.status_snapshot()

    assert (
        status.operational_state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        status.runtime_running
        is True
    )


# =========================================================
# Test K
# Healthy State Keeps Trading Active
# =========================================================

def test_healthy_state_keeps_trading_active():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    protection.update(
        WatchdogHealthState.HEALTHY,
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


# =========================================================
# Test L
# Stopped Runtime Does Not Become Degraded
# =========================================================

def test_stopped_runtime_does_not_become_degraded():

    runtime, protection = (
        _create_runtime()
    )

    result = runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    assert result is False

    status = runtime.status_snapshot()

    assert (
        status.operational_state
        == RuntimeOperationalState.STOPPED
    )

    assert (
        status.runtime_running
        is False
    )


# =========================================================
# Test M
# Failed Runtime Does Not Become Degraded
# =========================================================

def test_failed_runtime_does_not_become_degraded():

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

    status = runtime.status_snapshot()

    assert (
        status.operational_state
        == RuntimeOperationalState.FAILED
    )


# =========================================================
# Test N
# Degradation Does Not Change Running Flag
# =========================================================

def test_degradation_does_not_change_running_flag():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    assert runtime.running is True

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    assert runtime.running is True


# =========================================================
# Test O
# Repeated Degradation Is Stable
# =========================================================

def test_repeated_degradation_is_stable():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    first = runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    first_status = (
        runtime.status_snapshot()
    )

    second = runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    second_status = (
        runtime.status_snapshot()
    )

    assert first is True
    assert second is True

    assert (
        first_status.operational_state
        == RuntimeOperationalState.DEGRADED
    )

    assert (
        second_status.operational_state
        == RuntimeOperationalState.DEGRADED
    )

    assert (
        runtime.running
        is True
    )


# =========================================================
# Test P
# Degradation Reason Is Observable
# =========================================================

def test_degradation_reason_is_observable():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    status = runtime.status_snapshot()

    assert (
        "health"
        in status.reason.lower()
    )

    assert (
        "degraded"
        in status.reason.lower()
    )


# =========================================================
# Test Q
# Degradation Does Not Automatically Stop Runtime
# =========================================================

def test_degradation_does_not_automatically_stop_runtime():

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


# =========================================================
# Test R
# Explicit Stop Still Works After Degradation
# =========================================================

def test_explicit_stop_still_works_after_degradation():

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

    status = runtime.status_snapshot()

    assert (
        status.operational_state
        == RuntimeOperationalState.STOPPED
    )

    assert (
        status.runtime_running
        is False
    )

    assert (
        runtime.running
        is False
    )


# =========================================================
# Test S
# Degradation Does Not Expose Runtime Credentials
# =========================================================

def test_degradation_does_not_expose_runtime_credentials():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    status = runtime.status_snapshot()

    assert not hasattr(
        status,
        "mt5_password",
    )

    assert not hasattr(
        status,
        "telegram_bot_token",
    )


# =========================================================
# Test T
# Runtime Remains Lifecycle Owner
# =========================================================

def test_runtime_remains_lifecycle_owner():

    runtime, protection = (
        _create_runtime()
    )

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    assert runtime.running is True

    runtime.stop()

    assert runtime.running is False

    status = runtime.status_snapshot()

    assert (
        status.operational_state
        == RuntimeOperationalState.STOPPED
    )