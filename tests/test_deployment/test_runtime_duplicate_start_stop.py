"""
=================================================
Project Phoenix
Runtime Duplicate Start / Stop Tests
M62.7.4 - Duplicate Start/Stop Protection
=================================================
"""

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

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )

    return runtime


# =================================================
# Duplicate Start Protection
# =================================================


def test_duplicate_start_is_rejected():

    runtime = _start_runtime()

    result = runtime.start(
        cycles=1,
    )

    assert result is False

    assert runtime.running is True

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )


def test_duplicate_start_does_not_restart_runner():

    runtime = _start_runtime()

    runtime.continuous_runner.start.reset_mock()

    result = runtime.start(
        cycles=1,
    )

    assert result is False

    runtime.continuous_runner.start.assert_not_called()


def test_duplicate_start_does_not_create_new_session():

    runtime = _start_runtime()

    session_id = (
        runtime.session.session_id
    )

    result = runtime.start(
        cycles=1,
    )

    assert result is False

    assert (
        runtime.session.session_id
        == session_id
    )


def test_duplicate_start_does_not_change_session_start_time():

    runtime = _start_runtime()

    started_at = (
        runtime.session.started_at
    )

    runtime.start(
        cycles=1,
    )

    assert (
        runtime.session.started_at
        == started_at
    )


def test_duplicate_start_does_not_change_operational_state():

    runtime = _start_runtime()

    before = (
        runtime.operational_state()
    )

    runtime.start(
        cycles=1,
    )

    after = (
        runtime.operational_state()
    )

    assert (
        after.state
        == before.state
    )


# =================================================
# Duplicate Stop Protection
# =================================================


def test_duplicate_stop_is_safe():

    runtime = _start_runtime()

    runtime.stop()

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.STOPPED
    )

    runtime.stop()

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.STOPPED
    )

    assert runtime.running is False


def test_duplicate_stop_does_not_stop_runner_again():

    runtime = _start_runtime()

    runtime.stop()

    runtime.continuous_runner.stop.reset_mock()

    runtime.stop()

    runtime.continuous_runner.stop.assert_not_called()


def test_duplicate_stop_does_not_change_session():

    runtime = _start_runtime()

    runtime.stop()

    session = runtime.session

    runtime.stop()

    assert (
        runtime.session
        == session
    )


def test_duplicate_stop_does_not_change_stop_time():

    runtime = _start_runtime()

    runtime.stop()

    stopped_at = (
        runtime.session.stopped_at
    )

    runtime.stop()

    assert (
        runtime.session.stopped_at
        == stopped_at
    )


# =================================================
# Start / Stop Sequence Protection
# =================================================


def test_start_stop_sequence():

    runtime = _start_runtime()

    assert runtime.running is True

    runtime.stop()

    assert runtime.running is False

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.STOPPED
    )


def test_stop_before_start_is_safe():

    runtime = _create_runtime()

    runtime.stop()

    assert runtime.running is False

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.STOPPED
    )

    runtime.continuous_runner.stop.assert_not_called()


def test_stop_before_start_does_not_activate_session():

    runtime = _create_runtime()

    session = runtime.session

    runtime.stop()

    assert (
        runtime.session
        == session
    )

    assert runtime.session.active is False

    assert runtime.session.terminal is False


# =================================================
# Session Identity Protection
# =================================================


def test_active_runtime_has_active_session():

    runtime = _start_runtime()

    assert isinstance(
        runtime.session,
        RuntimeSession,
    )

    assert runtime.session.active is True

    assert runtime.session.terminal is False


def test_stopped_runtime_has_terminal_session():

    runtime = _start_runtime()

    runtime.stop()

    assert runtime.session.active is False

    assert runtime.session.terminal is True


def test_duplicate_start_does_not_replace_session_object():

    runtime = _start_runtime()

    session = runtime.session

    runtime.start(
        cycles=1,
    )

    assert (
        runtime.session
        is session
    )


def test_duplicate_stop_does_not_replace_session_object():

    runtime = _start_runtime()

    runtime.stop()

    session = runtime.session

    runtime.stop()

    assert (
        runtime.session
        is session
    )


# =================================================
# Runner Protection
# =================================================


def test_start_calls_runner_exactly_once():

    runtime = _create_runtime()

    runtime.start(
        cycles=1,
    )

    runtime.continuous_runner.start.assert_called_once_with(
        cycles=1,
    )


def test_duplicate_start_keeps_single_runner_start():

    runtime = _create_runtime()

    runtime.start(
        cycles=1,
    )

    runtime.start(
        cycles=1,
    )

    assert (
        runtime.continuous_runner.start.call_count
        == 1
    )


def test_stop_calls_runner_exactly_once():

    runtime = _start_runtime()

    runtime.stop()

    runtime.continuous_runner.stop.assert_called_once()


def test_duplicate_stop_keeps_single_runner_stop():

    runtime = _start_runtime()

    runtime.stop()

    runtime.stop()

    assert (
        runtime.continuous_runner.stop.call_count
        == 1
    )


# =================================================
# Lifecycle State Protection
# =================================================


def test_duplicate_start_does_not_leave_runtime_starting():

    runtime = _start_runtime()

    runtime.start(
        cycles=1,
    )

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )


def test_duplicate_stop_does_not_leave_runtime_stopping():

    runtime = _start_runtime()

    runtime.stop()

    runtime.stop()

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.STOPPED
    )


# =================================================
# Trading Protection Isolation
# =================================================


def test_duplicate_start_does_not_update_trading_protection():

    runtime = _start_runtime()

    runtime.trading_protection.reset_mock()

    runtime.start(
        cycles=1,
    )

    runtime.trading_protection.update.assert_not_called()


def test_duplicate_stop_does_not_update_trading_protection():

    runtime = _start_runtime()

    runtime.stop()

    runtime.trading_protection.reset_mock()

    runtime.stop()

    runtime.trading_protection.update.assert_not_called()


# =================================================
# Alert Isolation
# =================================================


def test_duplicate_start_does_not_dispatch_duplicate_alert():

    runtime = _start_runtime()

    dispatcher = (
        runtime.alert_dispatcher
    )

    dispatcher.reset_mock()

    runtime.start(
        cycles=1,
    )

    dispatcher.dispatch.assert_not_called()


def test_duplicate_stop_does_not_dispatch_duplicate_alert():

    runtime = _start_runtime()

    runtime.stop()

    dispatcher = (
        runtime.alert_dispatcher
    )

    dispatcher.reset_mock()

    runtime.stop()

    dispatcher.dispatch.assert_not_called()


# =================================================
# Final Safety Contract
# =================================================


def test_runtime_has_exactly_one_session_identity():

    runtime = _start_runtime()

    assert isinstance(
        runtime.session,
        RuntimeSession,
    )

    assert runtime.session.session_id


def test_duplicate_operations_do_not_create_new_session_identity():

    runtime = _start_runtime()

    session_id = (
        runtime.session.session_id
    )

    runtime.start(
        cycles=1,
    )

    runtime.stop()

    assert (
        runtime.session.session_id
        == session_id
    )


def test_duplicate_operations_preserve_terminal_session():

    runtime = _start_runtime()

    runtime.stop()

    runtime.stop()

    assert runtime.session.terminal is True

    assert runtime.session.active is False