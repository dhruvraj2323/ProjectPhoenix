"""
=================================================
Project Phoenix
M62.3 Final Integration Tests
M62.3.5 - Integration & Regression
=================================================
"""

from unittest.mock import MagicMock

from config.configuration_readiness_models import (
    ConfigurationReadinessResult,
)

from deployment.runtime import Runtime

from deployment.runtime_manager import (
    RuntimeManager,
)

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


def _failed_configuration():
    return ConfigurationReadinessResult(
        ready=False,
        environment_ready=False,
        mt5_ready=True,
        runtime_ready=True,
        secrets_safe=True,
        errors=(
            "Environment configuration is not ready.",
        ),
    )


def _create_runtime(
    configuration,
    healthy=True,
):
    runtime = Runtime(
        interval=0,
        configuration_readiness=configuration,
    )

    runtime.health_monitor = MagicMock()

    runtime.health_monitor.is_healthy.return_value = (
        healthy
    )

    runtime.continuous_runner = MagicMock()

    return runtime


# =========================================================
# Test A
# Complete Successful Runtime Flow
# =========================================================

def test_m62_3_successful_runtime_flow():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    result = manager.start(
        cycles=1,
    )

    assert result is True

    status = manager.runtime_status()

    assert isinstance(
        status,
        RuntimeStatus,
    )

    assert (
        status.operational_state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        status.configuration_ready
        is True
    )

    assert (
        status.deployment_healthy
        is True
    )

    assert (
        status.runtime_running
        is True
    )

    assert status.ready is True
    assert status.healthy is True
    assert status.operational is True


# =========================================================
# Test B
# Configuration Failure Blocks Complete Flow
# =========================================================

