"""
=================================================
Project Phoenix
Runtime Recovery Tests
M62.4.4 - Recovery → RUNNING Integration
=================================================
"""

from unittest.mock import MagicMock

from config.configuration_readiness_models import (
    ConfigurationReadinessResult,
)

from deployment.runtime import Runtime

from deployment.runtime_operational_state import (
    RuntimeOperationalState,
    RuntimeOperationalStatus,
)

from deployment.runtime_status import (
    RuntimeStatus,
)

from deployment.runtime_watchdog import (
    WatchdogHealthState,
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

    runtime = Runtime(
        interval=0,
        configuration_readiness=(
            _ready_configuration()
        ),
    )

    runtime.health_monitor = MagicMock()

    runtime.health_monitor.is_healthy.return_value = (
        True
    )

    runtime.continuous_runner = MagicMock()

    return runtime


# =========================================================
# Test A
# Running → Degraded → Running
# =========================================================

def test_running_degraded_running_recovery_cycle():

    runtime = _create_runtime()

    assert runtime.start(
        cycles=1,
    ) is True

    degraded = runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    assert degraded is True

    degraded_status = (
        runtime.status_snapshot()
    )

    assert (
        degraded_status.operational_state
        == RuntimeOperationalState.DEGRADED
    )

    recovered = runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    assert recovered is True

    recovered_status = (
        runtime.status_snapshot()
    )

    assert (
        recovered_status.operational_state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        recovered_status.runtime_running
        is True
    )


# =========================================================
# Test B
# Recovery Does Not Start Runner Again
# =========================================================

def test_recovery_does_not_restart_runner():

    runtime = _create_runtime()

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    runtime.continuous_runner.start.reset_mock()

    result = runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    assert result is True

    runtime.continuous_runner.start.assert_not_called()


# =========================================================
# Test C
# Recovery Does Not Stop Runner
# =========================================================

def test_recovery_does_not_stop_runner():

    runtime = _create_runtime()

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    runtime.continuous_runner.stop.reset_mock()

    result = runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    assert result is True

    runtime.continuous_runner.stop.assert_not_called()


# =========================================================
# Test D
# Recovery Preserves Running Flag
# =========================================================

def test_recovery_preserves_running_flag():

    runtime = _create_runtime()

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    assert runtime.running is True

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    assert runtime.running is True


# =========================================================
# Test E
# Recovery Produces Running Operational State
# =========================================================

def test_recovery_produces_running_operational_state():

    runtime = _create_runtime()

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    operational = (
        runtime.operational_state()
    )

    assert (
        operational.state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        "recovered"
        in operational.reason.lower()
    )


# =========================================================
# Test F
# Recovery Produces Structured RuntimeStatus
# =========================================================

def test_recovery_produces_structured_status():

    runtime = _create_runtime()

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    status = runtime.status_snapshot()

    assert isinstance(
        status,
        RuntimeStatus,
    )

    assert (
        status.operational_state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        status.runtime_running
        is True
    )


# =========================================================
# Test G
# Stopped Runtime Cannot Recover Into Running
# =========================================================

def test_stopped_runtime_cannot_recover_into_running():

    runtime = _create_runtime()

    result = runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
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
# Test H
# Failed Runtime Cannot Recover Into Running
# =========================================================

def test_failed_runtime_cannot_recover_into_running():

    runtime = _create_runtime()

    runtime._operational_status = (
        RuntimeOperationalStatus(
            state=(
                RuntimeOperationalState.FAILED
            ),
            reason=(
                "Runtime execution failed."
            ),
        )
    )

    result = runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    assert result is False

    status = runtime.status_snapshot()

    assert (
        status.operational_state
        == RuntimeOperationalState.FAILED
    )

    assert (
        status.runtime_running
        is False
    )


# =========================================================
# Test I
# Starting Runtime Cannot Recover Into Running
# =========================================================

def test_starting_runtime_cannot_recover_into_running():

    runtime = _create_runtime()

    runtime._operational_status = (
        RuntimeOperationalStatus(
            state=(
                RuntimeOperationalState.STARTING
            ),
            reason=(
                "Runtime startup initiated."
            ),
        )
    )

    runtime.running = True

    result = runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    assert result is False

    status = runtime.status_snapshot()

    assert (
        status.operational_state
        == RuntimeOperationalState.STARTING
    )


# =========================================================
# Test J
# Ready Runtime Cannot Be Recovered
# =========================================================

def test_ready_runtime_cannot_be_recovered():

    runtime = _create_runtime()

    runtime._operational_status = (
        RuntimeOperationalStatus(
            state=(
                RuntimeOperationalState.READY
            ),
            reason=(
                "Runtime configuration and "
                "deployment health are ready."
            ),
        )
    )

    runtime.running = True

    result = runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    assert result is False

    status = runtime.status_snapshot()

    assert (
        status.operational_state
        == RuntimeOperationalState.READY
    )


# =========================================================
# Test K
# Recovery From Degraded Is Idempotent
# =========================================================

def test_recovery_from_degraded_is_idempotent():

    runtime = _create_runtime()

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    first = runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    first_status = (
        runtime.status_snapshot()
    )

    second = runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    second_status = (
        runtime.status_snapshot()
    )

    assert first is True

    assert second is True

    assert (
        first_status.operational_state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        second_status.operational_state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        runtime.running
        is True
    )


# =========================================================
# Test L
# Recovery Does Not Change Configuration Readiness
# =========================================================

def test_recovery_does_not_change_configuration_readiness():

    runtime = _create_runtime()

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    status = runtime.status_snapshot()

    assert (
        status.configuration_ready
        is True
    )


# =========================================================
# Test M
# Recovery Does Not Expose Trading Permission
# =========================================================

def test_recovery_status_does_not_expose_trading_permission():

    runtime = _create_runtime()

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    status = runtime.status_snapshot()

    assert not hasattr(
        status,
        "can_trade",
    )

    assert not hasattr(
        status,
        "live_approved",
    )


# =========================================================
# Test N
# Recovery Does Not Expose Secrets
# =========================================================

def test_recovery_status_does_not_expose_secrets():

    runtime = _create_runtime()

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
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
# Test O
# Explicit Stop After Recovery Still Works
# =========================================================

def test_explicit_stop_after_recovery_still_works():

    runtime = _create_runtime()

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
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
# Test P
# Recovery Reason Is Observable
# =========================================================

def test_recovery_reason_is_observable():

    runtime = _create_runtime()

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    status = runtime.status_snapshot()

    assert (
        "recovered"
        in status.reason.lower()
    )

    assert (
        "operational"
        in status.reason.lower()
    )


# =========================================================
# Test Q
# Recovery Does Not Automatically Execute Trades
# =========================================================

def test_recovery_does_not_execute_trades():

    runtime = _create_runtime()

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
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
# Test R
# Recovery Keeps Runtime Lifecycle Ownership
# =========================================================

def test_recovery_keeps_runtime_lifecycle_ownership():

    runtime = _create_runtime()

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

    runtime.stop()

    assert (
        runtime.running
        is False
    )


# =========================================================
# Test S
# Recovery From Degraded Does Not Invoke Runner
# =========================================================

def test_recovery_from_degraded_does_not_invoke_runner():

    runtime = _create_runtime()

    runtime.start(
        cycles=1,
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    )

    runtime.continuous_runner.start.reset_mock()
    runtime.continuous_runner.stop.reset_mock()

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    )

    runtime.continuous_runner.start.assert_not_called()
    runtime.continuous_runner.stop.assert_not_called()


# =========================================================
# Test T
# Recovery Completes Full State Transition
# =========================================================

def test_recovery_completes_full_state_transition():

    runtime = _create_runtime()

    assert runtime.start(
        cycles=1,
    ) is True

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )

    assert runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY,
    ) is True

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.DEGRADED
    )

    assert runtime.apply_health_state(
        WatchdogHealthState.HEALTHY,
    ) is True

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )

    assert runtime.running is True