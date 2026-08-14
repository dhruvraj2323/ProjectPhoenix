"""
=================================================
Project Phoenix
Runtime Operational State Tests
M62.3.3.2
=================================================
"""

from deployment.runtime_operational_state import (
    RuntimeOperationalState,
    RuntimeOperationalStatus,
)


def test_all_runtime_operational_states_exist():

    assert (
        RuntimeOperationalState.STARTING.value
        == "STARTING"
    )

    assert (
        RuntimeOperationalState.READY.value
        == "READY"
    )

    assert (
        RuntimeOperationalState.RUNNING.value
        == "RUNNING"
    )

    assert (
        RuntimeOperationalState.DEGRADED.value
        == "DEGRADED"
    )

    assert (
        RuntimeOperationalState.STOPPING.value
        == "STOPPING"
    )

    assert (
        RuntimeOperationalState.STOPPED.value
        == "STOPPED"
    )

    assert (
        RuntimeOperationalState.FAILED.value
        == "FAILED"
    )


def test_running_is_true_only_for_running_state():

    status = RuntimeOperationalStatus(
        state=RuntimeOperationalState.RUNNING,
        reason="Runtime is operational.",
    )

    assert status.running is True


def test_running_is_false_for_non_running_states():

    non_running_states = (
        RuntimeOperationalState.STARTING,
        RuntimeOperationalState.READY,
        RuntimeOperationalState.DEGRADED,
        RuntimeOperationalState.STOPPING,
        RuntimeOperationalState.STOPPED,
        RuntimeOperationalState.FAILED,
    )

    for state in non_running_states:

        status = RuntimeOperationalStatus(
            state=state,
            reason="Test state.",
        )

        assert status.running is False


def test_stopped_is_terminal():

    status = RuntimeOperationalStatus(
        state=RuntimeOperationalState.STOPPED,
        reason="Runtime stopped.",
    )

    assert status.terminal is True


def test_failed_is_terminal():

    status = RuntimeOperationalStatus(
        state=RuntimeOperationalState.FAILED,
        reason="Runtime failed.",
    )

    assert status.terminal is True


def test_starting_is_not_terminal():

    status = RuntimeOperationalStatus(
        state=RuntimeOperationalState.STARTING,
        reason="Runtime starting.",
    )

    assert status.terminal is False


def test_ready_is_not_terminal():

    status = RuntimeOperationalStatus(
        state=RuntimeOperationalState.READY,
        reason="Runtime ready.",
    )

    assert status.terminal is False


def test_running_is_not_terminal():

    status = RuntimeOperationalStatus(
        state=RuntimeOperationalState.RUNNING,
        reason="Runtime running.",
    )

    assert status.terminal is False


def test_degraded_is_not_terminal():

    status = RuntimeOperationalStatus(
        state=RuntimeOperationalState.DEGRADED,
        reason="Runtime degraded.",
    )

    assert status.terminal is False


def test_stopping_is_not_terminal():

    status = RuntimeOperationalStatus(
        state=RuntimeOperationalState.STOPPING,
        reason="Runtime stopping.",
    )

    assert status.terminal is False


def test_reason_is_preserved():

    reason = "Configuration readiness passed."

    status = RuntimeOperationalStatus(
        state=RuntimeOperationalState.READY,
        reason=reason,
    )

    assert status.reason == reason


def test_status_is_immutable():

    status = RuntimeOperationalStatus(
        state=RuntimeOperationalState.RUNNING,
        reason="Runtime is operational.",
    )

    try:

        status.state = (
            RuntimeOperationalState.FAILED
        )

    except (
        AttributeError,
        TypeError,
    ):

        pass

    else:

        raise AssertionError(
            "RuntimeOperationalStatus must be immutable."
        )


def test_state_enum_members_are_unique():

    values = [
        state.value
        for state in RuntimeOperationalState
    ]

    assert len(values) == len(set(values))


def test_terminal_states_are_exactly_stopped_and_failed():

    terminal_states = {
        state
        for state in RuntimeOperationalState
        if RuntimeOperationalStatus(
            state=state,
            reason="Test.",
        ).terminal
    }

    assert terminal_states == {
        RuntimeOperationalState.STOPPED,
        RuntimeOperationalState.FAILED,
    }


def test_only_running_state_reports_running():

    running_states = {
        state
        for state in RuntimeOperationalState
        if RuntimeOperationalStatus(
            state=state,
            reason="Test.",
        ).running
    }

    assert running_states == {
        RuntimeOperationalState.RUNNING,
    }