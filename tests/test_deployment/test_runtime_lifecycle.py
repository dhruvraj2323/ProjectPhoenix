"""
=================================================
Project Phoenix
Runtime Lifecycle Transition Tests
M62.7.1 - Runtime Lifecycle Transition Contract
=================================================
"""

from deployment.runtime_operational_state import (
    RuntimeOperationalState,
)


# =================================================
# Expected Lifecycle States
# =================================================


def test_runtime_lifecycle_contains_required_states():

    required_states = {
        RuntimeOperationalState.STARTING,
        RuntimeOperationalState.READY,
        RuntimeOperationalState.RUNNING,
        RuntimeOperationalState.DEGRADED,
        RuntimeOperationalState.STOPPING,
        RuntimeOperationalState.STOPPED,
        RuntimeOperationalState.FAILED,
    }

    available_states = set(
        RuntimeOperationalState
    )

    assert required_states.issubset(
        available_states
    )


# =================================================
# Helper
# =================================================


def _transition_contract():

    return {
        RuntimeOperationalState.STARTING: {
            RuntimeOperationalState.READY,
            RuntimeOperationalState.FAILED,
        },
        RuntimeOperationalState.READY: {
            RuntimeOperationalState.RUNNING,
            RuntimeOperationalState.FAILED,
        },
        RuntimeOperationalState.RUNNING: {
            RuntimeOperationalState.DEGRADED,
            RuntimeOperationalState.STOPPING,
            RuntimeOperationalState.FAILED,
        },
        RuntimeOperationalState.DEGRADED: {
            RuntimeOperationalState.RUNNING,
            RuntimeOperationalState.STOPPING,
            RuntimeOperationalState.FAILED,
        },
        RuntimeOperationalState.STOPPING: {
            RuntimeOperationalState.STOPPED,
        },
        RuntimeOperationalState.STOPPED: set(),
        RuntimeOperationalState.FAILED: set(),
    }


# =================================================
# Valid Lifecycle Transitions
# =================================================


def test_starting_can_transition_to_ready():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.READY
        in contract[
            RuntimeOperationalState.STARTING
        ]
    )


def test_starting_can_transition_to_failed():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.FAILED
        in contract[
            RuntimeOperationalState.STARTING
        ]
    )


def test_ready_can_transition_to_running():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.RUNNING
        in contract[
            RuntimeOperationalState.READY
        ]
    )


def test_ready_can_transition_to_failed():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.FAILED
        in contract[
            RuntimeOperationalState.READY
        ]
    )


def test_running_can_transition_to_degraded():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.DEGRADED
        in contract[
            RuntimeOperationalState.RUNNING
        ]
    )


def test_running_can_transition_to_stopping():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.STOPPING
        in contract[
            RuntimeOperationalState.RUNNING
        ]
    )


def test_running_can_transition_to_failed():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.FAILED
        in contract[
            RuntimeOperationalState.RUNNING
        ]
    )


def test_degraded_can_transition_to_running():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.RUNNING
        in contract[
            RuntimeOperationalState.DEGRADED
        ]
    )


def test_degraded_can_transition_to_stopping():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.STOPPING
        in contract[
            RuntimeOperationalState.DEGRADED
        ]
    )


def test_degraded_can_transition_to_failed():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.FAILED
        in contract[
            RuntimeOperationalState.DEGRADED
        ]
    )


def test_stopping_can_transition_to_stopped():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.STOPPED
        in contract[
            RuntimeOperationalState.STOPPING
        ]
    )


# =================================================
# Terminal States
# =================================================


def test_stopped_has_no_outgoing_transitions():

    contract = _transition_contract()

    assert (
        contract[
            RuntimeOperationalState.STOPPED
        ]
        == set()
    )


def test_failed_has_no_outgoing_transitions():

    contract = _transition_contract()

    assert (
        contract[
            RuntimeOperationalState.FAILED
        ]
        == set()
    )


# =================================================
# Invalid Lifecycle Transitions
# =================================================


def test_starting_cannot_directly_transition_to_running():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.RUNNING
        not in contract[
            RuntimeOperationalState.STARTING
        ]
    )


def test_starting_cannot_directly_transition_to_stopped():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.STOPPED
        not in contract[
            RuntimeOperationalState.STARTING
        ]
    )


def test_ready_cannot_transition_to_degraded():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.DEGRADED
        not in contract[
            RuntimeOperationalState.READY
        ]
    )