def test_m62_3_configuration_failure_blocks_runtime():

    runtime = _create_runtime(
        _failed_configuration(),
        healthy=True,
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    result = manager.start(
        cycles=1,
    )

    assert result is False

    status = manager.runtime_status()

    assert (
        status.operational_state
        == RuntimeOperationalState.FAILED
    )

    assert (
        status.configuration_ready
        is False
    )

    assert (
        status.runtime_running
        is False
    )

    assert status.ready is False
    assert status.operational is False

    runtime.health_monitor.is_healthy.assert_called_once()

    runtime.continuous_runner.start.assert_not_called()


# =========================================================
# Test C
# Health Failure Blocks Complete Flow
# =========================================================

def test_m62_3_health_failure_blocks_runtime():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=False,
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    result = manager.start(
        cycles=1,
    )

    assert result is False

    status = manager.runtime_status()

    assert (
        status.operational_state
        == RuntimeOperationalState.FAILED
    )

    assert (
        status.configuration_ready
        is True
    )

    assert (
        status.deployment_healthy
        is False
    )

    assert (
        status.runtime_running
        is False
    )

    assert status.ready is False
    assert status.healthy is False
    assert status.operational is False

    runtime.continuous_runner.start.assert_not_called()


# =========================================================
# Test D
# Runtime Stop Flow
# =========================================================

def test_m62_3_stop_flow():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    assert manager.start(
        cycles=1,
    ) is True

    manager.stop()

    status = manager.runtime_status()

    assert (
        status.operational_state
        == RuntimeOperationalState.STOPPED
    )

    assert (
        status.runtime_running
        is False
    )

    assert status.operational is False

    runtime.continuous_runner.stop.assert_called_once()


# =========================================================
# Test E
# Runner Failure Produces Failed Runtime
# =========================================================

def test_m62_3_runner_failure():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    runtime.continuous_runner.start.side_effect = (
        RuntimeError(
            "Simulated runner failure."
        )
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    result = manager.start(
        cycles=1,
    )

    assert result is False

    status = manager.runtime_status()

    assert (
        status.operational_state
        == RuntimeOperationalState.FAILED
    )

    assert (
        status.runtime_running
        is False
    )

    assert status.operational is False


# =========================================================
# Test F
# RuntimeManager Boolean Status Contract
# =========================================================

def test_m62_3_existing_boolean_status_contract():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    assert manager.start(
        cycles=1,
    ) is True

    assert (
        manager.status()
        is True
    )

    assert isinstance(
        manager.status(),
        bool,
    )


# =========================================================
# Test G
# Structured Status Is Available Alongside Boolean Status
# =========================================================

def test_m62_3_boolean_and_structured_status_coexist():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    manager.start(
        cycles=1,
    )

    boolean_status = manager.status()

    structured_status = (
        manager.runtime_status()
    )

    assert isinstance(
        boolean_status,
        bool,
    )

    assert isinstance(
        structured_status,
        RuntimeStatus,
    )

    assert (
        boolean_status
        == structured_status.runtime_running
    )


# =========================================================
# Test H
# Health Watchdog Remains Independent
# =========================================================

def test_m62_3_watchdog_remains_independent():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    watchdog = MagicMock()

    watchdog.check.return_value = (
        WatchdogHealthState.HEALTHY
    )

    protection = MagicMock()

    protection.state = (
        TradingProtectionState.ACTIVE
    )

    manager = RuntimeManager(
        runtime=runtime,
        watchdog=watchdog,
        trading_protection=protection,
    )

    manager.start(
        cycles=1,
    )

    status = manager.runtime_status()

    assert (
        status.operational_state
        == RuntimeOperationalState.RUNNING
    )

    watchdog.check.assert_not_called()

    manager.health_state()

    watchdog.check.assert_called_once()


# =========================================================
# Test I
# Trading Protection Remains Independent
# =========================================================

def test_m62_3_trading_protection_remains_independent():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    protection = MagicMock()

    protection.state = (
        TradingProtectionState.ACTIVE
    )

    protection.can_trade.return_value = True

    manager = RuntimeManager(
        runtime=runtime,
        trading_protection=protection,
    )

    manager.start(
        cycles=1,
    )

    manager.runtime_status()

    protection.update.assert_not_called()

    assert (
        manager.can_trade()
        is True
    )


# =========================================================
# Test J
# Runtime Status Does Not Grant Trading Permission
# =========================================================

def test_m62_3_runtime_status_does_not_grant_trading_permission():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    manager.start(
        cycles=1,
    )

    status = manager.runtime_status()

    assert not hasattr(
        status,
        "can_trade",
    )

    assert not hasattr(
        status,
        "live_approved",
    )


# =========================================================
# Test K
# Runtime Status Does Not Expose Secrets
# =========================================================

def test_m62_3_runtime_status_does_not_expose_secrets():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    status = manager.runtime_status()

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
# Test L
# Runtime Status Does Not Start Or Stop Runtime
# =========================================================

def test_m62_3_status_query_is_observational_only():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    runtime.start = MagicMock()
    runtime.stop = MagicMock()

    manager = RuntimeManager(
        runtime=runtime,
    )

    manager.runtime_status()

    runtime.start.assert_not_called()
    runtime.stop.assert_not_called()


# =========================================================
# Test M
# Runtime Status Snapshot Is Immutable
# =========================================================

def test_m62_3_runtime_status_is_immutable():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    status = manager.runtime_status()

    try:

        status.runtime_running = True

    except (
        AttributeError,
        TypeError,
    ):

        pass

    else:

        raise AssertionError(
            "RuntimeStatus must be immutable."
        )


# =========================================================
# Test N
# Restart Preserves Readiness Gate
# =========================================================

def test_m62_3_restart_preserves_readiness_gate():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    assert manager.restart(
        cycles=1,
    ) is True

    status = manager.runtime_status()

    assert (
        status.operational_state
        == RuntimeOperationalState.RUNNING
    )

    assert status.configuration_ready is True
    assert status.deployment_healthy is True


# =========================================================
# Test O
# Failed Configuration Prevents Runner Execution
# =========================================================

def test_m62_3_failed_configuration_prevents_runner_execution():

    runtime = _create_runtime(
        _failed_configuration(),
        healthy=True,
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    manager.start(
        cycles=1,
    )

    runtime.continuous_runner.start.assert_not_called()

    status = manager.runtime_status()

    assert (
        status.operational_state
        == RuntimeOperationalState.FAILED
    )


# =========================================================
# Test P
# Successful Runtime Has Timestamp
# =========================================================

def test_m62_3_successful_status_has_timestamp():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    manager.start(
        cycles=1,
    )

    status = manager.runtime_status()

    assert status.timestamp is not None


# =========================================================
# Test Q
# Runtime Status Reason Is Meaningful
# =========================================================

def test_m62_3_successful_status_has_meaningful_reason():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    manager.start(
        cycles=1,
    )

    status = manager.runtime_status()

    assert (
        status.reason
        == "Runtime is operational."
    )


# =========================================================
# Test R
# Configuration Failure Reason Is Observable
# =========================================================

def test_m62_3_configuration_failure_reason_is_observable():

    runtime = _create_runtime(
        _failed_configuration(),
        healthy=True,
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    manager.start(
        cycles=1,
    )

    status = manager.runtime_status()

    assert (
        "configuration readiness"
        in status.reason.lower()
    )


# =========================================================
# Test S
# Runtime Health Failure Reason Is Observable
# =========================================================

def test_m62_3_health_failure_reason_is_observable():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=False,
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    manager.start(
        cycles=1,
    )

    status = manager.runtime_status()

    assert (
        "deployment health"
        in status.reason.lower()
    )


# =========================================================
# Test T
# Runtime Operational State Matches Running Flag
# =========================================================

def test_m62_3_running_state_matches_running_flag():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    manager.start(
        cycles=1,
    )

    status = manager.runtime_status()

    assert (
        status.operational_state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        status.runtime_running
        is True
    )

    assert (
        status.operational
        is True
    )


# =========================================================
# Test U
# Final M62.3 Architecture Boundary
# =========================================================

def test_m62_3_architecture_boundary():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    manager.start(
        cycles=1,
    )

    status = manager.runtime_status()

    # Runtime observability is exposed.
    assert isinstance(
        status,
        RuntimeStatus,
    )

    # Runtime state is exposed.
    assert (
        status.operational_state
        == RuntimeOperationalState.RUNNING
    )

    # Configuration and health are exposed.
    assert status.configuration_ready is True
    assert status.deployment_healthy is True

    # Trading authority is NOT exposed.
    assert not hasattr(
        status,
        "can_trade",
    )

    assert not hasattr(
        status,
        "live_approved",
    )

    # Secrets are NOT exposed.
    assert not hasattr(
        status,
        "password",
    )

    assert not hasattr(
        status,
        "bot_token",
    )