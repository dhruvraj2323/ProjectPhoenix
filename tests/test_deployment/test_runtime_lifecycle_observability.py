"""
=================================================
Project Phoenix
Runtime Lifecycle Observability Tests
M62.7.5 - Lifecycle Observability
=================================================
"""

from datetime import datetime

from unittest.mock import MagicMock

from config.configuration_readiness_models import (
    ConfigurationReadinessResult,
)

from deployment.runtime import (
    Runtime,
)

from deployment.runtime_operational_state import (
    RuntimeOperationalState,
)

from deployment.runtime_session import (
    RuntimeSession,
)

from deployment.runtime_status import (
    RuntimeStatus,
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

    assert runtime.running is True

    return runtime


# =================================================
# Runtime Status Snapshot
# =================================================


def test_status_snapshot_returns_runtime_status():

    runtime = _create_runtime()

    snapshot = (
        runtime.status_snapshot()
    )

    assert isinstance(
        snapshot,
        RuntimeStatus,
    )


def test_initial_status_snapshot_reports_stopped():

    runtime = _create_runtime()

    snapshot = (
        runtime.status_snapshot()
    )

    assert (
        snapshot.operational_state
        == RuntimeOperationalState.STOPPED
    )


def test_initial_status_snapshot_reports_runtime_not_running():

    runtime = _create_runtime()

    snapshot = (
        runtime.status_snapshot()
    )

    assert snapshot.runtime_running is False


def test_initial_status_snapshot_reports_configuration_ready():

    runtime = _create_runtime()

    snapshot = (
        runtime.status_snapshot()
    )

    assert snapshot.configuration_ready is True


def test_initial_status_snapshot_reports_deployment_health():

    runtime = _create_runtime()

    snapshot = (
        runtime.status_snapshot()
    )

    assert snapshot.deployment_healthy is True


def test_status_snapshot_contains_reason():

    runtime = _create_runtime()

    snapshot = (
        runtime.status_snapshot()
    )

    assert isinstance(
        snapshot.reason,
        str,
    )

    assert snapshot.reason


def test_status_snapshot_contains_timestamp():

    runtime = _create_runtime()

    snapshot = (
        runtime.status_snapshot()
    )

    assert isinstance(
        snapshot.timestamp,
        datetime,
    )


# =================================================
# Running Observability
# =================================================


def test_running_status_snapshot_reports_running():

    runtime = _start_runtime()

    snapshot = (
        runtime.status_snapshot()
    )

    assert (
        snapshot.operational_state
        == RuntimeOperationalState.RUNNING
    )


def test_running_status_snapshot_reports_runtime_running():

    runtime = _start_runtime()

    snapshot = (
        runtime.status_snapshot()
    )

    assert snapshot.runtime_running is True


def test_running_status_snapshot_reports_configuration_ready():

    runtime = _start_runtime()

    snapshot = (
        runtime.status_snapshot()
    )

    assert snapshot.configuration_ready is True


def test_running_status_snapshot_reports_deployment_health():

    runtime = _start_runtime()

    snapshot = (
        runtime.status_snapshot()
    )

    assert snapshot.deployment_healthy is True


def test_running_status_snapshot_contains_reason():

    runtime = _start_runtime()

    snapshot = (
        runtime.status_snapshot()
    )

    assert snapshot.reason

    assert isinstance(
        snapshot.reason,
        str,
    )


# =================================================
# Degraded Observability
# =================================================


def test_degraded_status_snapshot_reports_degraded():

    runtime = _start_runtime()

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY
    )

    snapshot = (
        runtime.status_snapshot()
    )

    assert (
        snapshot.operational_state
        == RuntimeOperationalState.DEGRADED
    )


def test_degraded_status_snapshot_keeps_runtime_running():

    runtime = _start_runtime()

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY
    )

    snapshot = (
        runtime.status_snapshot()
    )

    assert snapshot.runtime_running is True


def test_degraded_status_snapshot_contains_reason():

    runtime = _start_runtime()

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY
    )

    snapshot = (
        runtime.status_snapshot()
    )

    assert snapshot.reason

    assert isinstance(
        snapshot.reason,
        str,
    )


# =================================================
# Recovery Observability
# =================================================


def test_recovery_status_snapshot_reports_running():

    runtime = _start_runtime()

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY
    )

    snapshot = (
        runtime.status_snapshot()
    )

    assert (
        snapshot.operational_state
        == RuntimeOperationalState.RUNNING
    )


def test_recovery_status_snapshot_reports_runtime_running():

    runtime = _start_runtime()

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY
    )

    snapshot = (
        runtime.status_snapshot()
    )

    assert snapshot.runtime_running is True


def test_recovery_status_snapshot_contains_reason():

    runtime = _start_runtime()

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY
    )

    snapshot = (
        runtime.status_snapshot()
    )

    assert snapshot.reason

    assert isinstance(
        snapshot.reason,
        str,
    )


# =================================================
# Shutdown Observability
# =================================================


def test_stopped_status_snapshot_reports_stopped():

    runtime = _start_runtime()

    runtime.stop()

    snapshot = (
        runtime.status_snapshot()
    )

    assert (
        snapshot.operational_state
        == RuntimeOperationalState.STOPPED
    )


