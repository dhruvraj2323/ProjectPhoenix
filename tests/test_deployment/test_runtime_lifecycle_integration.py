"""
=================================================
Project Phoenix
Runtime Lifecycle Integration Tests
M62.7.1 - Runtime Lifecycle / Runtime Integration
=================================================
"""

from unittest.mock import MagicMock

import pytest

from config.configuration_readiness_models import (
    ConfigurationReadinessResult,
)

from deployment.runtime import (
    Runtime,
)

from deployment.runtime_lifecycle import (
    RuntimeLifecycle,
)

from deployment.runtime_operational_state import (
    RuntimeOperationalState,
)

from deployment.runtime_watchdog import (
    WatchdogHealthState,
)


# =================================================
# Helpers
# =================================================


def _ready_configuration():

    return ConfigurationReadinessResult(
        ready=True,
        environment_ready=True,
        mt5_ready=True,
        runtime_ready=True,
        secrets_safe=True,
        errors=[],
        warnings=[],
    )


def _create_runtime():

    protection = MagicMock()

    runtime = Runtime(
        interval=0,
        configuration_readiness=(
            _ready_configuration()
        ),
        trading_protection=protection,
        alert_dispatcher=MagicMock(),
    )

    # Prevent the integration tests from executing
    # the real ContinuousRunner.

    runtime.continuous_runner.start = (
        MagicMock()
    )

    runtime.continuous_runner.stop = (
        MagicMock()
    )

    return runtime


def _start_runtime():

    runtime = _create_runtime()

    result = runtime.start(
        cycles=1,
    )

    assert result is True

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )

    assert runtime.running is True

    return runtime


# =================================================
# Lifecycle Contract Ownership
# =================================================


def test_runtime_exposes_authoritative_lifecycle():

    runtime = _create_runtime()

    assert hasattr(
        runtime,
        "lifecycle",
    )

    assert isinstance(
        runtime.lifecycle,
        RuntimeLifecycle,
    )


def test_runtime_lifecycle_is_stable_for_runtime_session():

    runtime = _create_runtime()

    lifecycle = runtime.lifecycle

    assert (
        runtime.lifecycle
        is lifecycle
    )

    assert (
        runtime.lifecycle
        is lifecycle
    )


def test_runtime_operational_state_uses_frozen_state_enum():

    runtime = _create_runtime()

    status = runtime.operational_state()

    assert isinstance(
        status.state,
        RuntimeOperationalState,
    )


# =================================================
# Initial State
# =================================================


def test_runtime_initial_state_is_stopped():

    runtime = _create_runtime()

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.STOPPED
    )

    assert runtime.running is False


def test_runtime_initial_lifecycle_contract_marks_stopped_terminal():

    runtime = _create_runtime()

    assert runtime.lifecycle.is_terminal(
        RuntimeOperationalState.STOPPED
    )


def test_runtime_initial_lifecycle_contract_does_not_allow_restart():

    runtime = _create_runtime()

    assert not runtime.lifecycle.can_transition(
        RuntimeOperationalState.STOPPED,
        RuntimeOperationalState.STARTING,
    )


# =================================================
# Runtime Startup Lifecycle
# =================================================


def test_runtime_start_moves_runtime_to_running():

    runtime = _start_runtime()

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )


def test_runtime_start_marks_runtime_running():

    runtime = _start_runtime()

    assert runtime.running is True


def test_runtime_start_uses_valid_lifecycle_path():

    runtime = _start_runtime()

    assert (
        runtime.lifecycle.can_transition(
            RuntimeOperationalState.STARTING,
            RuntimeOperationalState.READY,
        )
        is True
    )

    assert (
        runtime.lifecycle.can_transition(
            RuntimeOperationalState.READY,
            RuntimeOperationalState.RUNNING,
        )
        is True
    )


def test_runtime_start_does_not_allow_direct_stopped_to_running():

    runtime = _create_runtime()

    assert not runtime.lifecycle.can_transition(
        RuntimeOperationalState.STOPPED,
        RuntimeOperationalState.RUNNING,
    )


