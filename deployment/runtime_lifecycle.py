"""
=================================================
Project Phoenix
Runtime Lifecycle
M62.7.1 - Runtime Lifecycle Transition Contract
=================================================
"""

from __future__ import annotations

from types import MappingProxyType

from deployment.runtime_operational_state import (
    RuntimeOperationalState,
)


class RuntimeLifecycle:
    """
    Authoritative runtime lifecycle transition contract.

    This class defines which RuntimeOperationalState
    transitions are valid.

    Responsibilities:
    - define valid lifecycle transitions
    - validate lifecycle transitions
    - expose terminal-state information
    - preserve one authoritative lifecycle contract

    This class does not:
    - start the runtime
    - stop the runtime
    - execute trades
    - control TradingProtection
    - execute strategies
    - modify risk
    - send alerts
    - restart the runtime
    """

    _TRANSITIONS = MappingProxyType(
        {
            RuntimeOperationalState.STARTING: frozenset(
                {
                    RuntimeOperationalState.READY,
                    RuntimeOperationalState.FAILED,
                }
            ),
            RuntimeOperationalState.READY: frozenset(
                {
                    RuntimeOperationalState.RUNNING,
                    RuntimeOperationalState.FAILED,
                }
            ),
            RuntimeOperationalState.RUNNING: frozenset(
                {
                    RuntimeOperationalState.DEGRADED,
                    RuntimeOperationalState.STOPPING,
                    RuntimeOperationalState.FAILED,
                }
            ),
            RuntimeOperationalState.DEGRADED: frozenset(
                {
                    RuntimeOperationalState.RUNNING,
                    RuntimeOperationalState.STOPPING,
                    RuntimeOperationalState.FAILED,
                }
            ),
            RuntimeOperationalState.STOPPING: frozenset(
                {
                    RuntimeOperationalState.STOPPED,
                }
            ),
            RuntimeOperationalState.STOPPED: frozenset(),
            RuntimeOperationalState.FAILED: frozenset(),
        }
    )

    @classmethod
    def can_transition(
        cls,
        current_state: RuntimeOperationalState,
        next_state: RuntimeOperationalState,
    ) -> bool:
        """
        Return True when the requested lifecycle transition
        is explicitly permitted.
        """

        return (
            next_state
            in cls._TRANSITIONS.get(
                current_state,
                frozenset(),
            )
        )

    @classmethod
    def validate_transition(
        cls,
        current_state: RuntimeOperationalState,
        next_state: RuntimeOperationalState,
    ) -> None:
        """
        Validate a lifecycle transition.

        Raises:
            ValueError:
                when the transition is not permitted.
        """

        if not cls.can_transition(
            current_state,
            next_state,
        ):
            raise ValueError(
                (
                    "Invalid runtime lifecycle "
                    f"transition: "
                    f"{current_state.value} -> "
                    f"{next_state.value}"
                )
            )

    @classmethod
    def allowed_transitions(
        cls,
        state: RuntimeOperationalState,
    ) -> frozenset[
        RuntimeOperationalState
    ]:
        """
        Return the immutable set of states that may
        immediately follow the supplied state.
        """

        return cls._TRANSITIONS.get(
            state,
            frozenset(),
        )

    @classmethod
    def is_terminal(
        cls,
        state: RuntimeOperationalState,
    ) -> bool:
        """
        Return True when the supplied lifecycle state
        has no outgoing transitions.
        """

        return not cls.allowed_transitions(
            state
        )

    @classmethod
    def is_operational(
        cls,
        state: RuntimeOperationalState,
    ) -> bool:
        """
        Return True when the runtime is operational.

        RUNNING and DEGRADED are both operational
        lifecycle states.

        This does NOT grant trading permission.
        """

        return state in (
            RuntimeOperationalState.RUNNING,
            RuntimeOperationalState.DEGRADED,
        )

    @classmethod
    def transition_map(
        cls,
    ) -> MappingProxyType:
        """
        Return the immutable authoritative transition map.
        """

        return cls._TRANSITIONS