def test_stopped_status_snapshot_reports_not_running():

    runtime = _start_runtime()

    runtime.stop()

    snapshot = (
        runtime.status_snapshot()
    )

    assert snapshot.runtime_running is False


def test_stopped_status_snapshot_contains_reason():

    runtime = _start_runtime()

    runtime.stop()

    snapshot = (
        runtime.status_snapshot()
    )

    assert snapshot.reason

    assert isinstance(
        snapshot.reason,
        str,
    )


# =================================================
# Session Observability
# =================================================


def test_runtime_exposes_session():

    runtime = _create_runtime()

    assert hasattr(
        runtime,
        "session",
    )


def test_runtime_session_has_expected_type():

    runtime = _create_runtime()

    assert isinstance(
        runtime.session,
        RuntimeSession,
    )


def test_runtime_session_exposes_identity():

    runtime = _create_runtime()

    assert isinstance(
        runtime.session.session_id,
        str,
    )

    assert runtime.session.session_id


def test_session_becomes_active_after_start():

    runtime = _start_runtime()

    assert runtime.session.active is True

    assert runtime.session.terminal is False


def test_session_records_start_time():

    runtime = _start_runtime()

    assert (
        runtime.session.started_at
        is not None
    )

    assert isinstance(
        runtime.session.started_at,
        datetime,
    )


def test_session_becomes_terminal_after_stop():

    runtime = _start_runtime()

    runtime.stop()

    assert runtime.session.active is False

    assert runtime.session.terminal is True


def test_session_records_stop_time():

    runtime = _start_runtime()

    runtime.stop()

    assert (
        runtime.session.stopped_at
        is not None
    )

    assert isinstance(
        runtime.session.stopped_at,
        datetime,
    )


# =================================================
# Session Identity Stability
# =================================================


def test_session_identity_remains_stable_during_runtime():

    runtime = _start_runtime()

    session_id = (
        runtime.session.session_id
    )

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY
    )

    runtime.apply_health_state(
        WatchdogHealthState.HEALTHY
    )

    assert (
        runtime.session.session_id
        == session_id
    )


def test_session_identity_remains_stable_after_stop():

    runtime = _start_runtime()

    session_id = (
        runtime.session.session_id
    )

    runtime.stop()

    assert (
        runtime.session.session_id
        == session_id
    )


# =================================================
# Observability Does Not Control Trading
# =================================================


def test_status_snapshot_does_not_grant_trading_permission():

    runtime = _create_runtime()

    snapshot = (
        runtime.status_snapshot()
    )

    assert not hasattr(
        snapshot,
        "can_trade",
    )

    assert not hasattr(
        snapshot,
        "live_approved",
    )


def test_session_does_not_grant_trading_permission():

    runtime = _create_runtime()

    assert not hasattr(
        runtime.session,
        "can_trade",
    )

    assert not hasattr(
        runtime.session,
        "live_approved",
    )


def test_session_does_not_own_trading_protection():

    runtime = _create_runtime()

    assert not hasattr(
        runtime.session,
        "trading_protection",
    )


# =================================================
# Observability Does Not Mutate Runtime
# =================================================


def test_status_snapshot_does_not_change_runtime_state():

    runtime = _start_runtime()

    before = (
        runtime.operational_state().state
    )

    runtime.status_snapshot()

    after = (
        runtime.operational_state().state
    )

    assert before == after


def test_status_snapshot_does_not_change_running_flag():

    runtime = _start_runtime()

    before = runtime.running

    runtime.status_snapshot()

    after = runtime.running

    assert before == after


def test_status_snapshot_does_not_change_session():

    runtime = _start_runtime()

    session = runtime.session

    runtime.status_snapshot()

    assert (
        runtime.session
        is session
    )


# =================================================
# Lifecycle Observability
# =================================================


def test_lifecycle_contract_is_exposed():

    runtime = _create_runtime()

    assert hasattr(
        runtime,
        "lifecycle",
    )


def test_lifecycle_contract_is_runtime_lifecycle():

    from deployment.runtime_lifecycle import (
        RuntimeLifecycle,
    )

    runtime = _create_runtime()

    assert isinstance(
        runtime.lifecycle,
        RuntimeLifecycle,
    )


def test_lifecycle_contract_does_not_store_runtime_state():

    runtime = _create_runtime()

    assert not hasattr(
        runtime.lifecycle,
        "current_state",
    )

    assert not hasattr(
        runtime.lifecycle,
        "state",
    )


# =================================================
# Timestamp Ordering
# =================================================


def test_session_start_precedes_session_stop():

    runtime = _start_runtime()

    runtime.stop()

    assert (
        runtime.session.started_at
        is not None
    )

    assert (
        runtime.session.stopped_at
        is not None
    )

    assert (
        runtime.session.started_at
        <= runtime.session.stopped_at
    )


def test_status_snapshot_timestamp_is_available_after_start():

    runtime = _start_runtime()

    snapshot = (
        runtime.status_snapshot()
    )

    assert (
        snapshot.timestamp
        is not None
    )


def test_status_snapshot_timestamp_is_available_after_stop():

    runtime = _start_runtime()

    runtime.stop()

    snapshot = (
        runtime.status_snapshot()
    )

    assert (
        snapshot.timestamp
        is not None
    )