# =================================================
# Configuration Failure
# =================================================


def test_configuration_failure_moves_runtime_to_failed():

    runtime = _create_runtime()

    runtime.configuration_readiness = (
        ConfigurationReadinessResult(
            ready=False,
            environment_ready=False,
            mt5_ready=True,
            runtime_ready=True,
            secrets_safe=True,
            errors=[
                "Configuration is not ready."
            ],
            warnings=[],
        )
    )

    result = runtime.start(
        cycles=1,
    )

    assert result is False

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.FAILED
    )

    assert runtime.running is False


def test_failed_start_is_terminal():

    runtime = _create_runtime()

    runtime.configuration_readiness = (
        ConfigurationReadinessResult(
            ready=False,
            environment_ready=False,
            mt5_ready=True,
            runtime_ready=True,
            secrets_safe=True,
            errors=[
                "Configuration is not ready."
            ],
            warnings=[],
        )
    )

    runtime.start(
        cycles=1,
    )

    assert runtime.lifecycle.is_terminal(
        RuntimeOperationalState.FAILED
    )


def test_failed_runtime_cannot_transition_to_running():

    runtime = _create_runtime()

    runtime.configuration_readiness = (
        ConfigurationReadinessResult(
            ready=False,
            environment_ready=False,
            mt5_ready=True,
            runtime_ready=True,
            secrets_safe=True,
            errors=[
                "Configuration is not ready."
            ],
            warnings=[],
        )
    )

    runtime.start(
        cycles=1,
    )

    assert not runtime.lifecycle.can_transition(
        RuntimeOperationalState.FAILED,
        RuntimeOperationalState.RUNNING,
    )


# =================================================
# Runtime Execution Failure
# =================================================


def test_runtime_execution_failure_moves_to_failed():

    runtime = _create_runtime()

    runtime.continuous_runner.start = (
        MagicMock(
            side_effect=RuntimeError(
                "Simulated runtime failure."
            )
        )
    )

    result = runtime.start(
        cycles=1,
    )

    assert result is False

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.FAILED
    )

    assert runtime.running is False


def test_runtime_execution_failure_is_terminal():

    runtime = _create_runtime()

    runtime.continuous_runner.start = (
        MagicMock(
            side_effect=RuntimeError(
                "Simulated runtime failure."
            )
        )
    )

    runtime.start(
        cycles=1,
    )

    assert runtime.lifecycle.is_terminal(
        RuntimeOperationalState.FAILED
    )


# =================================================
# Degradation
# =================================================


def test_running_runtime_can_enter_degraded_state():

    runtime = _start_runtime()

    result = runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY
    )

    assert result is True

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.DEGRADED
    )

    assert runtime.running is True


def test_degraded_state_is_valid_lifecycle_state():

    runtime = _create_runtime()

    assert runtime.lifecycle.can_transition(
        RuntimeOperationalState.RUNNING,
        RuntimeOperationalState.DEGRADED,
    )


def test_degraded_runtime_remains_operational():

    runtime = _start_runtime()

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY
    )

    assert runtime.lifecycle.is_operational(
        RuntimeOperationalState.DEGRADED
    )

    assert runtime.running is True


# =================================================
# Recovery
# =================================================


def test_degraded_runtime_can_recover():

    runtime = _start_runtime()

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY
    )

    result = runtime.apply_health_state(
        WatchdogHealthState.HEALTHY
    )

    assert result is True

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )

    assert runtime.running is True


def test_degraded_to_running_is_valid_lifecycle_transition():

    runtime = _create_runtime()

    assert runtime.lifecycle.can_transition(
        RuntimeOperationalState.DEGRADED,
        RuntimeOperationalState.RUNNING,
    )


# =================================================
# Shutdown Lifecycle
# =================================================


def test_running_runtime_can_stop():

    runtime = _start_runtime()

    runtime.stop()

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.STOPPED
    )

    assert runtime.running is False


