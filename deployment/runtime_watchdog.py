"""
=================================================
Project Phoenix
Runtime Health Watchdog
M61.8.1 - Runtime Health Watchdog Foundation
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from deployment.health_monitor import (
    HealthMonitor,
)


# =========================================================
# Watchdog Health State
# =========================================================

class WatchdogHealthState(Enum):
    """
    Runtime watchdog health state.

    M61.8.1 currently distinguishes only the
    observed health condition.

    Severity/action policy is intentionally
    deferred to a later M61.8 milestone.
    """

    HEALTHY = "HEALTHY"

    UNHEALTHY = "UNHEALTHY"


# =========================================================
# Health Transition
# =========================================================

@dataclass(frozen=True)
class HealthTransition:
    """
    Represents a health state transition.
    """

    previous_state: WatchdogHealthState

    current_state: WatchdogHealthState


# =========================================================
# Runtime Watchdog
# =========================================================

class RuntimeWatchdog:
    """
    Monitors runtime health transitions.

    M61.8.1 responsibilities:
    - Read health from HealthMonitor
    - Track current watchdog state
    - Detect health state transitions
    - Detect recovery
    - Preserve a structured transition record

    M61.8.1 does NOT:
    - stop the runtime
    - stop trading
    - pause the runner
    - restart the runtime
    """

    def __init__(
        self,
        health_monitor: HealthMonitor | None = None,
    ) -> None:

        self.health_monitor = (
            health_monitor
            if health_monitor is not None
            else HealthMonitor()
        )

        self.state = (
            WatchdogHealthState.HEALTHY
        )

        self.last_transition: (
            HealthTransition | None
        ) = None

    # --------------------------------------------------
    # Read Current Health
    # --------------------------------------------------

    def current_state(
        self,
    ) -> WatchdogHealthState:
        """
        Read the current health condition from
        HealthMonitor.
        """

        healthy = (
            self.health_monitor.is_healthy()
        )

        if healthy:

            return (
                WatchdogHealthState.HEALTHY
            )

        return (
            WatchdogHealthState.UNHEALTHY
        )

    # --------------------------------------------------
    # Check Health
    # --------------------------------------------------

    def check(
        self,
    ) -> WatchdogHealthState:
        """
        Check runtime health and update watchdog state.

        Returns the current watchdog state.
        """

        observed_state = (
            self.current_state()
        )

        if (
            observed_state
            != self.state
        ):

            self.last_transition = (
                HealthTransition(
                    previous_state=self.state,
                    current_state=observed_state,
                )
            )

            self.state = (
                observed_state
            )

        return self.state

    # --------------------------------------------------
    # Transition Detection
    # --------------------------------------------------

    def has_transitioned(
        self,
    ) -> bool:
        """
        Return True when the most recent check
        detected a state transition.
        """

        return (
            self.last_transition
            is not None
        )

    # --------------------------------------------------
    # Recovery Detection
    # --------------------------------------------------

    def has_recovered(
        self,
    ) -> bool:
        """
        Return True when the most recent transition
        represents recovery from unhealthy to healthy.
        """

        transition = (
            self.last_transition
        )

        if transition is None:

            return False

        return (
            transition.previous_state
            == WatchdogHealthState.UNHEALTHY
            and
            transition.current_state
            == WatchdogHealthState.HEALTHY
        )

    # --------------------------------------------------
    # Clear Transition
    # --------------------------------------------------

    def clear_transition(
        self,
    ) -> None:
        """
        Clear the stored transition.

        This does not change the current health state.
        """

        self.last_transition = None