"""
=================================================
Project Phoenix
Runtime Status Integration Tests
M62.3.4.3
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


def _ready_configuration():
    return ConfigurationReadinessResult(
        ready=True,
        environment_ready=True,
        mt5_ready=True,
        runtime_ready=True,
        secrets_safe=True,
    )


def _not_ready_configuration():
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
# Initial Status Snapshot
# =========================================================

def test_initial_runtime_status_snapshot():

    runtime = _create_runtime(
        _ready_configuration()
    )

    status = runtime.status_snapshot()

    assert (
        status.operational_state
        == RuntimeOperationalState.STOPPED
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
        is False
    )

    assert (
        status.reason
        == "Runtime has not started."
    )


# =========================================================
# Test B
# Ready Runtime Status
# =========================================================

def test_runtime_status_after_successful_start():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    result = runtime.start(
        cycles=1,
    )

    assert result is True

    status = runtime.status_snapshot()

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

    assert (
        status.reason
        == "Runtime is operational."
    )

    assert status.ready is True

    assert status.healthy is True

    assert status.operational is True


# =========================================================
# Test C
# Configuration Failure Status
# =========================================================

def test_runtime_status_after_configuration_failure():

    runtime = _create_runtime(
        _not_ready_configuration(),
        healthy=True,
    )

    result = runtime.start(
        cycles=1,
    )

    assert result is False

    status = runtime.status_snapshot()

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

    assert (
        status.ready
        is False
    )

    assert (
        status.operational
        is False
    )


# =========================================================
# Test D
# Health Failure Status
# =========================================================

def test_runtime_status_after_health_failure():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=False,
    )

    result = runtime.start(
        cycles=1,
    )

    assert result is False

    status = runtime.status_snapshot()

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

    assert (
        status.ready
        is False
    )

    assert (
        status.healthy
        is False
    )


# =========================================================
# Test E
# Runtime Stop Status
# =========================================================

def test_runtime_status_after_stop():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    runtime.start(
        cycles=1,
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
        status.reason
        == "Runtime stopped."
    )

    assert (
        status.operational
        is False
    )


# =========================================================
# Test F
# Runner Failure Status
# =========================================================

def test_runtime_status_after_runner_failure():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    runtime.continuous_runner.start.side_effect = (
        RuntimeError(
            "Simulated runner failure."
        )
    )

    result = runtime.start(
        cycles=1,
    )

    assert result is False

    status = runtime.status_snapshot()

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
        is True
    )

    assert (
        status.runtime_running
        is False
    )

    assert (
        status.operational
        is False
    )


# =========================================================
# Test G
# Snapshot Is Immutable
# =========================================================

def test_runtime_status_snapshot_is_immutable():

    runtime = _create_runtime(
        _ready_configuration()
    )

    status = runtime.status_snapshot()

    try:

        status.runtime_running = True

    except (
        AttributeError,
        TypeError,
    ):

        pass

    else:

        raise AssertionError(
            "Runtime status snapshot must be immutable."
        )


# =========================================================
# Test H
# Snapshot Has Timestamp
# =========================================================

def test_runtime_status_snapshot_has_timestamp():

    runtime = _create_runtime(
        _ready_configuration()
    )

    status = runtime.status_snapshot()

    assert status.timestamp is not None


# =========================================================
# Test I
# Snapshot Does Not Expose Secrets
# =========================================================

def test_runtime_status_snapshot_does_not_expose_secrets():

    runtime = _create_runtime(
        _ready_configuration()
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
# Snapshot Does Not Expose Live Approval
# =========================================================

def test_runtime_status_snapshot_does_not_expose_live_approval():

    runtime = _create_runtime(
        _ready_configuration()
    )

    status = runtime.status_snapshot()

    assert not hasattr(
        status,
        "live_approved",
    )


# =========================================================
# Test K
# Snapshot Does Not Expose Trading Permission
# =========================================================

def test_runtime_status_snapshot_does_not_expose_trading_permission():

    runtime = _create_runtime(
        _ready_configuration()
    )

    status = runtime.status_snapshot()

    assert not hasattr(
        status,
        "can_trade",
    )


# =========================================================
# Test L
# Snapshot Does Not Expose MT5 Connection
# =========================================================

def test_runtime_status_snapshot_does_not_expose_mt5_connection():

    runtime = _create_runtime(
        _ready_configuration()
    )

    status = runtime.status_snapshot()

    assert not hasattr(
        status,
        "connected",
    )


# =========================================================
# Test M
# Configuration Readiness Is Reflected
# =========================================================

def test_status_reflects_configuration_readiness():

    runtime = _create_runtime(
        _not_ready_configuration(),
        healthy=True,
    )

    status = runtime.status_snapshot()

    assert (
        status.configuration_ready
        is False
    )


# =========================================================
# Test N
# Deployment Health Is Reflected
# =========================================================

def test_status_reflects_deployment_health():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=False,
    )

    status = runtime.status_snapshot()

    assert (
        status.deployment_healthy
        is False
    )


# =========================================================
# Test O
# Runtime Running State Is Reflected
# =========================================================

def test_status_reflects_runtime_running_state():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    runtime.running = True

    status = runtime.status_snapshot()

    assert (
        status.runtime_running
        is True
    )


# =========================================================
# Test P
# Snapshot Reason Matches Operational State
# =========================================================

def test_snapshot_reason_matches_operational_state():

    runtime = _create_runtime(
        _not_ready_configuration(),
        healthy=True,
    )

    runtime.start(
        cycles=1,
    )

    status = runtime.status_snapshot()

    assert (
        status.operational_state
        == RuntimeOperationalState.FAILED
    )

    assert (
        "configuration readiness"
        in status.reason.lower()
    )


# =========================================================
# Test Q
# Status Snapshot Is A Separate Object
# =========================================================

def test_status_snapshot_returns_separate_snapshot():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    first = runtime.status_snapshot()
    second = runtime.status_snapshot()

    assert first is not second

    assert (
        first.operational_state
        == second.operational_state
    )

    assert (
        first.configuration_ready
        == second.configuration_ready
    )


# =========================================================
# Test R
# Status Snapshot Does Not Start Runtime
# =========================================================

def test_status_snapshot_does_not_start_runtime():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    runtime.continuous_runner.start.reset_mock()

    runtime.status_snapshot()

    runtime.continuous_runner.start.assert_not_called()


# =========================================================
# Test S
# Status Snapshot Does Not Stop Runtime
# =========================================================

def test_status_snapshot_does_not_stop_runtime():

    runtime = _create_runtime(
        _ready_configuration(),
        healthy=True,
    )

    runtime.continuous_runner.stop.reset_mock()

    runtime.status_snapshot()

    runtime.continuous_runner.stop.assert_not_called()