def test_shutdown_uses_stopping_to_stopped_path():

    runtime = _create_runtime()

    assert runtime.lifecycle.can_transition(
        RuntimeOperationalState.RUNNING,
        RuntimeOperationalState.STOPPING,
    )

    assert runtime.lifecycle.can_transition(
        RuntimeOperationalState.STOPPING,
        RuntimeOperationalState.STOPPED,
    )


def test_stopped_runtime_is_terminal_after_shutdown():

    runtime = _start_runtime()

    runtime.stop()

    assert runtime.lifecycle.is_terminal(
        RuntimeOperationalState.STOPPED
    )


def test_duplicate_stop_does_not_create_new_lifecycle_state():

    runtime = _start_runtime()

    runtime.stop()

    first_state = (
        runtime.operational_state().state
    )

    runtime.stop()

    second_state = (
        runtime.operational_state().state
    )

    assert (
        first_state
        == RuntimeOperationalState.STOPPED
    )

    assert (
        second_state
        == RuntimeOperationalState.STOPPED
    )


# =================================================
# Terminal State Rules
# =================================================


def test_stopped_state_has_no_outgoing_transitions():

    runtime = _create_runtime()

    assert (
        runtime.lifecycle.allowed_transitions(
            RuntimeOperationalState.STOPPED
        )
        == frozenset()
    )


def test_failed_state_has_no_outgoing_transitions():

    runtime = _create_runtime()

    assert (
        runtime.lifecycle.allowed_transitions(
            RuntimeOperationalState.FAILED
        )
        == frozenset()
    )


def test_stopped_cannot_restart():

    runtime = _start_runtime()

    runtime.stop()

    assert not runtime.lifecycle.can_transition(
        RuntimeOperationalState.STOPPED,
        RuntimeOperationalState.STARTING,
    )


def test_stopped_cannot_jump_to_running():

    runtime = _start_runtime()

    runtime.stop()

    assert not runtime.lifecycle.can_transition(
        RuntimeOperationalState.STOPPED,
        RuntimeOperationalState.RUNNING,
    )


def test_failed_cannot_recover_to_running():

    runtime = _create_runtime()

    runtime.continuous_runner.start = (
        MagicMock(
            side_effect=RuntimeError(
                "Simulated runtime failure."
            )
        )
    )

    runtime.start(
        cycles=1,
    )

    assert not runtime.lifecycle.can_transition(
        RuntimeOperationalState.FAILED,
        RuntimeOperationalState.RUNNING,
    )


# =================================================
# Complete Normal Lifecycle
# =================================================


def test_complete_normal_runtime_lifecycle():

    runtime = _start_runtime()

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )

    runtime.stop()

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.STOPPED
    )


# =================================================
# Complete Degradation / Recovery Lifecycle
# =================================================


def test_complete_degradation_recovery_lifecycle():

    runtime = _start_runtime()

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY
    )

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.DEGRADED
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY
    )

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )

    runtime.stop()

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.STOPPED
    )


# =================================================
# Lifecycle Contract Does Not Own Trading
# =================================================


def test_lifecycle_does_not_grant_trading_permission():

    runtime = _create_runtime()

    assert not hasattr(
        runtime.lifecycle,
        "can_trade",
    )

    assert not hasattr(
        runtime.lifecycle,
        "live_approved",
    )


def test_lifecycle_does_not_own_trading_protection():

    runtime = _create_runtime()

    assert not hasattr(
        runtime.lifecycle,
        "trading_protection",
    )


# =================================================
# Lifecycle Contract Remains Separate
# =================================================


def test_runtime_lifecycle_contract_remains_stateless():

    runtime = _create_runtime()

    assert not hasattr(
        runtime.lifecycle,
        "current_state",
    )

    assert not hasattr(
        runtime.lifecycle,
        "state",
    )


def test_runtime_operational_status_remains_authoritative_state_store():

    runtime = _start_runtime()

    status = runtime.operational_state()

    assert (
        status.state
        == RuntimeOperationalState.RUNNING
    )

    runtime.stop()

    status = runtime.operational_state()

    assert (
        status.state
        == RuntimeOperationalState.STOPPED
    )