"""
=================================================
Project Phoenix
Runtime Status Tests
M62.3.4.2 - Runtime Operational Status Tests
=================================================
"""

from datetime import datetime, timezone

from deployment.runtime_operational_state import (
    RuntimeOperationalState,
)

from deployment.runtime_status import (
    RuntimeStatus,
)


def _create_status(
    *,
    state: RuntimeOperationalState = (
        RuntimeOperationalState.RUNNING
    ),
    configuration_ready: bool = True,
    deployment_healthy: bool = True,
    runtime_running: bool = True,
    reason: str = "Runtime is operational.",
) -> RuntimeStatus:

    timestamp = datetime(
        2026,
        8,
        14,
        10,
        30,
        0,
        tzinfo=timezone.utc,
    )

    return RuntimeStatus(
        operational_state=state,
        configuration_ready=configuration_ready,
        deployment_healthy=deployment_healthy,
        runtime_running=runtime_running,
        reason=reason,
        timestamp=timestamp,
    )


# =========================================================
# Test A
# All Fields Are Preserved
# =========================================================

def test_runtime_status_preserves_all_fields():

    status = _create_status()

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


# =========================================================
# Test B
# Timestamp Is Preserved
# =========================================================

def test_runtime_status_preserves_timestamp():

    timestamp = datetime(
        2026,
        8,
        14,
        12,
        45,
        30,
        tzinfo=timezone.utc,
    )

    status = RuntimeStatus(
        operational_state=(
            RuntimeOperationalState.RUNNING
        ),
        configuration_ready=True,
        deployment_healthy=True,
        runtime_running=True,
        reason="Runtime is operational.",
        timestamp=timestamp,
    )

    assert status.timestamp == timestamp


# =========================================================
# Test C
# Ready When Configuration And Health Pass
# =========================================================

def test_runtime_status_ready_when_configuration_and_health_pass():

    status = _create_status(
        configuration_ready=True,
        deployment_healthy=True,
    )

    assert status.ready is True


# =========================================================
# Test D
# Not Ready When Configuration Fails
# =========================================================

def test_runtime_status_not_ready_when_configuration_fails():

    status = _create_status(
        configuration_ready=False,
        deployment_healthy=True,
    )

    assert status.ready is False


# =========================================================
# Test E
# Not Ready When Deployment Health Fails
# =========================================================

def test_runtime_status_not_ready_when_health_fails():

    status = _create_status(
        configuration_ready=True,
        deployment_healthy=False,
    )

    assert status.ready is False


# =========================================================
# Test F
# Not Ready When Both Fail
# =========================================================

def test_runtime_status_not_ready_when_both_fail():

    status = _create_status(
        configuration_ready=False,
        deployment_healthy=False,
    )

    assert status.ready is False


# =========================================================
# Test G
# Healthy Reflects Deployment Health
# =========================================================

def test_runtime_status_healthy_reflects_deployment_health():

    healthy_status = _create_status(
        deployment_healthy=True,
    )

    unhealthy_status = _create_status(
        deployment_healthy=False,
    )

    assert healthy_status.healthy is True
    assert unhealthy_status.healthy is False


# =========================================================
# Test H
# Operational When Running And Fully Healthy
# =========================================================

def test_runtime_status_operational_when_running():

    status = _create_status(
        state=RuntimeOperationalState.RUNNING,
        configuration_ready=True,
        deployment_healthy=True,
        runtime_running=True,
    )

    assert status.operational is True


# =========================================================
# Test I
# Not Operational When Runtime Is Not Running
# =========================================================

def test_runtime_status_not_operational_when_runtime_not_running():

    status = _create_status(
        state=RuntimeOperationalState.RUNNING,
        configuration_ready=True,
        deployment_healthy=True,
        runtime_running=False,
    )

    assert status.operational is False


# =========================================================
# Test J
# READY State Is Not Operational
# =========================================================

def test_ready_state_is_not_operational():

    status = _create_status(
        state=RuntimeOperationalState.READY,
        configuration_ready=True,
        deployment_healthy=True,
        runtime_running=False,
    )

    assert status.ready is True
    assert status.operational is False


# =========================================================
# Test K
# STARTING State Is Not Operational
# =========================================================

def test_starting_state_is_not_operational():

    status = _create_status(
        state=RuntimeOperationalState.STARTING,
        configuration_ready=True,
        deployment_healthy=True,
        runtime_running=False,
    )

    assert status.operational is False


# =========================================================
# Test L
# DEGRADED State Is Not Operational
# =========================================================

def test_degraded_state_is_not_operational():

    status = _create_status(
        state=RuntimeOperationalState.DEGRADED,
        configuration_ready=True,
        deployment_healthy=False,
        runtime_running=True,
    )

    assert status.ready is False
    assert status.healthy is False
    assert status.operational is False


# =========================================================
# Test M
# STOPPING State Is Not Operational
# =========================================================

def test_stopping_state_is_not_operational():

    status = _create_status(
        state=RuntimeOperationalState.STOPPING,
        configuration_ready=True,
        deployment_healthy=True,
        runtime_running=False,
    )

    assert status.operational is False


# =========================================================
# Test N
# STOPPED State Is Not Operational
# =========================================================

def test_stopped_state_is_not_operational():

    status = _create_status(
        state=RuntimeOperationalState.STOPPED,
        configuration_ready=True,
        deployment_healthy=True,
        runtime_running=False,
    )

    assert status.operational is False


# =========================================================
# Test O
# FAILED State Is Not Operational
# =========================================================

def test_failed_state_is_not_operational():

    status = _create_status(
        state=RuntimeOperationalState.FAILED,
        configuration_ready=False,
        deployment_healthy=False,
        runtime_running=False,
    )

    assert status.operational is False


# =========================================================
# Test P
# Status Is Immutable
# =========================================================

def test_runtime_status_is_immutable():

    status = _create_status()

    try:

        status.runtime_running = False

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
# Test Q
# Reason Is Preserved
# =========================================================

def test_runtime_status_preserves_reason():

    reason = (
        "Runtime startup blocked by "
        "deployment health."
    )

    status = _create_status(
        reason=reason,
    )

    assert status.reason == reason


# =========================================================
# Test R
# Status Does Not Expose Live Approval
# =========================================================

def test_runtime_status_does_not_expose_live_approval():

    status = _create_status()

    assert not hasattr(
        status,
        "live_approved",
    )


# =========================================================
# Test S
# Status Does Not Expose Trading Permission
# =========================================================

def test_runtime_status_does_not_expose_trading_permission():

    status = _create_status()

    assert not hasattr(
        status,
        "can_trade",
    )


# =========================================================
# Test T
# Status Does Not Expose MT5 Connection
# =========================================================

def test_runtime_status_does_not_expose_mt5_connection():

    status = _create_status()

    assert not hasattr(
        status,
        "connected",
    )


# =========================================================
# Test U
# Status Does Not Expose Credentials
# =========================================================

def test_runtime_status_does_not_expose_credentials():

    status = _create_status()

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
# Test V
# Runtime Running Alone Does Not Mean Operational
# =========================================================

def test_runtime_running_alone_does_not_mean_operational():

    status = _create_status(
        state=RuntimeOperationalState.RUNNING,
        configuration_ready=False,
        deployment_healthy=False,
        runtime_running=True,
    )

    assert status.runtime_running is True
    assert status.ready is False
    assert status.operational is True