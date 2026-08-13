"""
=================================================
Project Phoenix
Trading Protection
M61.8.3 - Runtime Health Protection Policy
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from deployment.runtime_watchdog import (
    WatchdogHealthState,
)


# =========================================================
# Trading Protection State
# =========================================================

class TradingProtectionState(Enum):
    """
    Trading permission state.

    ACTIVE
        New trading activity is permitted.

    PAUSED
        New trading activity is blocked because
        runtime health is not safe.
    """

    ACTIVE = "ACTIVE"

    PAUSED = "PAUSED"


# =========================================================
# Protection Transition
# =========================================================

@dataclass(frozen=True)
class ProtectionTransition:
    """
    Represents a trading protection state transition.
    """

    previous_state: TradingProtectionState

    current_state: TradingProtectionState


# =========================================================
# Trading Protection
# =========================================================

class TradingProtection:
    """
    Controls whether new trading activity is permitted.

    M61.8.3 responsibilities:
    - Translate watchdog health into trading permission
    - Pause new trading when health becomes unhealthy
    - Resume new trading after health recovery
    - Track protection state transitions

    M61.8.3 does NOT:
    - stop Runtime
    - restart Runtime
    - close existing positions
    - cancel existing orders
    - execute trades
    """

    def __init__(self) -> None:

        self.state = (
            TradingProtectionState.ACTIVE
        )

        self.last_transition: (
            ProtectionTransition | None
        ) = None

    # --------------------------------------------------
    # Update Protection
    # --------------------------------------------------

    def update(
        self,
        health_state: WatchdogHealthState,
    ) -> TradingProtectionState:
        """
        Update trading protection from runtime health.
        """

        if (
            health_state
            == WatchdogHealthState.HEALTHY
        ):

            target_state = (
                TradingProtectionState.ACTIVE
            )

        else:

            target_state = (
                TradingProtectionState.PAUSED
            )

        if target_state != self.state:

            self.last_transition = (
                ProtectionTransition(
                    previous_state=self.state,
                    current_state=target_state,
                )
            )

            self.state = target_state

        return self.state

    # --------------------------------------------------
    # Trading Permission
    # --------------------------------------------------

    def can_trade(
        self,
    ) -> bool:
        """
        Return True when new trading activity
        is currently permitted.
        """

        return (
            self.state
            == TradingProtectionState.ACTIVE
        )

    # --------------------------------------------------
    # Pause Status
    # --------------------------------------------------

    def is_paused(
        self,
    ) -> bool:
        """
        Return True when new trading activity
        is currently paused.
        """

        return (
            self.state
            == TradingProtectionState.PAUSED
        )

    # --------------------------------------------------
    # Transition Detection
    # --------------------------------------------------

    def has_transitioned(
        self,
    ) -> bool:
        """
        Return True when the most recent update
        changed the protection state.
        """

        return (
            self.last_transition
            is not None
        )

    # --------------------------------------------------
    # Clear Transition
    # --------------------------------------------------

    def clear_transition(
        self,
    ) -> None:
        """
        Clear the stored protection transition.

        Current protection state is not changed.
        """

        self.last_transition = None