def test_ready_cannot_transition_to_stopping():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.STOPPING
        not in contract[
            RuntimeOperationalState.READY
        ]
    )


def test_running_cannot_directly_transition_to_stopped():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.STOPPED
        not in contract[
            RuntimeOperationalState.RUNNING
        ]
    )


def test_running_cannot_transition_back_to_starting():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.STARTING
        not in contract[
            RuntimeOperationalState.RUNNING
        ]
    )


def test_degraded_cannot_transition_to_ready():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.READY
        not in contract[
            RuntimeOperationalState.DEGRADED
        ]
    )


def test_degraded_cannot_transition_back_to_starting():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.STARTING
        not in contract[
            RuntimeOperationalState.DEGRADED
        ]
    )


def test_stopping_cannot_transition_back_to_running():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.RUNNING
        not in contract[
            RuntimeOperationalState.STOPPING
        ]
    )


def test_stopping_cannot_transition_to_failed():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.FAILED
        not in contract[
            RuntimeOperationalState.STOPPING
        ]
    )


def test_stopped_cannot_restart_directly():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.STARTING
        not in contract[
            RuntimeOperationalState.STOPPED
        ]
    )

    assert (
        RuntimeOperationalState.RUNNING
        not in contract[
            RuntimeOperationalState.STOPPED
        ]
    )


def test_failed_cannot_recover_directly():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.STARTING
        not in contract[
            RuntimeOperationalState.FAILED
        ]
    )

    assert (
        RuntimeOperationalState.RUNNING
        not in contract[
            RuntimeOperationalState.FAILED
        ]
    )


# =================================================
# Complete Normal Lifecycle
# =================================================


def test_complete_normal_lifecycle_is_valid():

    contract = _transition_contract()

    lifecycle = [
        RuntimeOperationalState.STARTING,
        RuntimeOperationalState.READY,
        RuntimeOperationalState.RUNNING,
        RuntimeOperationalState.STOPPING,
        RuntimeOperationalState.STOPPED,
    ]

    for current_state, next_state in zip(
        lifecycle,
        lifecycle[1:],
    ):

        assert (
            next_state
            in contract[current_state]
        )


# =================================================
# Complete Degradation / Recovery Lifecycle
# =================================================


def test_complete_degradation_recovery_lifecycle_is_valid():

    contract = _transition_contract()

    lifecycle = [
        RuntimeOperationalState.STARTING,
        RuntimeOperationalState.READY,
        RuntimeOperationalState.RUNNING,
        RuntimeOperationalState.DEGRADED,
        RuntimeOperationalState.RUNNING,
        RuntimeOperationalState.STOPPING,
        RuntimeOperationalState.STOPPED,
    ]

    for current_state, next_state in zip(
        lifecycle,
        lifecycle[1:],
    ):

        assert (
            next_state
            in contract[current_state]
        )


# =================================================
# Failure Paths
# =================================================


def test_starting_failure_path_is_valid():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.FAILED
        in contract[
            RuntimeOperationalState.STARTING
        ]
    )


def test_running_failure_path_is_valid():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.FAILED
        in contract[
            RuntimeOperationalState.RUNNING
        ]
    )


def test_degraded_failure_path_is_valid():

    contract = _transition_contract()

    assert (
        RuntimeOperationalState.FAILED
        in contract[
            RuntimeOperationalState.DEGRADED
        ]
    )


# =================================================
# Authoritative State Enumeration
# =================================================


def test_runtime_operational_state_has_exactly_seven_members():

    assert len(
        list(RuntimeOperationalState)
    ) == 7


def test_runtime_operational_state_values_are_unique():

    values = [
        state.value
        for state in RuntimeOperationalState
    ]

    assert (
        len(values)
        == len(set(values))
    )


# =================================================
# Lifecycle Contract Does Not Introduce
# Trading Permission
# =================================================


def test_lifecycle_state_does_not_expose_trading_permission():

    for state in RuntimeOperationalState:

        assert not hasattr(
            state,
            "can_trade",
        )

        assert not hasattr(
            state,
            "live_approved",
        )


# =================================================
# Lifecycle Contract Does Not Introduce
# Credentials
# =================================================


def test_lifecycle_state_does_not_expose_credentials():

    for state in RuntimeOperationalState:

        assert not hasattr(
            state,
            "password",
        )

        assert not hasattr(
            state,
            "api_key",
        )

        assert not hasattr(
            state,
            "bot_token",
        )