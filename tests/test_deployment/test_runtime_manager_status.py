"""
=================================================
Project Phoenix
Runtime Manager Status Tests
M62.3.4.4
=================================================
"""

from unittest.mock import MagicMock

from deployment.runtime_manager import (
    RuntimeManager,
)

from deployment.runtime_operational_state import (
    RuntimeOperationalState,
)

from deployment.runtime_status import (
    RuntimeStatus,
)


def _create_manager():

    runtime = MagicMock()

    runtime.running = False

    runtime_status = RuntimeStatus(
        operational_state=(
            RuntimeOperationalState.STOPPED
        ),
        configuration_ready=True,
        deployment_healthy=True,
        runtime_running=False,
        reason="Runtime has not started.",
        timestamp=__import__(
            "datetime"
        ).datetime.now(
            __import__(
                "datetime"
            ).timezone.utc
        ),
    )

    runtime.status_snapshot.return_value = (
        runtime_status
    )

    manager = RuntimeManager(
        runtime=runtime,
    )

    return manager, runtime, runtime_status


# =========================================================
# Test A
# RuntimeManager Returns Structured Runtime Status
# =========================================================

def test_runtime_manager_returns_runtime_status():

    manager, runtime, expected = (
        _create_manager()
    )

    result = manager.runtime_status()

    assert isinstance(
        result,
        RuntimeStatus,
    )

    assert result is expected


# =========================================================
# Test B
# RuntimeManager Delegates To Runtime
# =========================================================

def test_runtime_manager_runtime_status_delegates_to_runtime():

    manager, runtime, expected = (
        _create_manager()
    )

    manager.runtime_status()

    runtime.status_snapshot.assert_called_once()


# =========================================================
# Test C
# Existing Boolean Status Contract Is Preserved
# =========================================================

def test_runtime_manager_status_remains_boolean():

    runtime = MagicMock()

    runtime.running = True

    manager = RuntimeManager(
        runtime=runtime,
    )

    result = manager.status()

    assert result is True

    assert isinstance(
        result,
        bool,
    )


# =========================================================
# Test D
# Structured Status Is Separate From Boolean Status
# =========================================================

def test_structured_status_is_separate_from_boolean_status():

    manager, runtime, expected = (
        _create_manager()
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


# =========================================================
# Test E
# Status Query Does Not Start Runtime
# =========================================================

def test_runtime_status_does_not_start_runtime():

    manager, runtime, expected = (
        _create_manager()
    )

    runtime.start.reset_mock()

    manager.runtime_status()

    runtime.start.assert_not_called()


# =========================================================
# Test F
# Status Query Does Not Stop Runtime
# =========================================================

def test_runtime_status_does_not_stop_runtime():

    manager, runtime, expected = (
        _create_manager()
    )

    runtime.stop.reset_mock()

    manager.runtime_status()

    runtime.stop.assert_not_called()


# =========================================================
# Test G
# Status Query Does Not Trigger Health Watchdog
# =========================================================

def test_runtime_status_does_not_trigger_watchdog():

    manager, runtime, expected = (
        _create_manager()
    )

    manager.watchdog.check = MagicMock()

    manager.runtime_status()

    manager.watchdog.check.assert_not_called()


# =========================================================
# Test H
# Status Query Does Not Change Trading Protection
# =========================================================

def test_runtime_status_does_not_change_trading_protection():

    manager, runtime, expected = (
        _create_manager()
    )

    manager.trading_protection.update = (
        MagicMock()
    )

    manager.runtime_status()

    manager.trading_protection.update.assert_not_called()


# =========================================================
# Test I
# RuntimeManager Does Not Create A New Snapshot
# =========================================================

def test_runtime_manager_uses_runtime_snapshot():

    manager, runtime, expected = (
        _create_manager()
    )

    result = manager.runtime_status()

    assert result is expected


# =========================================================
# Test J
# Runtime Status Preserves Operational State
# =========================================================

def test_runtime_status_preserves_operational_state():

    manager, runtime, expected = (
        _create_manager()
    )

    result = manager.runtime_status()

    assert (
        result.operational_state
        == RuntimeOperationalState.STOPPED
    )


# =========================================================
# Test K
# Runtime Status Preserves Readiness
# =========================================================

def test_runtime_status_preserves_readiness():

    manager, runtime, expected = (
        _create_manager()
    )

    result = manager.runtime_status()

    assert (
        result.configuration_ready
        is True
    )

    assert (
        result.deployment_healthy
        is True
    )


# =========================================================
# Test L
# Runtime Status Preserves Running State
# =========================================================

def test_runtime_status_preserves_running_state():

    manager, runtime, expected = (
        _create_manager()
    )

    result = manager.runtime_status()

    assert (
        result.runtime_running
        is False
    )


# =========================================================
# Test M
# Runtime Status Preserves Reason
# =========================================================

def test_runtime_status_preserves_reason():

    manager, runtime, expected = (
        _create_manager()
    )

    result = manager.runtime_status()

    assert (
        result.reason
        == "Runtime has not started."
    )


# =========================================================
# Test N
# Runtime Status Has Timestamp
# =========================================================

def test_runtime_status_has_timestamp():

    manager, runtime, expected = (
        _create_manager()
    )

    result = manager.runtime_status()

    assert result.timestamp is not None


# =========================================================
# Test O
# Runtime Status Does Not Expose Secrets
# =========================================================

def test_runtime_status_does_not_expose_secrets():

    manager, runtime, expected = (
        _create_manager()
    )

    result = manager.runtime_status()

    assert not hasattr(
        result,
        "password",
    )

    assert not hasattr(
        result,
        "bot_token",
    )

    assert not hasattr(
        result,
        "api_key",
    )


# =========================================================
# Test P
# Runtime Status Does Not Expose Live Approval
# =========================================================

def test_runtime_status_does_not_expose_live_approval():

    manager, runtime, expected = (
        _create_manager()
    )

    result = manager.runtime_status()

    assert not hasattr(
        result,
        "live_approved",
    )


# =========================================================
# Test Q
# Runtime Status Does Not Expose Trading Permission
# =========================================================

def test_runtime_status_does_not_expose_trading_permission():

    manager, runtime, expected = (
        _create_manager()
    )

    result = manager.runtime_status()

    assert not hasattr(
        result,
        "can_trade",
    )


# =========================================================
# Test R
# Runtime Status Does Not Expose MT5 Connection
# =========================================================

def test_runtime_status_does_not_expose_mt5_connection():

    manager, runtime, expected = (
        _create_manager()
    )

    result = manager.runtime_status()

    assert not hasattr(
        result,
        "connected",
    )


# =========================================================
# Test S
# Runtime Status Remains Immutable
# =========================================================

def test_runtime_status_remains_immutable():

    manager, runtime, expected = (
        _create_manager()
    )

    result = manager.runtime_status()

    try:

        result.runtime_running = True

    except (
        AttributeError,
        TypeError,
    ):

        pass

    else:

        raise AssertionError(
            "RuntimeStatus must remain immutable."
        )